# Шах Lounge

Сайт кофе-бара и кальянной «Шах Lounge» в Махачкале.

Стек: Nuxt 4, Vue 3, TypeScript, Nuxt UI, Nuxt Image, sitemap, robots и Schema.org для SEO.
Сайт собирается в статический HTML (`nuxt generate`), поэтому поисковики получают готовую страницу, а на сервере хватает nginx.

## Запуск у себя

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

## Обновление

После `git push` с изменениями:

```bash
sudo bash /var/www/shah/deploy/update.sh
```
