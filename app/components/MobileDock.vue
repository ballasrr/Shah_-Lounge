<script setup lang="ts">
// Нижняя панель на телефоне: появляется после первого экрана и прячется в разделе брони
import { venue } from '~/data/venue'

const show = ref(false)

function update() {
  const book = document.getElementById('book')
  const hero = document.getElementById('hero')
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
  <div
    class="fixed inset-x-0 bottom-0 z-25 hidden grid-cols-[1fr_1.4fr] gap-2.5 border-t border-line bg-ink/92 pt-2.5 pr-(--gutter-r) pb-[calc(10px+env(safe-area-inset-bottom,0px))] pl-(--gutter-l) backdrop-blur-[10px] transition-transform duration-350 ease-[cubic-bezier(.2,.7,.2,1)] phone:grid"
    :class="show ? 'translate-y-0' : 'translate-y-[110%]'"
  >
    <UButton :href="`tel:${venue.phone.tel}`" class="btn-outline" size="lg" icon="i-lucide-phone" label="Позвонить" />
    <UButton to="#book" size="lg" label="Забронировать" />
  </div>
</template>
