#!/usr/bin/env bash
# Первый деплой «Шах Lounge» на Ubuntu/Debian: Node.js, сборка Nuxt, nginx и бесплатный HTTPS.
#
#   sudo git clone https://github.com/<аккаунт>/<репозиторий>.git /var/www/shah
#   sudo bash /var/www/shah/deploy/deploy.sh shah-lounge.duckdns.org
#
# Дальше обновлять сайт: sudo bash /var/www/shah/deploy/update.sh
set -euo pipefail

DOMAIN="${1:?Укажи домен: sudo bash deploy/deploy.sh shah-lounge.duckdns.org}"
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC="$APP_DIR/.output/public"

[ "$(id -u)" -eq 0 ] || { echo "Запусти через sudo"; exit 1; }
cd "$APP_DIR"

echo "==> Системные пакеты: nginx, certbot, curl, python3"
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y nginx certbot python3-certbot-nginx curl ca-certificates python3-venv python3-pip

echo "==> Node.js 22"
if ! command -v node >/dev/null || [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 20 ]; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
fi
node -v

# Сборке Nuxt нужно ~1,5 ГБ памяти. На маленьком VPS добавляем файл подкачки, чтобы сборка не упала.
MEM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
if [ "$MEM_MB" -lt 1800 ] && ! swapon --show | grep -q .; then
  echo "==> Памяти ${MEM_MB} МБ — создаю swap 2 ГБ"
  fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
  chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

echo "$DOMAIN" > "$APP_DIR/deploy/.domain"

echo "==> Установка зависимостей и сборка сайта"
npm ci --no-audit --no-fund
NUXT_SITE_URL="https://$DOMAIN" npm run generate
[ -f "$PUBLIC/index.html" ] || { echo "Сборка не создала $PUBLIC/index.html"; exit 1; }

echo "==> Бэкенд API: venv, зависимости и systemd-служба"
# Сайт статический, а статусы столов отдаёт FastAPI из backend/. В nginx ниже /api/ уходит на него.
[ -d "$APP_DIR/backend/.venv" ] || python3 -m venv "$APP_DIR/backend/.venv"
"$APP_DIR/backend/.venv/bin/pip" install --no-cache-dir -r "$APP_DIR/backend/requirements.txt"

cat > /etc/systemd/system/shah-api.service <<EOF
[Unit]
Description=Шах Lounge API (FastAPI)
After=network.target

[Service]
WorkingDirectory=$APP_DIR/backend
# ключ iiko лежит здесь; нет файла — сервер отдаёт тестовые данные
EnvironmentFile=-$APP_DIR/backend/.env
ExecStart=$APP_DIR/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3
User=www-data

[Install]
WantedBy=multi-user.target
EOF
chown -R www-data:www-data "$APP_DIR/backend"
systemctl daemon-reload
systemctl enable --now shah-api
systemctl restart shah-api
for _ in $(seq 1 20); do
  curl -fsS http://127.0.0.1:8000/api/health >/dev/null && break
  sleep 1
done
curl -fsS http://127.0.0.1:8000/api/health >/dev/null \
  || { echo "API не отвечает на 127.0.0.1:8000 — смотри journalctl -u shah-api"; exit 1; }

echo "==> Проверяю, не занят ли порт 80 другой программой"
if ss -ltnp | grep -E ':80\s' | grep -vq nginx; then
  ss -ltnp | grep -E ':80\s'
  echo "Порт 80 занят не nginx. Освободи его и запусти скрипт ещё раз."; exit 1
fi

echo "==> Настраиваю nginx для $DOMAIN"
cat > /etc/nginx/sites-available/shah <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;

    root $PUBLIC;
    index index.html;

    # статусы столов: сайт статический, а /api отдаёт FastAPI на 127.0.0.1:8000
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        try_files \$uri \$uri/ \$uri/index.html =404;
    }

    # файлы сборки и картинки с хешем в имени можно кешировать надолго
    location ^~ /_nuxt/ { expires 1y; add_header Cache-Control "public, immutable"; }
    location ^~ /_ipx/  { expires 30d; add_header Cache-Control "public"; }
    location ^~ /img/   { expires 7d;  add_header Cache-Control "public"; }

    error_page 404 /404.html;

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml application/xml;
}
EOF
ln -sf /etc/nginx/sites-available/shah /etc/nginx/sites-enabled/shah
nginx -t
systemctl enable --now nginx
systemctl reload nginx

if command -v ufw >/dev/null && ufw status | grep -q "Status: active"; then
  echo "==> Открываю порты 80 и 443"
  ufw allow 80/tcp && ufw allow 443/tcp
fi

echo "==> Получаю бесплатный HTTPS-сертификат (Let's Encrypt)"
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email --redirect

echo ""
echo "Готово! Сайт: https://$DOMAIN"
echo "Обновить сайт после изменений: sudo bash $APP_DIR/deploy/update.sh"
