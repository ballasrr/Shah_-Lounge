<script setup lang="ts">
import { venue } from '~/data/venue'

const facts = [
  { title: venue.rating, star: true, text: 'рейтинг в 2ГИС' },
  { title: 'Бильярд', text: 'большой стол в отдельной зоне' },
  { title: 'PS5 и кино', text: '4 приставки, проектор и большие экраны' },
  { title: 'Кофе с собой', text: 'заходите по пути' }
]
</script>

<template>
  <div class="wrap facts">
    <div v-for="f in facts" :key="f.title">
      <strong>{{ f.title }} <span v-if="f.star">★</span></strong>
      <small>{{ f.text }}</small>
    </div>
  </div>
</template>

<style scoped>
.facts { display: grid; grid-template-columns: repeat(4, 1fr); border-bottom: 1px solid var(--line); }
.facts div { padding: 26px 20px; border-right: 1px solid var(--line); min-width: 0; }
.facts div:last-child { border-right: 0; }
strong { display: block; font-family: var(--display); font-size: 1.9rem; font-weight: 700; line-height: 1.1; }
strong span { color: var(--red); }
small { color: var(--muted); font-size: .9rem; }
@media (max-width: 760px) {
  .facts { grid-template-columns: repeat(2, 1fr); }
  .facts div { padding: 20px 14px; }
  .facts div:nth-child(2) { border-right: 0; }
  .facts div:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
  strong { font-size: 1.55rem; }
}
</style>
