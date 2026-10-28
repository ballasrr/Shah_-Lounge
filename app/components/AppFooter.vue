<template>
  <footer>
    <div class="wrap row">
      <LogoWide class="logo" />
      <span>© Шах Lounge, Махачкала</span>
      <span>18+ · Курение вредит вашему здоровью</span>
    </div>
  </footer>
</template>

<style scoped>
footer { border-top: 1px solid var(--line); padding-block: 28px; color: var(--muted); font-size: .85rem; }
.row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; }
.logo { height: 26px; width: auto; display: block; }
@media (max-width: 760px) { footer { padding-bottom: calc(96px + env(safe-area-inset-bottom, 0px)); } }
</style>
