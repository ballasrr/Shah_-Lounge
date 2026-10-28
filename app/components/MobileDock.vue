<script setup lang="ts">
// Нижняя панель на телефоне: появляется после первого экрана и прячется в разделе брони
import { venue } from '~/data/venue'

const show = ref(false)

function update() {
  const book = document.getElementById('book')
  const hero = document.querySelector('.hero') as HTMLElement | null
  const heroOut = window.scrollY > (hero?.offsetHeight ?? 600) * 0.6
  const r = book?.getBoundingClientRect()
  const inBook = !!r && r.top < innerHeight && r.bottom > 0
  show.value = heroOut && !inBook
}

onMounted(() => {
  window.addEventListener('scroll', update, { passive: true })
  update()
})
onBeforeUnmount(() => window.removeEventListener('scroll', update))
</script>

<template>
  <div class="dock" :class="{ show }">
    <UButton :href="`tel:${venue.phone.tel}`" class="btn-outline" size="lg" icon="i-lucide-phone" label="Позвонить" />
    <UButton to="#book" size="lg" label="Забронировать" />
  </div>
</template>

<style scoped>
.dock { display: none; }
@media (max-width: 760px) {
  .dock {
    display: grid;
    grid-template-columns: 1fr 1.4fr;
    gap: 10px;
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 25;
    background: rgba(19, 15, 17, .92);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid var(--line);
    padding: 10px var(--gutter-r) calc(10px + env(safe-area-inset-bottom, 0px)) var(--gutter-l);
    transform: translateY(110%);
    transition: transform .35s cubic-bezier(.2, .7, .2, 1);
  }
  .dock.show { transform: none; }
}
</style>
