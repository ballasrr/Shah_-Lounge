<script setup lang="ts">
// cell — место в сетке, pos — какую часть фото показывать, h3 — размер заголовка
interface Zone { id: string; src: string; title: string; text: string; alt: string; w: number; h: number; cell?: string; pos?: string; h3?: string }

const zones: Zone[] = [
  { id: 'hall', src: '/img/hall.jpg', title: 'Главный зал', text: 'Просторный и уютный, для встреч с друзьями', alt: 'Главный зал с бирюзовыми диванами и проектором', w: 857, h: 1087, cell: 'col-span-2 row-span-2 tablet:row-span-1', pos: 'object-[50%_60%]', h3: 'text-[clamp(2.2rem,4.4vw,3.6rem)]' },
  { id: 'ps5', src: '/img/ps5.jpg', title: 'PS5', text: 'Четыре приставки и большие экраны для игры компанией', alt: 'Зона с PS5: телевизоры и диваны', w: 640, h: 1073, pos: 'object-[50%_45%]' },
  { id: 'bill', src: '/img/billiard.jpg', title: 'Бильярд', text: 'Большой стол рядом с баром', alt: 'Бильярдный стол под зелёными лампами', w: 645, h: 1101 },
  { id: 'cab', src: '/img/cabins.jpg', title: 'Кабинки', text: 'Закрываются шторами, для тихого вечера', alt: 'Кабинки, отделённые бархатными шторами', w: 860, h: 1090, pos: 'object-[40%_55%]' },
  { id: 'cin', src: '/img/cinema.jpg', title: 'Кино', text: 'Проектор для фильмов и матчей', alt: 'Зал с проектором и телевизорами', w: 628, h: 1100, cell: 'col-span-2 tablet:col-span-1', pos: 'object-[85%_38%] narrow:object-[85%_50%]' }
]

const viewer = ref<Zone | null>(null)
const viewerOpen = computed({
  get: () => viewer.value !== null,
  set: v => { if (!v) viewer.value = null }
})

// Фото «садятся» на место, когда галерея появляется на экране
const gallery = ref<HTMLElement>()
const shown = ref(new Set<string>())
const active = ref(0)

onMounted(() => {
  const g = gallery.value!
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) {
        shown.value.add((e.target as HTMLElement).dataset.id!)
        io.unobserve(e.target)
      }
    }), { threshold: 0.25 })
    g.querySelectorAll<HTMLElement>('figure').forEach(el => io.observe(el))
    onBeforeUnmount(() => io.disconnect())
  }
  // точки под галереей на телефоне
  g.addEventListener('scroll', () => {
    const first = g.querySelector<HTMLElement>('figure')
    if (!first) return
    active.value = Math.min(zones.length - 1, Math.round(g.scrollLeft / (first.offsetWidth + 12)))
  }, { passive: true })
})
</script>

