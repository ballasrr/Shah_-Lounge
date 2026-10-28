<script setup lang="ts">
// Карта с вкладками 2ГИС / Яндекс Карты. Виджеты тяжёлые, поэтому сначала показываем лёгкое превью:
// на компьютере карта подгружается, когда блок доходит до экрана, на телефоне — по нажатию,
// чтобы карта не перехватывала свайп при прокрутке страницы.
import { venue } from '~/data/venue'

const { lat, lon } = venue.address

// src — адрес виджета; когда будут готовые коды виджетов, заменить здесь
const maps = [
  {
    id: '2gis',
    label: '2ГИС',
    title: 'Шах Lounge на карте 2ГИС',
    src: `https://widgets.2gis.com/widget?type=firmsonmap&options=${encodeURIComponent(JSON.stringify({
      pos: { lat, lon, zoom: 17 },
      opt: { city: 'makhachkala' },
      org: venue.links.twoGisId
    }))}`,
    // на узком экране карточка заведения не помещается — рисуем карту шире и уменьшаем
    frame: 'phone:size-[125%] phone:scale-80'
  },
  {
    id: 'yandex',
    label: 'Яндекс Карты',
    title: 'Шах Lounge на Яндекс Картах',
    src: `https://yandex.ru/map-widget/v1/?ll=${lon}%2C${lat}&z=17&pt=${lon}%2C${lat}%2Cpm2rdm`,
    frame: ''
  }
]

const active = ref(maps[0]!.id)
const tabs = maps.map(m => ({ label: m.label, value: m.id }))

const wrap = ref<HTMLDivElement>()
const shown = ref(false)
// уже открытые карты не убираем из DOM, чтобы при переключении вкладок они не грузились заново
const loaded = reactive(new Set<string>())
watchEffect(() => { if (shown.value) loaded.add(active.value) })

let io: IntersectionObserver | undefined

onMounted(() => {
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return
  io = new IntersectionObserver(([e]) => {
    if (!e?.isIntersecting) return
    shown.value = true
    io?.disconnect()
  }, { rootMargin: '300px' })
  io.observe(wrap.value!)
})
onBeforeUnmount(() => io?.disconnect())
</script>

<template>
  <div ref="wrap">
    <div class="mb-3.5 overflow-x-auto scrollbar-none">
      <UTabs
        v-model="active"
        :items="tabs"
        :content="false"
        variant="pill"
        color="primary"
        :ui="{
          root: 'w-max',
          list: 'bg-transparent p-0 gap-2 w-max',
          indicator: 'rounded-full',
          trigger: 'rounded-full px-[18px] py-2 text-[.88rem] font-bold shrink-0 grow-0 border border-line data-[state=active]:border-brand data-[state=inactive]:text-mist hover:data-[state=inactive]:text-cream'
        }"
      />
    </div>

    <div class="relative h-[440px] overflow-hidden rounded-card border border-line bg-panel phone:h-[320px]">
      <template v-if="shown">
        <!-- видно, пока виджет не отрисовался поверх -->
        <div class="absolute inset-0 flex items-center justify-center gap-2 text-sm text-mist">
          <UIcon name="i-lucide-loader-circle" class="size-4 animate-spin" /> Загружаем карту…
        </div>
        <template v-for="m in maps" :key="m.id">
          <iframe
            v-if="loaded.has(m.id)"
            v-show="active === m.id"
            class="absolute top-0 left-0 size-full origin-top-left border-0"
            :class="m.frame"
            :src="m.src"
            :title="m.title"
            allow="geolocation"
          />
        </template>
      </template>
      <button
        v-else
        type="button"
        class="group absolute inset-0 flex cursor-pointer flex-col items-center justify-center gap-4 bg-[radial-gradient(circle_at_50%_45%,rgba(227,0,15,.16),transparent_55%),repeating-linear-gradient(28deg,transparent_0_46px,rgba(255,255,255,.035)_46px_48px),repeating-linear-gradient(-62deg,transparent_0_70px,rgba(255,255,255,.035)_70px_72px)] text-cream"
        aria-label="Показать карту"
        @click="shown = true"
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
  </div>
</template>
