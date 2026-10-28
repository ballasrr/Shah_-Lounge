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
  <div class="shell grid grid-cols-4 border-b border-line phone:grid-cols-2">
    <div
      v-for="f in facts"
      :key="f.title"
      class="min-w-0 border-r border-line px-5 py-[26px] last:border-r-0 phone:px-3.5 phone:py-5 phone:nth-2:border-r-0 phone:nth-[-n+2]:border-b"
    >
      <strong class="block font-display text-[1.9rem] leading-[1.1] font-bold phone:text-[1.55rem]">
        {{ f.title }} <span v-if="f.star" class="text-brand">★</span>
      </strong>
      <small class="text-[.9rem] text-mist">{{ f.text }}</small>
    </div>
  </div>
</template>
