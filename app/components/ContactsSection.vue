<script setup lang="ts">
import { venue, weekdays } from '~/data/venue'

const status = useOpenStatus()
const h3 = 'mb-3 text-[1.7rem] uppercase'
const socials = [
  { href: `https://wa.me/${venue.phone.whatsapp}`, icon: 'i-simple-icons-whatsapp', label: 'WhatsApp', meta: venue.phone.display },
  { href: venue.links.twoGis, icon: 'i-lucide-map-pin', label: 'Отзывы в 2ГИС', meta: `${venue.rating} ★` },
  { href: venue.links.instagram, icon: 'i-simple-icons-instagram', label: 'Instagram', meta: venue.links.instagramHandle }
]
</script>

<template>
  <section id="contacts" class="scroll-mt-[72px] pb-[clamp(56px,9vw,108px)] phone:pb-14">
    <div class="shell">
      <SectionHead eyebrow="Контакты" title="Как нас найти" />

      <div class="grid grid-cols-3 gap-10 tablet:grid-cols-1 tablet:gap-8">
        <div>
          <h3 :class="h3">Адрес</h3>
          <figure class="m-0 mb-[18px] aspect-[4/3] overflow-hidden rounded-card border border-line">
            <NuxtImg class="block size-full object-cover object-[50%_40%]" src="/img/facade.jpg" alt="Фасад здания с вывеской Шах на втором этаже" width="642" height="1101" sizes="xs:90vw md:360px" loading="lazy" format="webp" />
          </figure>
          <address class="mb-4 not-italic">
            {{ venue.address.city }}, {{ venue.address.street }}<br>
            <span class="text-mist">{{ venue.address.hint }}</span>
          </address>
          <div class="flex flex-wrap gap-2.5 phone:*:flex-1">
            <UButton :to="venue.links.twoGis" target="_blank" class="btn-outline" icon="i-lucide-map" label="Открыть в 2ГИС" />
            <UButton :to="venue.links.yandexMaps" target="_blank" class="btn-outline" icon="i-lucide-navigation" label="Яндекс Карты" />
          </div>
        </div>

        <div>
          <h3 :class="h3">Часы работы</h3>
          <table class="w-full border-collapse tabular-nums">
            <tbody>
              <tr v-for="(d, i) in weekdays" :key="d" :class="status?.today === i && 'font-bold text-brand-hi'">
                <td class="border-b border-line py-[7px]">{{ d }}</td>
                <td class="border-b border-line py-[7px] text-right">{{ pad(venue.hours[i]![0]) }} — {{ pad(venue.hours[i]![1]) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h3 :class="h3">Соцсети</h3>
          <div class="flex flex-col gap-2.5">
            <a
              v-for="s in socials"
              :key="s.label"
              :href="s.href"
              target="_blank"
              rel="noopener"
              class="flex items-center justify-between gap-3 rounded-[10px] border border-line px-4 py-3 font-semibold transition-colors duration-200 hover:border-brand-hi hover:text-brand-hi"
            >
              <span class="inline-flex items-center gap-2.5"><UIcon :name="s.icon" class="size-[18px]" /> {{ s.label }}</span>
              <small class="font-medium text-mist">{{ s.meta }}</small>
            </a>
          </div>
        </div>
      </div>

      <TwoGisMap class="mt-10 tablet:mt-8" />
    </div>
  </section>
</template>
