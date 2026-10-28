<script setup lang="ts">
defineProps<{ eyebrow: string; title: string }>()
</script>

<template>
  <div class="mb-[34px] flex flex-wrap items-end justify-between gap-5 phone:mb-6">
    <div class="min-w-0">
      <div class="eyebrow">{{ eyebrow }}</div>
      <h2 class="mt-2 wrap-break-word text-[clamp(2.4rem,7vw,4rem)] leading-none uppercase phone:text-[clamp(2.3rem,11vw,3rem)]">{{ title }}</h2>
    </div>
    <p v-if="$slots.default" class="m-0 max-w-[42ch] text-mist"><slot /></p>
  </div>
</template>
