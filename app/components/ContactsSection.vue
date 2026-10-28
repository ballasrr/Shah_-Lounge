<script setup lang="ts">
import { venue, weekdays } from '~/data/venue'

const status = useOpenStatus()
const socials = [
  { href: `https://wa.me/${venue.phone.whatsapp}`, icon: 'i-simple-icons-whatsapp', label: 'WhatsApp', meta: venue.phone.display },
  { href: venue.links.twoGis, icon: 'i-lucide-map-pin', label: 'Отзывы в 2ГИС', meta: `${venue.rating} ★` },
  { href: venue.links.instagram, icon: 'i-simple-icons-instagram', label: 'Instagram', meta: venue.links.instagramHandle }
]
</script>

<template>
  <section id="contacts" class="section tight">
    <div class="wrap">
      <div class="head">
        <div>
          <div class="eyebrow">Контакты</div>
          <h2>Как нас найти</h2>
        </div>
      </div>

      <div class="contacts">
        <div>
          <h3>Адрес</h3>
          <figure class="facade">
            <NuxtImg src="/img/facade.jpg" alt="Фасад здания с вывеской Шах на втором этаже" width="642" height="1101" sizes="xs:90vw md:360px" loading="lazy" format="webp" />
          </figure>
          <address>
            {{ venue.address.city }}, {{ venue.address.street }}<br>
            <span>{{ venue.address.hint }}</span>
          </address>
          <div class="row">
            <UButton :to="venue.links.twoGis" target="_blank" class="btn-outline" icon="i-lucide-map" label="Открыть в 2ГИС" />
            <UButton :to="venue.links.yandexMaps" target="_blank" class="btn-outline" icon="i-lucide-navigation" label="Яндекс Карты" />
          </div>
        </div>

        <div>
          <h3>Часы работы</h3>
          <table class="hours">
            <tbody>
              <tr v-for="(d, i) in weekdays" :key="d" :class="{ today: status?.today === i }">
                <td>{{ d }}</td>
                <td>{{ pad(venue.hours[i]![0]) }} — {{ pad(venue.hours[i]![1]) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h3>Соцсети</h3>
          <div class="social">
            <a v-for="s in socials" :key="s.label" :href="s.href" target="_blank" rel="noopener">
              <span><UIcon :name="s.icon" class="ic" /> {{ s.label }}</span>
              <small>{{ s.meta }}</small>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.contacts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
h3 { font-size: 1.7rem; text-transform: uppercase; margin-bottom: 12px; }
.facade { margin: 0 0 18px; border-radius: var(--r); overflow: hidden; border: 1px solid var(--line); aspect-ratio: 4 / 3; }
.facade img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; display: block; }
address { font-style: normal; margin: 0 0 16px; }
address span { color: var(--muted); }
.row { display: flex; flex-wrap: wrap; gap: 10px; }
.hours { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.hours td { padding: 7px 0; border-bottom: 1px solid var(--line); }
.hours td:last-child { text-align: right; }
.hours tr.today td { color: var(--red-hi); font-weight: 700; }
.social { display: flex; flex-direction: column; gap: 10px; }
.social a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 1px solid var(--line);
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: border-color .2s, color .2s;
}
.social a span { display: inline-flex; align-items: center; gap: 10px; }
.ic { width: 18px; height: 18px; }
.social a:hover { border-color: var(--red-hi); color: var(--red-hi); }
.social small { color: var(--muted); font-weight: 500; }

@media (max-width: 860px) { .contacts { grid-template-columns: 1fr; gap: 32px; } }
@media (max-width: 760px) { .row > * { flex: 1 1 0; } }
</style>
