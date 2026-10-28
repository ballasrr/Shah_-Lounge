import { venue } from '~/data/venue'

export interface OpenStatus {
  open: boolean
  /** до скольки открыто сегодня или во сколько откроется */
  hour: number
  /** индекс сегодняшнего дня, 0 = понедельник */
  today: number
}

export const pad = (h: number) => `${String(h).padStart(2, '0')}:00`

/** Текущее время в Махачкале (UTC+3) независимо от часового пояса посетителя */
function nowInMakhachkala() {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Moscow',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).formatToParts(new Date())
  const get = (t: string) => parts.find(p => p.type === t)?.value ?? '0'
  const day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(get('weekday'))
  return { day, time: (Number(get('hour')) % 24) + Number(get('minute')) / 60 }
}

export function computeStatus(): OpenStatus {
  const { day, time } = nowInMakhachkala()
  const H = venue.hours
  const prev = (day + 6) % 7
  const [pOpen, pClose] = H[prev]!
  const [open, close] = H[day]!

  // хвост вчерашней смены после полуночи
  if (pClose < pOpen && time < pClose) return { open: true, hour: pClose, today: day }
  // сегодняшняя смена
  if (time >= open && (close < open || time < close)) return { open: true, hour: close, today: day }
  return { open: false, hour: open, today: day }
}

/** Статус считается только в браузере, чтобы статичный HTML не «застывал» на времени сборки */
export function useOpenStatus() {
  const status = ref<OpenStatus | null>(null)
  onMounted(() => {
    status.value = computeStatus()
    const id = setInterval(() => (status.value = computeStatus()), 60_000)
    onBeforeUnmount(() => clearInterval(id))
  })
  return status
}
