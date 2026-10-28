<script setup lang="ts">
import { menu, type Price } from '~/data/menu'

const active = ref(menu[0]!.id)
const tabs = menu.map(t => ({ label: t.label, value: t.id }))
const current = computed(() => menu.find(t => t.id === active.value)!)
const bookOpen = ref(false)

const rub = (n: number) => `${n.toLocaleString('ru-RU')} ₽`
const prices = (p: Price) => (Array.isArray(p) ? p : [p])
const sizes = (s?: string | [string, string]) => (s ? (Array.isArray(s) ? s : [s]) : [])
</script>

<template>
  <section id="menu" class="scroll-mt-[72px] py-[clamp(56px,9vw,108px)] phone:py-14">
    <div class="shell">
      <SectionHead eyebrow="Меню" title="Что подаём" />

      <div class="mb-[30px] overflow-x-auto scrollbar-none phone:bleed-x">
        <UTabs
          v-model="active"
          :items="tabs"
          :content="false"
          variant="pill"
          color="primary"
          :ui="{
            root: 'w-max',
            list: 'bg-transparent p-0 gap-2 w-max',
            // красим саму кнопку: стандартная подложка Nuxt UI квадратнее рамки и даёт щели по краям
            trigger: 'rounded-full px-[18px] py-[10px] text-[.92rem] font-bold shrink-0 grow-0 border border-line before:hidden data-[state=active]:border-brand data-[state=active]:bg-brand data-[state=inactive]:text-mist hover:data-[state=inactive]:text-cream'
          }"
        />
      </div>

      <Transition
        mode="out-in"
        enter-active-class="transition-opacity duration-150"
        leave-active-class="transition-opacity duration-150"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div :key="active" class="columns-2 gap-x-16 phone:columns-1">
          <section
            v-for="(g, gi) in current.groups"
            :key="g.title"
            class="mb-9 animate-fade-in break-inside-avoid motion-reduce:animate-none"
            :style="{ animationDelay: `${gi * 50}ms` }"
          >
            <h3 class="mb-2.5 flex items-baseline gap-3 text-[1.9rem] leading-none uppercase after:h-0.5 after:flex-1 after:-translate-y-1.5 after:bg-brand after:opacity-85 after:content-[''] phone:text-[1.7rem]">{{ g.title }}</h3>
            <div v-if="g.sizes" class="grid grid-cols-[1fr_auto] items-baseline gap-3 pt-0.5 pb-1 text-[.78rem] font-bold tracking-[.06em] text-mist uppercase">
              <span />
              <span class="flex gap-3.5 font-bold whitespace-nowrap tabular-nums"><span v-for="s in sizes(g.sizes)" :key="s" class="min-w-[4.6em] text-right">{{ s }}</span></span>
            </div>
            <div v-for="it in g.items" :key="it.name" class="grid grid-cols-[1fr_auto] items-baseline gap-3 py-[7px]">
              <div class="flex min-w-0 items-baseline gap-2.5 after:min-w-3 after:flex-1 after:-translate-y-1 after:border-b after:border-dotted after:border-line after:content-['']">
                <span class="flex-initial">{{ it.name }}<small v-if="it.note" class="block text-[.8rem] leading-[1.3] text-mist">{{ it.note }}</small></span>
              </div>
              <span class="flex gap-3.5 font-bold whitespace-nowrap tabular-nums"><span v-for="(p, i) in prices(it.price)" :key="i" class="min-w-[4.6em] text-right">{{ rub(p) }}</span></span>
            </div>
          </section>
        </div>
      </Transition>

      <UButton class="btn-outline mt-1" size="lg" icon="i-lucide-book-open" label="Открыть меню целиком" @click="bookOpen = true" />
      <MenuBook v-model:open="bookOpen" />
    </div>
  </section>
</template>
