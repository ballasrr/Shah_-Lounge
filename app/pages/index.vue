<script setup lang="ts">
import { venue } from '~/data/venue'

const site = useSiteConfig()
const title = 'Шах Lounge — кофе-бар и кальянная в Махачкале'
const ogImage = `${site.url}/og.jpg`

useSeoMeta({
  title,
  description: venue.description,
  ogTitle: title,
  ogDescription: venue.description,
  ogImage,
  ogImageWidth: 1200,
  ogImageHeight: 630,
  ogImageAlt: 'Интерьер и логотип Шах Lounge',
  ogType: 'website',
  ogLocale: 'ru_RU',
  ogSiteName: venue.name,
  twitterCard: 'summary_large_image',
  twitterImage: ogImage
})

// Разметка для Яндекса и Google: заведение, адрес, телефон, часы работы
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] as const
const pad2 = (h: number) => `${String(h).padStart(2, '0')}:00`

useSchemaOrg([
  defineFoodEstablishment({
    '@type': ['Organization', 'LocalBusiness', 'FoodEstablishment', 'CafeOrCoffeeShop'],
    name: venue.name,
    description: venue.description,
    url: site.url,
    image: [ogImage, `${site.url}/img/hall.jpg`, `${site.url}/img/facade.jpg`],
    telephone: venue.phone.tel,
    priceRange: '₽₽',
    acceptsReservations: true,
    hasMenu: `${site.url}/#menu`,
    servesCuisine: 'Кофе, чай, напитки',
    address: {
      streetAddress: venue.address.street,
      addressLocality: venue.address.city,
      postalCode: venue.address.postalCode,
      addressCountry: 'RU'
    },
    geo: { latitude: venue.address.lat, longitude: venue.address.lon },
    openingHoursSpecification: venue.hours.map(([open, close], i) => ({
      dayOfWeek: days[i]!,
      opens: pad2(open),
      closes: pad2(close)
    })),
    sameAs: [venue.links.instagram, venue.links.twoGis]
  })
])
</script>

<template>
  <div>
    <AppHeader />
    <main id="top">
      <HeroSection />
      <FactsStrip />
      <MenuSection />
      <GallerySection />
      <BookingSection />
      <ContactsSection />
    </main>
    <AppFooter />
    <MobileDock />
  </div>
</template>
