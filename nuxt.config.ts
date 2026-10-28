// Адрес сайта для canonical, sitemap и превью ссылок. На сервере задаётся переменной NUXT_SITE_URL.
const siteUrl = process.env.NUXT_SITE_URL || 'https://shah-lounge.duckdns.org'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: ['@nuxt/ui', '@nuxt/image', '@nuxtjs/sitemap', '@nuxtjs/robots', 'nuxt-schema-org'],

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      viewport: 'width=device-width, initial-scale=1, viewport-fit=cover',
      link: [
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' }
      ],
      meta: [{ name: 'theme-color', content: '#130f11' }]
    }
  },

  site: {
    url: siteUrl,
    name: 'Шах Lounge',
    defaultLocale: 'ru'
  },

  // Сайт тёмный по задумке: логотип нарисован под тёмный фон
  colorMode: {
    preference: 'dark',
    fallback: 'dark'
  },

  // Шрифты подключены из npm в main.css — внешние провайдеры шрифтов не нужны
  fonts: {
    providers: { google: false, googleicons: false, bunny: false, fontshare: false, fontsource: false, adobe: false }
  },

  // Иконки вшиваются в сборку, без запросов к внешнему API
  icon: {
    clientBundle: { scan: true },
    serverBundle: 'local'
  },

  image: {
    format: ['webp'],
    quality: 78,
    screens: { xs: 360, sm: 640, md: 768, lg: 1024, xl: 1280, '2xl': 1536 }
  },

  nitro: {
    prerender: {
      routes: ['/'],
      crawlLinks: true
    }
  }
})
