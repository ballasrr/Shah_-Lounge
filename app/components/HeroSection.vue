<script setup lang="ts">
import { venue } from '~/data/venue'

const status = useOpenStatus()
const logo = ref<{ el?: HTMLElement }>()
const logoEl = computed(() => logo.value?.el ?? null)
</script>

<template>
  <section class="hero">
    <HeroSmoke :source="logoEl" />
    <div class="wrap hero-grid">
      <div class="hero-text">
        <p class="status" :class="{ open: status?.open }">
          <i />
          <span v-if="!status">{{ venue.address.city }} · {{ venue.address.street }}</span>
          <span v-else-if="status.open"><b>Открыто</b> · сегодня до {{ pad(status.hour) }}</span>
          <span v-else><b>Закрыто</b> · откроемся в {{ pad(status.hour) }}</span>
        </p>
        <h1>Шах <em>Lounge</em></h1>
        <p class="sub">{{ venue.tagline }}</p>
        <p class="lead">{{ venue.lead }}</p>
        <div class="cta">
          <UButton to="#book" size="xl" label="Забронировать стол" />
          <UButton to="#menu" size="xl" class="btn-outline" label="Смотреть меню" />
        </div>
      </div>
      <div class="emblem">
        <LogoNeon ref="logo" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero { position: relative; overflow: hidden; border-bottom: 1px solid var(--line); }
.hero-grid {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.15fr .85fr;
  align-items: center;
  gap: 40px;
  padding-block: clamp(56px, 8vw, 104px);
}
.hero-text { min-width: 0; }
h1 {
  font-size: clamp(4rem, 11vw, 8.5rem);
  line-height: .88;
  text-transform: uppercase;
  margin: 16px 0 0;
  animation: rise .9s cubic-bezier(.2, .7, .2, 1) both;
}
h1 em { font-style: normal; color: var(--red); }
.sub {
  font-family: var(--display);
  font-weight: 500;
  font-size: clamp(1.4rem, 3vw, 2rem);
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 6px 0 0;
  animation: rise .9s .1s both;
}
.lead { max-width: 36ch; font-size: clamp(1rem, 2vw, 1.15rem); color: var(--muted); margin: 20px 0 30px; animation: rise .9s .2s both; }
.cta { display: flex; flex-wrap: wrap; gap: 12px; animation: rise .9s .3s both; }
.emblem { justify-self: center; width: min(330px, 100%); }

.status { display: inline-flex; align-items: center; gap: 10px; font-size: .9rem; color: var(--muted); margin: 0; animation: rise .9s both; }
.status i { width: 9px; height: 9px; border-radius: 50%; background: var(--muted); }
.status.open i { background: #55c27a; animation: pulse 2.2s infinite; }
.status b { color: var(--fg); font-weight: 700; }
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(85, 194, 122, .55); }
  70% { box-shadow: 0 0 0 9px rgba(85, 194, 122, 0); }
  100% { box-shadow: 0 0 0 0 rgba(85, 194, 122, 0); }
}

@media (max-width: 820px) {
  .hero-grid { grid-template-columns: 1fr; gap: 28px; padding-block: 36px 56px; }
  .emblem { order: -1; width: min(210px, 58%); }
}
@media (max-width: 760px) {
  .sub { letter-spacing: .08em; font-size: 1.35rem; }
  .cta { display: grid; grid-template-columns: 1fr; gap: 10px; }
}
@media (prefers-reduced-motion: reduce) {
  h1, .sub, .lead, .cta, .status, .status.open i { animation: none; }
}
</style>
