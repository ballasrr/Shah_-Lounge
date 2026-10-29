<script setup lang="ts">
// Столы прямо сейчас — схема зала: свободен / занят / забронирован. Данные берутся из бэкенда (backend/), а он — из кассы iiko.
// Пока бэкенд отдаёт тестовые данные, блок виден только на localhost, чтобы гости не видели выдуманных статусов.

type Status = 'free' | 'busy' | 'reserved'
interface Table { id: string; number: number; name: string; seats: number; section: string; status: Status; reserved_at: string | null }
interface TablesResponse { updatedAt: string; demo: boolean; stale: boolean; tables: Table[] }

const emit = defineEmits<{ pick: [table: Table] }>()

const data = ref<TablesResponse | null>(null)
const local = ref(false)

// top — столешница, chair — стулья вокруг, pill — подпись под столом
const STATUS: Record<Status, { label: string; dot: string; top: string; chair: string; pill: string }> = {
  free: {
    label: 'свободен',
    dot: 'bg-live',
    top: 'border-live bg-live/15 text-cream shadow-[0_0_28px_rgba(85,194,122,.28)] group-hover:bg-live/25 group-hover:shadow-[0_0_36px_rgba(85,194,122,.5)]',
    chair: 'bg-live/55',
    pill: 'bg-live/15 text-live'
  },
  busy: {
    label: 'занят',
    dot: 'bg-brand',
    top: 'border-line bg-ink/60 text-mist/50',
    chair: 'bg-line',
    pill: 'text-mist/60'
  },
  reserved: {
    label: 'бронь',
    dot: 'bg-hold',
    top: 'border-hold bg-hold/12 text-cream shadow-[0_0_24px_rgba(233,162,59,.22)]',
    chair: 'bg-hold/50',
    pill: 'bg-hold/15 text-hold'
  }
}

const visible = computed(() => !!data.value?.tables.length && (!data.value.demo || local.value))

const sections = computed(() => {
  const map = new Map<string, Table[]>()
  for (const t of data.value?.tables ?? []) map.set(t.section, [...(map.get(t.section) ?? []), t])
  return [...map].map(([name, tables]) => ({ name, tables, free: tables.filter(t => t.status === 'free').length }))
})

const counts = computed(() => {
  const c: Record<Status, number> = { free: 0, busy: 0, reserved: 0 }
  for (const t of data.value?.tables ?? []) c[t.status]++
  return c
})

// стулья равномерно по кругу; до 10 штук, чтобы не слипались. Если в iiko места не указаны (0) — рисуем 4
const chairs = (n: number) => {
  const k = Math.min(n || 4, 10)
  return Array.from({ length: k }, (_, i) => (360 / k) * i)
}

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
          Свободно <span class="text-live">{{ counts.free }}</span> <span class="text-mist">из {{ data!.tables.length }}</span>
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

    <!-- зоны: ширина по количеству столов, на узком экране — друг под другом -->
    <div class="relative flex flex-wrap gap-4">
      <section
        v-for="s in sections"
        :key="s.name"
        class="min-w-0 rounded-[12px] border border-dashed border-line bg-[radial-gradient(rgba(255,255,255,.035)_1px,transparent_1px)] bg-size-[16px_16px] px-4 pt-3.5 pb-4 phone:px-2"
        :style="{ flex: `${s.tables.length} 1 ${s.tables.length * 118 + 34}px` }"
      >
        <div class="mb-2 flex items-baseline justify-between gap-3">
          <h4 class="font-display text-[1.35rem] leading-none uppercase">{{ s.name }}</h4>
          <span class="text-[.78rem] text-mist">свободно {{ s.free }} из {{ s.tables.length }}</span>
        </div>

        <div class="flex flex-wrap justify-center gap-x-2 gap-y-1 [--r:43px] phone:[--r:31px] phone:gap-x-1">
          <component
            :is="t.status === 'free' ? 'button' : 'div'"
            v-for="t in s.tables"
            :key="t.id"
            :type="t.status === 'free' ? 'button' : undefined"
            class="group flex w-[110px] flex-col items-center gap-1 py-1 phone:w-[82px]"
            :class="t.status === 'free' && 'cursor-pointer'"
            :aria-label="`${t.name}${t.seats ? `, мест: ${t.seats}` : ''}, ${STATUS[t.status].label}${t.reserved_at ? ` с ${t.reserved_at}` : ''}`"
            :title="t.status === 'free' ? 'Добавить в заявку' : undefined"
            @click="t.status === 'free' && emit('pick', t)"
          >
            <span class="relative block size-[106px] transition-transform duration-200 group-hover:scale-105 phone:size-[80px]" :class="t.status !== 'free' && 'group-hover:scale-100'">
              <i
                v-for="deg in chairs(t.seats)"
                :key="deg"
                class="absolute top-1/2 left-1/2 h-[9px] w-[18px] rounded-full transition-colors phone:h-[7px] phone:w-[14px]"
                :class="STATUS[t.status].chair"
                :style="{ transform: `translate(-50%, -50%) rotate(${deg}deg) translateY(calc(-1 * var(--r)))` }"
              />
              <span
                class="absolute inset-[22px] grid place-items-center content-center rounded-full border-2 transition-[background-color,box-shadow] duration-200 phone:inset-[17px]"
                :class="STATUS[t.status].top"
              >
                <b class="font-display text-[1.55rem] leading-none phone:text-[1.2rem]">{{ t.number }}</b>
                <span v-if="t.seats" class="mt-0.5 inline-flex items-center gap-0.5 text-[.68rem] leading-none opacity-75"><UIcon name="i-lucide-users" class="size-3" />{{ t.seats }}</span>
              </span>
            </span>
            <span class="rounded-full px-2.5 py-0.5 text-[.74rem] font-semibold whitespace-nowrap" :class="STATUS[t.status].pill">
              {{ t.status === 'reserved' && t.reserved_at ? `бронь с ${t.reserved_at}` : STATUS[t.status].label }}
            </span>
          </component>
        </div>
      </section>
    </div>

    <div class="relative mt-6 flex flex-wrap items-center justify-between gap-x-6 gap-y-2 text-[.85rem] text-mist">
      <span class="inline-flex items-center gap-2"><UIcon name="i-lucide-mouse-pointer-click" class="size-4 text-live" />Нажмите на свободный стол — добавим его в заявку</span>
      <span class="inline-flex items-center gap-1.5">
        <UIcon name="i-lucide-refresh-cw" class="size-3.5" />обновлено в {{ data!.updatedAt }}<template v-if="data!.stale"> · касса временно не отвечает</template>
      </span>
    </div>
  </div>
</template>
