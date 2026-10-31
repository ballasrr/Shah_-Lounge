# Шах Lounge

Сайт кофе-бара и кальянной «Шах Lounge» в Махачкале.

Стек: Nuxt 4, Vue 3, TypeScript, Nuxt UI, Nuxt Image, sitemap, robots и Schema.org для SEO.
Сайт собирается в статический HTML (`nuxt generate`), поэтому поисковики получают готовую страницу, а на сервере хватает nginx.

## Запуск в Docker — одной командой

Нужен только Docker (на Windows и Mac — Docker Desktop).

```bash
docker compose up -d --build
```

- сайт: http://localhost:8080
- API бэкенда: http://localhost:8080/api/tables, описание — http://localhost:8080/api/docs

Поднимаются два контейнера: `web` (сайт собирается в статику, nginx отдаёт её и передаёт `/api` дальше) и `api` (бэкенд на Python, см. `backend/README.md`).
Ключ iiko кладётся в `backend/.env`; без него бэкенд отдаёт тестовые данные.
Порт и адрес сайта меняются в `.env` рядом с `docker-compose.yml`: `PORT=80`, `SITE_URL=https://shah-lounge.ru`.

```bash
docker compose logs -f   # логи
docker compose down      # остановить
```

После изменений в коде — снова `docker compose up -d --build`.

## Запуск для разработки

Нужен Node.js 20 или новее.

```bash
npm install
npm run dev        # http://localhost:3000
npm run generate   # статическая сборка в .output/public
npm run typecheck  # проверка типов
```

## Где что править

| Что | Файл |
| --- | --- |
| Телефон, адрес, часы работы, ссылки, тексты | `app/data/venue.ts` |
| Меню и цены | `app/data/menu.ts` |
| Фото зон и подписи к ним | `app/components/GallerySection.vue`, сами фото в `public/img/` |
| Страницы бумажного меню | `public/img/menu-1.jpg`, `public/img/menu-2.jpg` |
| Заголовок и описание для поисковиков, разметка Schema.org | `app/pages/index.vue` |
| Цвета и шрифты | `app/assets/css/main.css` |

## Как устроено

- `app/components/LogoNeon.vue` — логотип на canvas: прорисовывается неоновой линией, наливается цветом, мигает и загорается.
- `app/components/HeroSmoke.vue` — дым над логотипом, тоже на canvas.
- `app/components/MenuBook.vue` — полное меню книжкой с перелистыванием.
- Фото выводятся через `<NuxtImg>`: при сборке нарезаются в WebP под разные экраны.
- Шрифты подключены из npm (`@fontsource`), сборка не ходит в Google Fonts.
- Анимации отключаются у посетителей с настройкой «уменьшить движение».

## Деплой на сервер (Ubuntu/Debian)

1. Бесплатный домен: зарегистрируй поддомен на duckdns.org и укажи IP сервера.
2. На сервере:

```bash
sudo git clone https://github.com/<аккаунт>/<репозиторий>.git /var/www/shah
sudo bash /var/www/shah/deploy/deploy.sh shah-lounge.duckdns.org
```

Скрипт ставит Node.js 22, nginx и certbot, собирает сайт, настраивает домен и получает бесплатный HTTPS-сертификат. Если на сервере меньше 2 ГБ памяти, он создаёт файл подкачки, чтобы сборка не упала.

Заодно он поднимает бэкенд: создаёт `backend/.venv`, ставит зависимости и включает systemd-службу `shah-api` (uvicorn на `127.0.0.1:8000`), а nginx передаёт ей `/api/`. Проверить: `curl https://<домен>/api/tables` и `systemctl status shah-api`. Ключ iiko кладётся в `backend/.env` уже после первого запуска — служба перезапускается командой `systemctl restart shah-api`.

## Обновление

После `git push` с изменениями:

```bash
sudo bash /var/www/shah/deploy/update.sh
```
