<script setup lang="ts">
// Логотип «Шах», который «включается» как неоновая вывеска — всё рисуется на canvas:
// 1) контур прорисовывается неоновой линией, 2) наливается красным, 3) проявляются надписи,
// 4) вывеска мигает и загорается, 5) дальше мягко «дышит» свечением.
import { emblemPaths, emblemViewBox } from '~/data/logo'

const wrap = ref<HTMLDivElement>()
const canvas = ref<HTMLCanvasElement>()

const RED = '#e3000f'
const WHITE = '#f3ece4'
const T = { draw: 1400, fillStart: 1250, fillEnd: 1700, textStart: 1500, textEnd: 2000, flickerStart: 1800, flickerEnd: 2600 }
const FLICKER: [number, number][] = [[0, 1], [0.08, 0.25], [0.12, 1], [0.22, 0.4], [0.26, 1], [0.44, 0.7], [0.48, 1], [1, 1]]

// запас по краям холста, чтобы свечение не обрезалось
const PAD = 24

const clamp = (v: number) => Math.min(1, Math.max(0, v))
const span = (t: number, a: number, b: number) => clamp((t - a) / (b - a))
const ease = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2)

function flicker(t: number) {
  const p = span(t, T.flickerStart, T.flickerEnd)
  if (p <= 0 || p >= 1) return 1
  for (let i = 1; i < FLICKER.length; i++) {
    const [x1, y1] = FLICKER[i]!
    const [x0, y0] = FLICKER[i - 1]!
    if (p <= x1) return y0 + (y1 - y0) * ((p - x0) / (x1 - x0))
  }
  return 1
}

let raf = 0
let visible = true
let io: IntersectionObserver | undefined
let ro: ResizeObserver | undefined

onMounted(() => {
  const el = canvas.value!
  const ctx = el.getContext('2d')!
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches

  const red = emblemPaths.filter(p => p.kind === 'r').map(p => ({ ...p, path: new Path2D(p.d), len: 0 }))
  const white = emblemPaths.filter(p => p.kind === 'w').map(p => ({ ...p, path: new Path2D(p.d) }))

  // Длины контуров нужны для эффекта «прорисовки» — меряем их через временный SVG
  const svgNS = 'http://www.w3.org/2000/svg'
  const probe = document.createElementNS(svgNS, 'svg')
  probe.setAttribute('style', 'position:absolute;width:0;height:0;visibility:hidden')
  document.body.appendChild(probe)
  for (const r of red) {
    const p = document.createElementNS(svgNS, 'path')
    p.setAttribute('d', r.d)
    probe.appendChild(p)
    r.len = Math.ceil(p.getTotalLength())
  }
  probe.remove()

  let scale = 1
  let dpr = 1
  // Готовая вывеска рисуется один раз в отдельный холст, дальше просто копируется со свечением
  const done = document.createElement('canvas')

  function resize() {
    const w = wrap.value!.clientWidth
    const h = (w * emblemViewBox.h) / emblemViewBox.w
    dpr = Math.min(window.devicePixelRatio || 1, 2)
    el.width = Math.round((w + PAD * 2) * dpr)
    el.height = Math.round((h + PAD * 2) * dpr)
    el.style.width = `${w + PAD * 2}px`
    el.style.height = `${h + PAD * 2}px`
    el.style.margin = `${-PAD}px`
    scale = w / emblemViewBox.w
    done.width = el.width
    done.height = el.height
    const d = done.getContext('2d')!
    d.setTransform(dpr * scale, 0, 0, dpr * scale, PAD * dpr, PAD * dpr)
    d.clearRect(-1e5, -1e5, 2e5, 2e5)
    d.fillStyle = RED
    red.forEach(r => d.fill(r.path, r.rule))
    d.fillStyle = WHITE
    white.forEach(w => d.fill(w.path, w.rule))
  }

  function toLogo() {
    ctx.setTransform(dpr * scale, 0, 0, dpr * scale, PAD * dpr, PAD * dpr)
  }

  function frame(t: number) {
    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.clearRect(0, 0, el.width, el.height)

    if (t >= T.flickerEnd) {
      // Вывеска горит: мягкое «дыхание» свечения
      const breath = 0.5 + 0.5 * Math.sin(((t - T.flickerEnd) / 5000) * Math.PI * 2)
      ctx.shadowColor = `rgba(227, 0, 15, ${0.18 + 0.12 * breath})`
      ctx.shadowBlur = (8 + 10 * breath) * dpr
      ctx.drawImage(done, 0, 0)
      ctx.shadowBlur = 0
      return
    }

    const alpha = flicker(t)
    ctx.globalAlpha = alpha
    toLogo()

    // 1. неоновая линия контура
    const draw = ease(span(t, 0, T.draw))
    const strokeFade = 1 - span(t, T.fillStart, T.fillEnd)
    if (strokeFade > 0) {
      ctx.strokeStyle = RED
      ctx.lineWidth = 2.2 / scale
      ctx.lineJoin = 'round'
      ctx.shadowColor = 'rgba(255, 43, 54, .7)'
      ctx.shadowBlur = 10 * dpr
      ctx.globalAlpha = alpha * strokeFade
      for (const r of red) {
        ctx.setLineDash([r.len, r.len])
        ctx.lineDashOffset = r.len * (1 - draw)
        ctx.stroke(r.path)
      }
      ctx.setLineDash([])
    }

    // 2. заливка красным
    const fill = span(t, T.fillStart, T.fillEnd)
    if (fill > 0) {
      ctx.globalAlpha = alpha * fill
      ctx.shadowBlur = 0
      ctx.fillStyle = RED
      red.forEach(r => ctx.fill(r.path, r.rule))
    }

    // 3. белые надписи «Кофе Бар» и HOOKAH BAR
    const text = span(t, T.textStart, T.textEnd)
    if (text > 0) {
      ctx.globalAlpha = alpha * text
      ctx.fillStyle = WHITE
      white.forEach(w => ctx.fill(w.path, w.rule))
    }

    ctx.globalAlpha = 1
    ctx.shadowBlur = 0
  }

  resize()

  if (reduce) {
    frame(T.flickerEnd)
    ro = new ResizeObserver(() => { resize(); frame(T.flickerEnd) })
    ro.observe(wrap.value!)
    return
  }

  let start = 0
  const loop = (now: number) => {
    if (!start) start = now
    if (visible) frame(now - start)
    raf = requestAnimationFrame(loop)
  }
  raf = requestAnimationFrame(loop)

  // не тратим батарею, когда логотип не на экране
  io = new IntersectionObserver(([e]) => (visible = !!e?.isIntersecting))
  io.observe(el)
  ro = new ResizeObserver(() => resize())
  ro.observe(wrap.value!)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  io?.disconnect()
  ro?.disconnect()
})

defineExpose({ el: wrap })
</script>

<template>
  <div ref="wrap" class="logo-neon">
    <canvas ref="canvas" role="img" aria-label="Логотип Шах — кофе-бар, hookah bar" />
  </div>
</template>

<style scoped>
.logo-neon {
  position: relative;
  width: 100%;
  aspect-ratio: 4374.8 / 6319.1;
}
canvas { display: block; }
</style>
