<script setup lang="ts">
import { venue } from '~/data/venue'

const toast = useToast()

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
  <section id="book" class="section tight">
    <div class="wrap">
      <div class="head">
        <div>
          <div class="eyebrow">Бронь</div>
          <h2>Забронировать стол</h2>
        </div>
        <p>Позвоните или отправьте заявку в WhatsApp, мы подтвердим бронь.</p>
      </div>

      <div class="book">
        <div class="card">
          <div class="eyebrow">Телефон для брони</div>
          <div id="booking-phone" class="phone">{{ venue.phone.display }}</div>
          <div class="row">
            <UButton :href="`tel:${venue.phone.tel}`" size="lg" icon="i-lucide-phone" label="Позвонить" />
            <UButton :to="`https://wa.me/${venue.phone.whatsapp}`" target="_blank" size="lg" class="btn-outline" icon="i-simple-icons-whatsapp" label="WhatsApp" />
            <UButton size="lg" class="btn-outline copy" icon="i-lucide-copy" label="Скопировать номер" @click="copyPhone" />
          </div>
          <p class="small">На вечер пятницы и выходных лучше бронировать заранее.</p>
        </div>

        <form class="card form" @submit.prevent>
          <UFormField label="Имя" class="full">
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
          <UButton :to="waLink" target="_blank" size="xl" block class="full" icon="i-simple-icons-whatsapp" label="Отправить заявку в WhatsApp" />
        </form>
      </div>
    </div>
  </section>
</template>

<style scoped>
.book { display: grid; grid-template-columns: 1fr 1.1fr; gap: 20px; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--r); padding: clamp(22px, 4vw, 36px); min-width: 0; }
.phone {
  font-family: var(--display);
  font-weight: 700;
  font-size: clamp(2.4rem, 6vw, 3.4rem);
  line-height: 1;
  margin: 14px 0 20px;
  user-select: all;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
.row { display: flex; flex-wrap: wrap; gap: 10px; }
.small { color: var(--muted); font-size: .9rem; margin: 18px 0 0; }
.form { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-content: start; }
.full { grid-column: 1 / -1; }

@media (max-width: 860px) { .book { grid-template-columns: 1fr; } }
@media (max-width: 760px) {
  .phone { font-size: clamp(2rem, 10vw, 2.6rem); }
  .row { display: grid; grid-template-columns: 1fr 1fr; }
  .copy { grid-column: 1 / -1; }
}
@media (max-width: 480px) { .form { grid-template-columns: 1fr; } }
</style>
