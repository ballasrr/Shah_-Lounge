<script setup lang="ts">
import { venue } from '~/data/venue'

const status = useOpenStatus()
const logo = ref<{ el?: HTMLElement }>()
const logoEl = computed(() => logo.value?.el ?? null)
</script>

<template>
  <section id="hero" class="relative overflow-hidden border-b border-line">
    <HeroVideo />
    <HeroSmoke :source="logoEl" />
    <div class="shell relative z-2 grid grid-cols-[1.15fr_.85fr] items-center gap-10 py-[clamp(56px,8vw,104px)] max-[820px]:grid-cols-1 max-[820px]:gap-4 max-[820px]:pt-5 max-[820px]:pb-10">
      <div class="min-w-0">
        <p class="m-0 inline-flex animate-rise items-center gap-2.5 text-[.9rem] text-mist motion-reduce:animate-none">
          <i class="size-[9px] rounded-full" :class="status?.open ? 'animate-pulse-ring bg-live motion-reduce:animate-none' : 'bg-mist'" />
          <span v-if="!status">{{ venue.address.city }} · {{ venue.address.street }}</span>
          <span v-else-if="status.open"><b class="font-bold text-cream">Открыто</b> · сегодня до {{ pad(status.hour) }}</span>
          <span v-else><b class="font-bold text-cream">Закрыто</b> · откроемся в {{ pad(status.hour) }}</span>
        </p>
        <h1 class="mt-4 animate-[rise_.9s_cubic-bezier(.2,.7,.2,1)_both] text-[clamp(4rem,11vw,8.5rem)] leading-[.88] uppercase motion-reduce:animate-none">Шах <em class="text-brand not-italic">Lounge</em></h1>
        <p class="mt-1.5 animate-rise font-display text-[clamp(1.4rem,3vw,2rem)] font-medium tracking-[.14em] text-mist uppercase [animation-delay:.1s] phone:text-[1.35rem] phone:tracking-[.08em] motion-reduce:animate-none">{{ venue.tagline }}</p>
        <p class="mt-5 mb-[30px] max-w-[36ch] animate-rise text-[clamp(1rem,2vw,1.15rem)] text-mist [animation-delay:.2s] motion-reduce:animate-none">{{ venue.lead }}</p>
        <div class="flex animate-rise flex-wrap gap-3 [animation-delay:.3s] phone:grid phone:grid-cols-1 phone:gap-2.5 motion-reduce:animate-none">
          <UButton to="#book" size="xl" label="Забронировать стол" />
          <UButton to="#menu" size="xl" class="btn-outline" label="Смотреть меню" />
        </div>
      </div>
      <div class="w-[min(330px,100%)] justify-self-center translate-x-[clamp(0px,5vw,72px)] max-[820px]:order-first max-[820px]:translate-x-0 max-[820px]:w-[min(150px,42%)]">
        <LogoNeon ref="logo" />
      </div>
    </div>
  </section>
</template>
