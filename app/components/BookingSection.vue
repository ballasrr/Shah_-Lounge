<script setup lang="ts">
import { venue } from '~/data/venue'

const toast = useToast()

const card = 'min-w-0 rounded-card border border-line bg-panel p-[clamp(22px,4vw,36px)]'

// Время брони: с открытия до 23:30 (закрываемся в 01:00)
const times: string[] = []
for (let h = 12; h <= 23; h++) for (const m of ['00', '30']) times.push(`${String(h).padStart(2, '0')}:${m}`)

const form = reactive({ name: '', date: '', time: '20:00', guests: 4, note: '' })

onMounted(() => {
  // сегодняшняя дата по Махачкале
  form.date = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Moscow' }).format(new Date())
})

const waLink = computed(() => {
  const date = form.date
    ? new Date(`${form.date}T12:00`).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })
    : ''
  const lines = [
    `Здравствуйте! Хочу забронировать стол в «${venue.name}».`,
    `Имя: ${form.name.trim() || '—'}`,
    `Дата: ${date}`,
    `Время: ${form.time}`,
    `Гостей: ${form.guests}`
  ]
  if (form.note.trim()) lines.push(`Пожелания: ${form.note.trim()}`)
  return `https://wa.me/${venue.phone.whatsapp}?text=${encodeURIComponent(lines.join('\n'))}`
})

// гость выбрал свободный стол на схеме — подставляем его в заявку
const formEl = ref<HTMLFormElement>()
function pickTable(t: { name: string; seats: number }) {
  form.note = t.name
  if (form.guests > t.seats) form.guests = t.seats
  formEl.value?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  toast.add({ title: `${t.name} добавлен в заявку`, icon: 'i-lucide-check' })
}

async function copyPhone() {
  try {
    await navigator.clipboard.writeText(venue.phone.display)
    toast.add({ title: 'Номер скопирован', icon: 'i-lucide-check' })
  } catch {
    const el = document.getElementById('booking-phone')
    if (el) {
      const r = document.createRange()
      r.selectNodeContents(el)
      const s = getSelection()
      s?.removeAllRanges()
      s?.addRange(r)
    }
    toast.add({ title: 'Номер выделен — скопируйте его', icon: 'i-lucide-copy' })
  }
}
</script>

<template>
  <section id="book" class="scroll-mt-[72px] pb-[clamp(56px,9vw,108px)] phone:pb-14">
    <div class="shell">
      <SectionHead eyebrow="Бронь" title="Забронировать стол">
        Позвоните или отправьте заявку в WhatsApp, мы подтвердим бронь.
      </SectionHead>

      <div class="grid grid-cols-[1fr_1.1fr] gap-5 tablet:grid-cols-1">
        <TablesNow class="col-span-full" @pick="pickTable" />

        <div :class="card">
          <div class="eyebrow">Телефон для брони</div>
          <div
            id="booking-phone"
            class="mt-3.5 mb-5 text-[clamp(1.9rem,4vw,2.5rem)] leading-none font-extrabold tracking-[-.02em] whitespace-nowrap select-all tabular-nums phone:text-[clamp(1.5rem,7.4vw,2rem)]"
          >{{ venue.phone.display }}</div>
          <div class="flex flex-wrap gap-2.5 phone:grid phone:grid-cols-2">
            <UButton :href="`tel:${venue.phone.tel}`" size="lg" icon="i-lucide-phone" label="Позвонить" />
            <UButton :to="`https://wa.me/${venue.phone.whatsapp}`" target="_blank" size="lg" class="btn-outline" icon="i-simple-icons-whatsapp" label="WhatsApp" />
            <UButton size="lg" class="btn-outline phone:col-span-full" icon="i-lucide-copy" label="Скопировать номер" @click="copyPhone" />
          </div>
          <p class="mt-[18px] mb-0 text-[.9rem] text-mist">На вечер пятницы и выходных лучше бронировать заранее.</p>
        </div>

        <form ref="formEl" :class="[card,'grid grid-cols-2 content-start gap-3.5 tiny:grid-cols-1']" @submit.prevent>
          <UFormField label="Имя" class="col-span-full">
            <UInput v-model="form.name" placeholder="Как к вам обращаться" autocomplete="name" size="lg" class="w-full" />
          </UFormField>
          <UFormField label="Дата">
            <UInput v-model="form.date" type="date" size="lg" class="w-full" />
          </UFormField>
          <UFormField label="Время">
            <USelect v-model="form.time" :items="times" size="lg" class="w-full" />
          </UFormField>
          <UFormField label="Гостей">
            <UInputNumber v-model="form.guests" :min="1" :max="40" size="lg" class="w-full" />
          </UFormField>
          <UFormField label="Пожелания">
            <UInput v-model="form.note" placeholder="День рождения, у окна…" size="lg" class="w-full" />
          </UFormField>
          <UButton :to="waLink" target="_blank" size="xl" block class="col-span-full" icon="i-simple-icons-whatsapp" label="Отправить заявку в WhatsApp" />
        </form>
      </div>
    </div>
  </section>
</template>
