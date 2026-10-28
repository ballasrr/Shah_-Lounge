<script setup lang="ts">
// Полное меню в виде книжки: страницы перелистываются с 3D-анимацией
const open = defineModel<boolean>('open', { default: false })

const pages = [
  { src: '/img/menu-2.jpg', alt: 'Меню Шах: кофе, не кофе, смузи, фреши, шоты' },
  { src: '/img/menu-1.jpg', alt: 'Меню Шах: чаи, лимонады, молочные коктейли, напитки' }
]

// страница книжки; затемнение при перелистывании рисует ::after
const sheet = "absolute inset-0 will-change-transform [transform-style:preserve-3d] after:pointer-events-none after:absolute after:inset-0 after:rounded-[10px] after:bg-[linear-gradient(90deg,rgba(0,0,0,.7),rgba(0,0,0,.15)_60%,rgba(255,255,255,.08))] after:opacity-0 after:content-['']"

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
      <div class="relative flex h-full min-h-dvh flex-col items-center justify-center gap-[18px] pt-[calc(64px+env(safe-area-inset-top,0px))] pr-(--gutter-r) pb-[calc(20px+env(safe-area-inset-bottom,0px))] pl-(--gutter-l)">
        <UButton
          class="absolute top-[calc(14px+env(safe-area-inset-top,0px))] right-[calc(14px+env(safe-area-inset-right,0px))] rounded-full"
          icon="i-lucide-x"
          color="neutral"
          variant="outline"
          square
          aria-label="Закрыть меню"
          @click="open = false"
        />
        <div
          class="relative aspect-[1600/1143] max-h-[calc(100dvh-190px)] w-[min(1100px,100%)] cursor-pointer [perspective:2200px]"
          @click="onStage"
          @touchstart.passive="touchStart"
          @touchend="touchEnd"
        >
          <div :key="`p${page}`" :class="[sheet, busy && 'animate-page-in motion-reduce:animate-none']">
            <img class="block size-full rounded-[10px] object-contain shadow-[0_30px_80px_rgba(0,0,0,.6)]" :src="pages[page]!.src" :alt="pages[page]!.alt">
          </div>
          <div
            v-if="leaving"
            :class="[sheet, 'z-2 after:animate-shade motion-reduce:animate-none motion-reduce:after:animate-none', leaving.dir > 0 ? 'origin-left animate-turn-next' : 'origin-right animate-turn-prev']"
            @animationend.self="leaving = null"
          >
            <img class="block size-full rounded-[10px] object-contain shadow-[0_30px_80px_rgba(0,0,0,.6)]" :src="leaving.src" alt="">
          </div>
        </div>
        <div class="flex items-center gap-3.5">
          <UButton class="btn-outline" icon="i-lucide-chevron-left" :disabled="page === 0" aria-label="Предыдущая страница" @click="turn(-1)">
            <span class="max-[560px]:hidden">Назад</span>
          </UButton>
          <div class="min-w-[4.5em] text-center font-bold text-mist tabular-nums">{{ page + 1 }} / {{ pages.length }}</div>
          <UButton class="btn-outline" trailing-icon="i-lucide-chevron-right" :disabled="page === pages.length - 1" aria-label="Следующая страница" @click="turn(1)">
            <span class="max-[560px]:hidden">Перелистнуть</span>
          </UButton>
        </div>
        <p class="m-0 text-[.82rem] text-mist">Листайте стрелками или свайпом</p>
      </div>
    </template>
  </UModal>
</template>
