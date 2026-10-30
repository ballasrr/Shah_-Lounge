<script setup lang="ts">
import { hallTables, hallWalls, hallZones, type HallTable } from '~/data/hall'

// Столы прямо сейчас — схема зала: свободен / занят / забронирован. Статусы берутся из бэкенда (backend/), а он — из кассы iiko; план и места — из data/hall.ts.
// Пока бэкенд отдаёт тестовые данные, блок виден только на localhost, чтобы гости не видели выдуманных статусов.

type Status = 'free' | 'busy' | 'reserved'
interface Table { id: string; number: number; name: string; seats: number; section: string; status: Status; reserved_at: string | null }
interface TablesResponse { updatedAt: string; demo: boolean; stale: boolean; tables: Table[] }

const emit = defineEmits<{ pick: [table: { number: number; name: string; seats: number }] }>()

const data = ref<TablesResponse | null>(null)
const local = ref(false)

// top — стол на плане, pill — цвет подписи статуса
const STATUS: Record<Status, { label: string; dot: string; top: string; pill: string }> = {
  free: {
    label: 'свободен',
    dot: 'bg-live',
    top: 'border-live bg-live/15 text-cream shadow-[0_0_28px_rgba(85,194,122,.28)] group-hover:bg-live/25 group-hover:shadow-[0_0_36px_rgba(85,194,122,.5)]',
    pill: 'text-live'
  },
  busy: {
    label: 'занят',
    dot: 'bg-brand',
    top: 'border-line bg-ink/60 text-mist/50',
    pill: 'text-mist/60'
  },
  reserved: {
    label: 'бронь',
    dot: 'bg-hold',
    top: 'border-hold bg-hold/12 text-cream shadow-[0_0_24px_rgba(233,162,59,.22)]',
    pill: 'text-hold'
  }
}

const visible = computed(() => !!data.value?.tables.length && (!data.value.demo || local.value))

// положение на плане: на телефоне свои координаты, переключает CSS
const place = (d: { x: number; y: number; w?: number; h?: number }, p: { x: number; y: number; w?: number; h?: number }) => ({
  '--x': `${d.x}%`, '--y': `${d.y}%`, '--w': `${d.w}%`, '--h': `${d.h}%`,
  '--px': `${p.x}%`, '--py': `${p.y}%`, '--pw': `${p.w}%`, '--ph': `${p.h}%`
})

// столы с плана со статусами из iiko; столы, которых нет на плане, не показываем
const tables = computed(() => {
  const live = new Map((data.value?.tables ?? []).map(t => [t.number, t]))
  return hallTables.flatMap((h: HallTable) => {
    const t = live.get(h.number)
    return t ? [{ ...h, id: t.id, status: t.status, reserved_at: t.reserved_at, name: h.title ?? `Стол №${h.number}` }] : []
  })
})

const counts = computed(() => {
  const c: Record<Status, number> = { free: 0, busy: 0, reserved: 0 }
  for (const t of tables.value) c[t.status]++
  return c
})

async function load() {
  try {
    data.value = await $fetch<TablesResponse>('/api/tables')
  } catch {
    // бэкенд недоступен — просто не показываем блок
  }
}

let timer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  local.value = ['localhost', '127.0.0.1'].includes(location.hostname)
  load()
  // обновляем раз в 10 секунд, пока вкладка открыта
  timer = setInterval(() => { if (!document.hidden) load() }, 10_000)
})
onBeforeUnmount(() => clearInterval(timer))
</script>

