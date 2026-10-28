<script setup lang="ts">
interface Zone { id: string; src: string; title: string; text: string; alt: string; w: number; h: number }

const zones: Zone[] = [
  { id: 'hall', src: '/img/hall.jpg', title: 'Главный зал', text: 'Просторный и уютный, для встреч с друзьями', alt: 'Главный зал с бирюзовыми диванами и проектором', w: 857, h: 1087 },
  { id: 'ps5', src: '/img/ps5.jpg', title: 'PS5', text: 'Четыре приставки и большие экраны для игры компанией', alt: 'Зона с PS5: телевизоры и диваны', w: 640, h: 1073 },
  { id: 'bill', src: '/img/billiard.jpg', title: 'Бильярд', text: 'Большой стол рядом с баром', alt: 'Бильярдный стол под зелёными лампами', w: 645, h: 1101 },
  { id: 'cab', src: '/img/cabins.jpg', title: 'Кабинки', text: 'Закрываются шторами, для тихого вечера', alt: 'Кабинки, отделённые бархатными шторами', w: 860, h: 1090 },
  { id: 'cin', src: '/img/cinema.jpg', title: 'Кино', text: 'Проектор для фильмов и матчей', alt: 'Зал с проектором и телевизорами', w: 628, h: 1100 }
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
    g.querySelectorAll<HTMLElement>('.ph').forEach(el => io.observe(el))
    onBeforeUnmount(() => io.disconnect())
  }
  // точки под галереей на телефоне
  g.addEventListener('scroll', () => {
    const first = g.querySelector<HTMLElement>('.ph')
    if (!first) return
    active.value = Math.min(zones.length - 1, Math.round(g.scrollLeft / (first.offsetWidth + 12)))
  }, { passive: true })
})
</script>

<template>
  <section id="zones" class="section tight">
    <div class="wrap">
      <div class="head">
        <div>
          <div class="eyebrow">Атмосфера</div>
          <h2>Как у нас</h2>
        </div>
        <p>Пять зон под любой вечер, от шумной компании до тихого разговора.</p>
      </div>

      <div ref="gallery" class="gallery">
        <figure
          v-for="z in zones"
          :key="z.id"
          :data-id="z.id"
          class="ph"
          :class="[`g-${z.id}`, { in: shown.has(z.id) }]"
          tabindex="0"
          role="button"
          :aria-label="`Открыть фото: ${z.title}`"
          @click="viewer = z"
          @keydown.enter.prevent="viewer = z"
          @keydown.space.prevent="viewer = z"
        >
          <NuxtImg
            :src="z.src"
            :alt="z.alt"
            :width="z.w"
            :height="z.h"
            sizes="xs:90vw md:50vw lg:760px"
            loading="lazy"
            format="webp"
          />
          <figcaption>
            <h3>{{ z.title }}</h3>
            <p>{{ z.text }}</p>
          </figcaption>
        </figure>
      </div>
      <div class="dots" aria-hidden="true">
        <i v-for="(z, i) in zones" :key="z.id" :class="{ on: i === active }" />
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
        <div v-if="viewer" class="viewer" @click="viewer = null">
          <img :src="viewer.src" :alt="viewer.alt">
          <UButton class="close" icon="i-lucide-x" color="neutral" variant="outline" square aria-label="Закрыть" @click.stop="viewer = null" />
        </div>
      </template>
    </UModal>
  </section>
</template>

<style scoped>
.gallery {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 280px 280px 300px;
  grid-template-areas: "hall hall ps5" "hall hall bill" "cab cin cin";
}
.g-hall { grid-area: hall; }
.g-ps5 { grid-area: ps5; }
.g-bill { grid-area: bill; }
.g-cab { grid-area: cab; }
.g-cin { grid-area: cin; }

