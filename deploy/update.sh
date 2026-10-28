#!/usr/bin/env bash
# Обновление сайта: забрать изменения из GitHub и пересобрать.
#   sudo bash /var/www/shah/deploy/update.sh
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"
DOMAIN="$(cat deploy/.domain 2>/dev/null || true)"
[ -n "$DOMAIN" ] || { echo "Сначала запусти deploy.sh с доменом"; exit 1; }

git pull --ff-only
npm ci --no-audit --no-fund
NUXT_SITE_URL="https://$DOMAIN" npm run generate

echo "Сайт обновлён: https://$DOMAIN"
