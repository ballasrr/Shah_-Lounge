<script setup lang="ts">
// Полное меню в виде книжки: страницы перелистываются с 3D-анимацией
const open = defineModel<boolean>('open', { default: false })

const pages = [
  { src: '/img/menu-2.jpg', alt: 'Меню Шах: кофе, не кофе, смузи, фреши, шоты' },
  { src: '/img/menu-1.jpg', alt: 'Меню Шах: чаи, лимонады, молочные коктейли, напитки' }
]

const page = ref(0)
const leaving = ref<{ src: string; alt: string; dir: 1 | -1 } | null>(null)
const busy = computed(() => leaving.value !== null)

watch(open, v => { if (v) { page.value = 0; leaving.value = null } })

function turn(dir: 1 | -1) {
  const to = page.value + dir
  if (busy.value || to < 0 || to >= pages.length) return
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { page.value = to; return }
  leaving.value = { ...pages[page.value]!, dir }
  page.value = to
}

function onStage(e: MouseEvent) {
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect()
  turn(e.clientX > r.left + r.width / 2 ? 1 : -1)
}

let sx: number | null = null
const touchStart = (e: TouchEvent) => (sx = e.touches[0]?.clientX ?? null)
function touchEnd(e: TouchEvent) {
  if (sx === null) return
  const dx = (e.changedTouches[0]?.clientX ?? sx) - sx
  if (Math.abs(dx) > 40) turn(dx < 0 ? 1 : -1)
  sx = null
}

function onKey(e: KeyboardEvent) {
  if (!open.value) return
  if (e.key === 'ArrowRight') turn(1)
  if (e.key === 'ArrowLeft') turn(-1)
}
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <UModal
    v-model:open="open"
    fullscreen
    title="Меню Шах"
    description="Полное меню, две страницы"
    :ui="{ content: 'bg-[rgba(10,8,9,.96)]', header: 'sr-only', body: 'p-0 sm:p-0' }"
  >
    <template #body>
      <div class="book">
        <UButton class="close" icon="i-lucide-x" color="neutral" variant="outline" square aria-label="Закрыть меню" @click="open = false" />
        <div class="stage" @click="onStage" @touchstart.passive="touchStart" @touchend="touchEnd">
          <div :key="`p${page}`" class="sheet" :class="{ rise: busy }">
            <img :src="pages[page]!.src" :alt="pages[page]!.alt">
          </div>
          <div
            v-if="leaving"
            class="sheet top"
            :class="leaving.dir > 0 ? 'turn-next' : 'turn-prev'"
            @animationend.self="leaving = null"
          >
            <img :src="leaving.src" alt="">
          </div>
        </div>
        <div class="bar">
          <UButton class="btn-outline" icon="i-lucide-chevron-left" :disabled="page === 0" aria-label="Предыдущая страница" @click="turn(-1)">
            <span class="hide-sm">Назад</span>
          </UButton>
          <div class="count">{{ page + 1 }} / {{ pages.length }}</div>
          <UButton class="btn-outline" trailing-icon="i-lucide-chevron-right" :disabled="page === pages.length - 1" aria-label="Следующая страница" @click="turn(1)">
            <span class="hide-sm">Перелистнуть</span>
          </UButton>
        </div>
        <p class="hint">Листайте стрелками или свайпом</p>
      </div>
    </template>
  </UModal>
</template>

<style scoped>
.book {
  position: relative;
  height: 100%;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding: calc(64px + env(safe-area-inset-top, 0px)) var(--gutter-r) calc(20px + env(safe-area-inset-bottom, 0px)) var(--gutter-l);
}
.close { position: absolute; top: calc(14px + env(safe-area-inset-top, 0px)); right: calc(14px + env(safe-area-inset-right, 0px)); border-radius: 999px; }
.stage { position: relative; width: min(1100px, 100%); aspect-ratio: 1600 / 1143; max-height: calc(100dvh - 190px); perspective: 2200px; cursor: pointer; }
.sheet { position: absolute; inset: 0; transform-style: preserve-3d; will-change: transform; }
.sheet img { width: 100%; height: 100%; object-fit: contain; display: block; border-radius: 10px; box-shadow: 0 30px 80px rgba(0, 0, 0, .6); }
.sheet::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 10px;
  pointer-events: none;
  opacity: 0;
  background: linear-gradient(90deg, rgba(0, 0, 0, .7), rgba(0, 0, 0, .15) 60%, rgba(255, 255, 255, .08));
}
.sheet.top { z-index: 2; }
.turn-next { transform-origin: 0% 50%; animation: turnNext .42s cubic-bezier(.6, 0, .3, 1) forwards; }
.turn-prev { transform-origin: 100% 50%; animation: turnPrev .42s cubic-bezier(.6, 0, .3, 1) forwards; }
.turn-next::after, .turn-prev::after { animation: shade .42s ease-in forwards; }
.rise { animation: rise2 .42s cubic-bezier(.2, .8, .2, 1) both; }
@keyframes turnNext { 0% { transform: none; } 35% { transform: rotateY(-25deg) skewY(1.5deg) scale(1.02); } 100% { transform: rotateY(-120deg) translateX(-6%) scale(.96); opacity: 0; } }
@keyframes turnPrev { 0% { transform: none; } 35% { transform: rotateY(25deg) skewY(-1.5deg) scale(1.02); } 100% { transform: rotateY(120deg) translateX(6%) scale(.96); opacity: 0; } }
@keyframes shade { to { opacity: 1; } }
@keyframes rise2 { from { transform: scale(.94); filter: brightness(.45); } to { transform: none; filter: none; } }

.bar { display: flex; align-items: center; gap: 14px; }
.count { min-width: 4.5em; text-align: center; color: var(--muted); font-weight: 700; font-variant-numeric: tabular-nums; }
.hint { color: var(--muted); font-size: .82rem; margin: 0; }
@media (max-width: 560px) { .hide-sm { display: none; } }
@media (prefers-reduced-motion: reduce) { .turn-next, .turn-prev, .rise, .sheet::after { animation: none !important; } }
</style>
