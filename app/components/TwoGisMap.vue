<script setup lang="ts">
// Карта 2ГИС с карточкой заведения. Виджет тяжёлый, поэтому сначала показываем лёгкое превью:
// на компьютере карта подгружается, когда блок доходит до экрана, на телефоне — по нажатию,
// чтобы карта не перехватывала свайп при прокрутке страницы.
import { venue } from '~/data/venue'

const wrap = ref<HTMLDivElement>()
const shown = ref(false)

const src = `https://widgets.2gis.com/widget?type=firmsonmap&options=${encodeURIComponent(JSON.stringify({
  pos: { lat: venue.address.lat, lon: venue.address.lon, zoom: 17 },
  opt: { city: 'makhachkala' },
  org: venue.links.twoGisId
}))}`

const show = () => (shown.value = true)

let io: IntersectionObserver | undefined

onMounted(() => {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return
  io = new IntersectionObserver(([e]) => {
    if (!e?.isIntersecting) return
    show()
    io?.disconnect()
  }, { rootMargin: '300px' })
  io.observe(wrap.value!)
})
onBeforeUnmount(() => io?.disconnect())
</script>

<template>
  <div ref="wrap" class="relative h-[440px] overflow-hidden rounded-card border border-line bg-panel phone:h-[320px]">
    <!-- видно, пока виджет не отрисовался поверх -->
    <div v-if="shown" class="absolute inset-0 flex items-center justify-center gap-2 text-sm text-mist">
      <UIcon name="i-lucide-loader-circle" class="size-4 animate-spin" /> Загружаем карту…
    </div>
    <iframe
      v-if="shown"
      class="absolute top-0 left-0 size-full origin-top-left border-0 phone:size-[125%] phone:scale-80"
      :src="src"
      title="Шах Lounge на карте 2ГИС"
      loading="lazy"
      allow="geolocation"
    />
    <button
      v-else
      type="button"
      class="group absolute inset-0 flex cursor-pointer flex-col items-center justify-center gap-4 bg-[radial-gradient(circle_at_50%_45%,rgba(227,0,15,.16),transparent_55%),repeating-linear-gradient(28deg,transparent_0_46px,rgba(255,255,255,.035)_46px_48px),repeating-linear-gradient(-62deg,transparent_0_70px,rgba(255,255,255,.035)_70px_72px)] text-cream"
      aria-label="Показать карту 2ГИС"
      @click="show"
    >
      <span class="relative grid size-14 place-items-center rounded-full bg-brand shadow-[0_10px_30px_rgba(227,0,15,.45)]">
        <span class="absolute inset-0 animate-ping rounded-full bg-brand/40 motion-reduce:animate-none" />
        <UIcon name="i-lucide-map-pin" class="relative size-7" />
      </span>
      <span class="text-center">
        <b class="block font-display text-[1.6rem] uppercase">{{ venue.address.street }}</b>
        <span class="text-[.9rem] text-mist">{{ venue.address.hint }}</span>
      </span>
      <span class="inline-flex items-center gap-2 rounded-md border border-line px-4 py-2 text-sm font-semibold transition-colors duration-200 group-hover:border-brand-hi group-hover:text-brand-hi">
        <UIcon name="i-lucide-map" class="size-4" /> Показать карту
      </span>
    </button>
  </div>
</template>