<template>
  <div v-if="visible" class="relative overflow-hidden rounded-card border border-line bg-panel p-[clamp(22px,4vw,36px)]">
    <!-- мягкая подсветка сверху, как свет над залом -->
    <div class="pointer-events-none absolute inset-x-0 -top-24 h-64 bg-[radial-gradient(ellipse_at_50%_0%,rgba(85,194,122,.12),transparent_70%)]" />

    <div class="relative mb-7 flex flex-wrap items-end justify-between gap-x-8 gap-y-4">
      <div>
        <div class="flex items-center gap-2.5">
          <i class="size-2 rounded-full bg-live animate-pulse-ring motion-reduce:animate-none" />
          <span class="eyebrow whitespace-nowrap">Столы сейчас</span>
          <UBadge v-if="data!.demo" color="neutral" variant="outline" size="sm" label="тестовые данные" />
        </div>
        <div class="mt-2.5 font-display text-[clamp(2rem,4.4vw,2.9rem)] leading-none uppercase">
          <!-- цифры в основном шрифте: в Yanone Kaffeesatz 1 и 2 ниже заглавных букв -->
          Свободно <span class="font-sans font-bold text-live">{{ counts.free }}</span> <span class="text-mist">из <span class="font-sans font-bold">{{ tables.length }}</span></span>
        </div>
      </div>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(s, key) in STATUS"
          :key="key"
          class="inline-flex items-center gap-2 rounded-full border border-line bg-ink/40 px-3 py-1.5 text-[.85rem] text-mist"
        >
          <i class="size-2.5 rounded-full" :class="s.dot" />{{ s.label }}
          <b class="font-bold text-cream tabular-nums">{{ counts[key] }}</b>
        </span>
      </div>
    </div>

    <!-- план зала: на телефоне повёрнут вертикально и помещается целиком -->
    <div class="relative">
      <div class="relative mx-auto aspect-[1000/645] max-w-[1000px] rounded-[12px] phone:aspect-[3/5] phone:max-w-[420px] border-2 border-line bg-[radial-gradient(rgba(255,255,255,.035)_1px,transparent_1px)] bg-size-[16px_16px]">
        <i
          v-for="(w, i) in hallWalls"
          :key="i"
          class="absolute top-(--y) left-(--x) h-(--h) w-(--w) bg-line phone:top-(--py) phone:left-(--px) phone:h-(--ph) phone:w-(--pw)"
          :style="place(w, w.p)"
        />
        <span
          v-for="z in hallZones"
          :key="z.name"
          class="absolute top-(--y) left-(--x) text-[.7rem] font-semibold tracking-[.08em] whitespace-nowrap text-mist/70 uppercase phone:top-(--py) phone:left-(--px) phone:text-[.62rem] phone:tracking-[.04em]"
          :style="place(z, z.p)"
        >{{ z.name }}</span>
        <div class="absolute top-[93%] left-[64%] grid h-[7%] w-[18%] place-items-center rounded-t-[6px] border border-b-0 border-line bg-ink/50 text-[.7rem] text-mist/70 uppercase phone:top-[18%] phone:left-[90%] phone:h-[20%] phone:w-[10%] phone:rounded-t-none phone:rounded-l-[6px] phone:border-r-0 phone:border-b phone:text-[.6rem]">Бар</div>
        <!-- проём входа перекрывает внешнюю стену -->
        <div class="absolute right-[6%] -bottom-[2px] h-[2px] w-[8%] bg-panel phone:top-[3%] phone:-right-[2px] phone:bottom-auto phone:h-[9%] phone:w-[2px]" />
        <span class="absolute right-[6%] bottom-[2%] flex w-[8%] justify-center gap-1 text-[.7rem] font-semibold text-mist uppercase phone:top-[3%] phone:right-0 phone:bottom-auto phone:h-[9%] phone:w-[10.5%] phone:items-center phone:text-[.58rem]">Вход</span>

        <component
          :is="t.status === 'free' ? 'button' : 'div'"
          v-for="t in tables"
          :key="t.id"
          :type="t.status === 'free' ? 'button' : undefined"
          class="group absolute top-(--y) left-(--x) grid h-(--h) w-(--w) -translate-x-1/2 -translate-y-1/2 place-items-center content-center rounded-[10px] border-2 px-1 phone:top-(--py) phone:left-(--px) phone:h-(--ph) phone:w-(--pw) phone:px-0 transition-[background-color,box-shadow,scale] duration-200 motion-reduce:transition-none"
          :class="[STATUS[t.status].top, t.status === 'free' && 'cursor-pointer hover:scale-105']"
          :style="place(t, t.p)"
          :aria-label="`${t.name}, ${t.zone}, мест: ${t.seats}, ${STATUS[t.status].label}${t.reserved_at ? ` с ${t.reserved_at}` : ''}`"
          :title="t.status === 'free' ? 'Добавить в заявку' : undefined"
          @click="t.status === 'free' && emit('pick', { number: t.number, name: t.name, seats: t.seats })"
        >
          <span class="inline-flex items-center gap-1.5 leading-none">
            <b class="font-display text-[1.2rem] leading-none" :class="t.title && 'uppercase'">{{ t.title ?? t.number }}</b>
            <span class="inline-flex items-center gap-0.5 text-[.68rem] opacity-75"><UIcon name="i-lucide-users" class="size-3 max-[360px]:hidden" />{{ t.seats }}</span>
            <UIcon v-if="t.tv" name="i-lucide-tv" class="size-3 opacity-75" />
          </span>
          <span class="mt-0.5 text-[.68rem] leading-none font-semibold whitespace-nowrap phone:text-[.62rem]" :class="STATUS[t.status].pill">
            {{ t.status === 'reserved' && t.reserved_at ? `бронь с ${t.reserved_at}` : STATUS[t.status].label }}
          </span>
        </component>
      </div>
    </div>

    <div class="relative mt-6 flex flex-wrap items-center justify-between gap-x-6 gap-y-2 text-[.85rem] text-mist">
      <span class="inline-flex items-center gap-2"><UIcon name="i-lucide-mouse-pointer-click" class="size-4 text-live" />Нажмите на свободный стол — добавим его в заявку</span>
      <span class="inline-flex items-center gap-1.5">
        <UIcon name="i-lucide-refresh-cw" class="size-3.5" />обновлено в {{ data!.updatedAt }}<template v-if="data!.stale"> · касса временно не отвечает</template>
      </span>
    </div>
  </div>
</template>
