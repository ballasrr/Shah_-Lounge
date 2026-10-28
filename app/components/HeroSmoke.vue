<script setup lang="ts">
// Дым, который поднимается из чашки на логотипе. Рисуется на canvas поверх первого экрана.
const props = defineProps<{
  /** элемент-источник дыма (логотип) */
  source?: HTMLElement | null
}>()

const canvas = ref<HTMLCanvasElement>()

interface Puff { x: number; y: number; r: number; vy: number; vx: number; a: number; max: number; ph: number; red: boolean }

let raf = 0
let visible = true
let io: IntersectionObserver | undefined
let ro: ResizeObserver | undefined
let restart: (() => void) | undefined

// логотип монтируется позже дыма — как только он появился, пересчитываем точку источника
watch(() => props.source, () => restart?.())

onMounted(() => {
  const el = canvas.value!
  const ctx = el.getContext('2d')!
  const host = el.parentElement!
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches
  if (still) return

  let W = 0
  let H = 0
  let src = { x: 0, y: 0, w: 1 }
  let puffs: Puff[] = []

  function size() {
    const r = host.getBoundingClientRect()
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    W = r.width
    H = r.height
    el.width = W * dpr
    el.height = H * dpr
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    const s = props.source?.getBoundingClientRect()
    if (s) src = { x: s.left - r.left + s.width * 0.5, y: s.top - r.top + s.height * 0.04, w: s.width }
  }

  function puff(init: boolean): Puff {
    const p: Puff = {
      x: src.x + (Math.random() - 0.5) * src.w * 0.12,
      y: src.y,
      r: 8 + Math.random() * 14,
      vy: 0.35 + Math.random() * 0.5,
      vx: (Math.random() - 0.5) * 0.5,
      a: 0,
      max: 0.05 + Math.random() * 0.07,
      ph: Math.random() * 6.28,
      red: Math.random() < 0.3
    }
    if (init) {
      const k = Math.random() * src.y
      p.y = src.y - k
      p.r += k * 0.35
    }
    return p
  }

  function frame() {
    if (visible) {
      ctx.clearRect(0, 0, W, H)
      for (const p of puffs) {
        p.y -= p.vy
        p.ph += 0.012
        p.x += p.vx + Math.sin(p.ph) * 0.45
        p.r += 0.32
        const life = Math.max(0, (p.y + p.r) / (src.y + 40))
        p.a = Math.min(p.max, p.a + 0.003) * Math.min(1, life * 1.4)
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r)
        const c = p.red ? '227,0,15' : '243,236,228'
        g.addColorStop(0, `rgba(${c},${p.a})`)
        g.addColorStop(1, `rgba(${c},0)`)
        ctx.fillStyle = g
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fill()
      }
      puffs = puffs.map(p => (p.y + p.r < -20 ? puff(false) : p))
    }
    raf = requestAnimationFrame(frame)
  }

  restart = () => {
    size()
    puffs = Array.from({ length: 40 }, () => puff(true))
  }
  restart()
  raf = requestAnimationFrame(frame)

  io = new IntersectionObserver(([e]) => (visible = !!e?.isIntersecting))
  io.observe(el)
  ro = new ResizeObserver(size)
  ro.observe(host)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  io?.disconnect()
  ro?.disconnect()
})
</script>

<template>
  <canvas ref="canvas" class="smoke" aria-hidden="true" />
</template>

<style scoped>
.smoke {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 3;
}
</style>