.ph {
  position: relative;
  margin: 0;
  border-radius: var(--r);
  overflow: hidden;
  border: 1px solid var(--line);
  cursor: zoom-in;
  background: var(--panel);
  min-width: 0;
  isolation: isolate;
  transition: border-color .4s;
}
.ph img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 1.2s cubic-bezier(.2, .7, .2, 1), filter .6s;
}
.g-cin img { object-position: 85% 38%; }
.g-ps5 img { object-position: 50% 45%; }
.g-hall img { object-position: 50% 60%; }
.g-cab img { object-position: 40% 55%; }
.ph.in img { animation: settle 1.6s cubic-bezier(.2, .7, .2, 1); }
@keyframes settle { from { transform: scale(1.14); } to { transform: scale(1); } }

.ph::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: radial-gradient(120% 90% at 50% 110%, rgba(227, 0, 15, 0), rgba(227, 0, 15, 0));
  transition: background .6s;
}
.ph::after { content: ""; position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, transparent 40%, rgba(19, 15, 17, .92)); }
figcaption { position: absolute; left: 20px; right: 20px; bottom: 18px; z-index: 2; }
h3 { font-size: clamp(1.6rem, 2.6vw, 2.1rem); text-transform: uppercase; line-height: 1; display: flex; align-items: center; gap: 12px; }
h3::before { content: ""; width: 22px; height: 3px; background: var(--red); border-radius: 2px; transition: width .5s cubic-bezier(.2, .7, .2, 1); flex: none; }
.g-hall h3 { font-size: clamp(2.2rem, 4.4vw, 3.6rem); }
figcaption p { margin: 6px 0 0; color: var(--muted); font-size: .88rem; line-height: 1.4; max-width: 38ch; transition: color .4s; }

.ph:hover, .ph:focus-visible { border-color: rgba(227, 0, 15, .38); }
.ph:hover img, .ph:focus-visible img { transform: scale(1.07); }
.ph:hover::before, .ph:focus-visible::before { background: radial-gradient(120% 90% at 50% 110%, rgba(227, 0, 15, .35), rgba(227, 0, 15, 0) 60%); }
.ph:hover h3::before, .ph:focus-visible h3::before { width: 48px; }
.ph:hover p, .ph:focus-visible p { color: var(--fg); }
@media (hover: hover) { .gallery:hover .ph:not(:hover) img { filter: brightness(.6) saturate(.8); } }

.dots { display: none; justify-content: center; gap: 8px; margin-top: 16px; }
.dots i { width: 7px; height: 7px; border-radius: 50%; background: rgba(243, 236, 228, .22); transition: background .3s, width .3s; }
.dots i.on { background: var(--red); width: 22px; border-radius: 4px; }

.viewer { position: relative; width: 100%; height: 100dvh; display: flex; align-items: center; justify-content: center; padding: calc(20px + env(safe-area-inset-top, 0px)) var(--gutter-r) calc(20px + env(safe-area-inset-bottom, 0px)) var(--gutter-l); cursor: zoom-out; }
.viewer img { max-width: 100%; max-height: 100%; border-radius: 12px; object-fit: contain; }
.close { position: absolute; top: calc(14px + env(safe-area-inset-top, 0px)); right: calc(14px + env(safe-area-inset-right, 0px)); border-radius: 999px; }

@media (max-width: 860px) {
  .gallery { grid-template-columns: 1fr 1fr; grid-template-rows: 300px 220px 220px; grid-template-areas: "hall hall" "ps5 bill" "cab cin"; }
}
@media (max-width: 600px) {
  /* на телефоне галерея листается пальцем */
  .gallery {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scrollbar-width: none;
    margin-inline: calc(-1 * var(--gutter-l)) calc(-1 * var(--gutter-r));
    padding-inline: var(--gutter-l) var(--gutter-r);
    scroll-padding-inline: var(--gutter-l);
  }
  .gallery::-webkit-scrollbar { display: none; }
  .ph { flex: 0 0 82%; height: 430px; scroll-snap-align: start; }
  h3, .g-hall h3 { font-size: 2.2rem; }
  .g-cin img { object-position: 85% 50%; }
  .dots { display: flex; }
}
@media (prefers-reduced-motion: reduce) {
  .ph img, h3::before { transition: none; }
  .ph.in img { animation: none; }
  .ph:hover img { transform: none; }
}
</style>
