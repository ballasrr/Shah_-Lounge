<script setup lang="ts">
// Видео на фоне всего первого экрана: кальян в дыму. На широком экране — горизонтальная нарезка, на узком — вертикальное.
// Источник выбирается после загрузки страницы, чтобы телефон не качал широкую версию и наоборот.
// При «уменьшить движение» и режиме экономии трафика остаётся только первый кадр.

const video = ref<HTMLVideoElement>()
const src = ref('')

let io: IntersectionObserver | undefined

onMounted(() => {
  const el = video.value!
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches
  const saveData = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection?.saveData
  if (still || saveData) return

  src.value = matchMedia('(max-width: 820px)').matches ? '/video/hero-tall.mp4' : '/video/hero-wide.mp4'

  // не крутим видео, когда первый экран ушёл из виду
  io = new IntersectionObserver(([e]) => {
    if (e?.isIntersecting) el.play().catch(() => {})
    else el.pause()
  })
  io.observe(el)
})
onBeforeUnmount(() => io?.disconnect())
</script>

<template>
  <div class="pointer-events-none absolute inset-0 bg-[url(/video/hero-wide.jpg)] bg-cover bg-center max-[820px]:bg-[url(/video/hero-tall.jpg)]" aria-hidden="true">
    <video
      ref="video"
      :src="src || undefined"
      class="size-full object-cover"
      muted
      loop
      playsinline
      autoplay
      preload="auto"
    />
    <!-- затемнение: текст слева и низ экрана должны читаться поверх дыма -->
    <div class="absolute inset-0 bg-ink/30" />
    <div class="absolute inset-0 bg-linear-to-r from-ink/80 via-ink/30 via-50% to-transparent max-[820px]:bg-linear-to-b max-[820px]:from-ink/10 max-[820px]:via-ink/35 max-[820px]:to-ink/90" />
    <div class="absolute inset-x-0 bottom-0 h-24 bg-linear-to-t from-ink to-transparent" />
  </div>
</template>