<template>
  <section id="zones" class="scroll-mt-[72px] pb-[clamp(56px,9vw,108px)] phone:pb-14">
    <div class="shell">
      <SectionHead eyebrow="Атмосфера" title="Как у нас">
        Пять зон под любой вечер, от шумной компании до тихого разговора.
      </SectionHead>

      <div
        ref="gallery"
        class="grid grid-cols-3 grid-rows-[280px_280px_300px] gap-3.5 tablet:grid-cols-2 tablet:grid-rows-[300px_220px_220px] narrow:flex narrow:snap-x narrow:snap-mandatory narrow:gap-3 narrow:overflow-x-auto narrow:scroll-px-(--gutter-l) narrow:bleed-x scrollbar-none [@media(hover:hover)]:[&:hover_figure:not(:hover)_img]:brightness-60 [@media(hover:hover)]:[&:hover_figure:not(:hover)_img]:saturate-80"
      >
        <figure
          v-for="z in zones"
          :key="z.id"
          :data-id="z.id"
          class="group relative isolate m-0 min-w-0 cursor-zoom-in overflow-hidden rounded-card border border-line bg-panel transition-[border-color] duration-400 before:pointer-events-none before:absolute before:inset-0 before:z-1 before:bg-[radial-gradient(120%_90%_at_50%_110%,rgba(227,0,15,.35),transparent_60%)] before:opacity-0 before:transition-opacity before:duration-600 before:content-[''] after:absolute after:inset-0 after:z-1 after:bg-[linear-gradient(180deg,transparent_40%,rgba(19,15,17,.92))] after:content-[''] hover:border-brand/40 hover:before:opacity-100 focus-visible:border-brand/40 focus-visible:before:opacity-100 narrow:h-[430px] narrow:flex-[0_0_82%] narrow:snap-start"
          :class="z.cell"
          tabindex="0"
          role="button"
          :aria-label="`Открыть фото: ${z.title}`"
          @click="viewer = z"
          @keydown.enter.prevent="viewer = z"
          @keydown.space.prevent="viewer = z"
        >
          <NuxtImg
            class="absolute inset-0 block size-full object-cover [transition:scale_1.2s_cubic-bezier(.2,.7,.2,1),filter_.6s] group-hover:scale-[1.07] group-focus-visible:scale-[1.07] motion-reduce:transition-none motion-reduce:group-hover:scale-100"
            :class="[z.pos, shown.has(z.id) && 'animate-settle motion-reduce:animate-none']"
            :src="z.src"
            :alt="z.alt"
            :width="z.w"
            :height="z.h"
            sizes="xs:90vw md:50vw lg:760px"
            loading="lazy"
            format="webp"
          />
          <figcaption class="absolute inset-x-5 bottom-[18px] z-2">
            <h3
              class="flex items-center gap-3 leading-none uppercase before:h-[3px] before:w-[22px] before:flex-none before:rounded-sm before:bg-brand before:transition-[width] before:duration-500 before:ease-[cubic-bezier(.2,.7,.2,1)] before:content-[''] group-hover:before:w-12 group-focus-visible:before:w-12 motion-reduce:before:transition-none narrow:text-[2.2rem]"
              :class="z.h3 ?? 'text-[clamp(1.6rem,2.6vw,2.1rem)]'"
            >{{ z.title }}</h3>
            <p class="mt-1.5 mb-0 max-w-[38ch] text-[.88rem] leading-[1.4] text-mist transition-colors duration-400 group-hover:text-cream group-focus-visible:text-cream">{{ z.text }}</p>
          </figcaption>
        </figure>
      </div>
      <div class="mt-4 hidden justify-center gap-2 narrow:flex" aria-hidden="true">
        <i
          v-for="(z, i) in zones"
          :key="z.id"
          class="h-[7px] transition-all duration-300"
          :class="i === active ? 'w-[22px] rounded-[4px] bg-brand' : 'w-[7px] rounded-full bg-cream/20'"
        />
      </div>
    </div>

    <UModal
      v-model:open="viewerOpen"
      fullscreen
      :title="viewer?.title"
      :description="viewer?.text"
      :ui="{ content: 'bg-[rgba(10,8,9,.95)]', header: 'sr-only', body: 'p-0 sm:p-0 flex items-center justify-center' }"
    >
      <template #body>
        <div
          v-if="viewer"
          class="relative flex h-dvh w-full cursor-zoom-out items-center justify-center pt-[calc(20px+env(safe-area-inset-top,0px))] pr-(--gutter-r) pb-[calc(20px+env(safe-area-inset-bottom,0px))] pl-(--gutter-l)"
          @click="viewer = null"
        >
          <img class="max-h-full max-w-full rounded-xl object-contain" :src="viewer.src" :alt="viewer.alt">
          <UButton
            class="absolute top-[calc(14px+env(safe-area-inset-top,0px))] right-[calc(14px+env(safe-area-inset-right,0px))] rounded-full"
            icon="i-lucide-x"
            color="neutral"
            variant="outline"
            square
            aria-label="Закрыть"
            @click.stop="viewer = null"
          />
        </div>
      </template>
    </UModal>
  </section>
</template>
