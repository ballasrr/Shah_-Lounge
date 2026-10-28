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
  <section id="menu" class="section">
    <div class="wrap">
      <div class="head">
        <div>
          <div class="eyebrow">Меню</div>
          <h2>Что подаём</h2>
        </div>
      </div>

      <div class="tabs-scroll">
        <UTabs
          v-model="active"
          :items="tabs"
          :content="false"
          variant="pill"
          color="primary"
          :ui="{
            root: 'w-max',
            list: 'bg-transparent p-0 gap-2 w-max',
            indicator: 'rounded-full',
            trigger: 'rounded-full px-[18px] py-[10px] text-[.92rem] font-bold shrink-0 grow-0 border border-[var(--line)] data-[state=active]:border-[var(--red)] data-[state=inactive]:text-[var(--muted)] hover:data-[state=inactive]:text-[var(--fg)]'
          }"
        />
      </div>

      <Transition name="swap" mode="out-in">
        <div :key="active" class="menu">
          <section v-for="(g, gi) in current.groups" :key="g.title" class="group" :style="{ animationDelay: `${gi * 50}ms` }">
            <h3>{{ g.title }}</h3>
            <div v-if="g.sizes" class="sizes">
              <span />
              <span class="pr"><span v-for="s in sizes(g.sizes)" :key="s">{{ s }}</span></span>
            </div>
            <div v-for="it in g.items" :key="it.name" class="line">
              <div class="n">
                <span>{{ it.name }}<small v-if="it.note">{{ it.note }}</small></span>
              </div>
              <span class="pr"><span v-for="(p, i) in prices(it.price)" :key="i">{{ rub(p) }}</span></span>
            </div>
          </section>
        </div>
      </Transition>

      <UButton class="btn-outline mt-1" size="lg" icon="i-lucide-book-open" label="Открыть меню целиком" @click="bookOpen = true" />
      <MenuBook v-model:open="bookOpen" />
    </div>
  </section>
</template>

<style scoped>
.tabs-scroll { margin-bottom: 30px; overflow-x: auto; scrollbar-width: none; }
.tabs-scroll::-webkit-scrollbar { display: none; }
.menu { columns: 2; column-gap: 64px; }
.group { break-inside: avoid; margin: 0 0 36px; animation: fadeIn .45s both; }
.group h3 {
  font-size: 1.9rem;
  text-transform: uppercase;
  line-height: 1;
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}
.group h3::after { content: ""; flex: 1; height: 2px; background: var(--red); opacity: .85; transform: translateY(-6px); }
.sizes, .line { display: grid; grid-template-columns: 1fr auto; align-items: baseline; gap: 12px; }
.sizes { color: var(--muted); font-size: .78rem; letter-spacing: .06em; text-transform: uppercase; font-weight: 700; padding: 2px 0 4px; }
.line { padding: 7px 0; }
.n { display: flex; align-items: baseline; gap: 10px; min-width: 0; }
.n > span { flex: 0 1 auto; }
.n::after { content: ""; flex: 1; border-bottom: 1px dotted var(--line); transform: translateY(-4px); min-width: 12px; }
.line small { display: block; color: var(--muted); font-size: .8rem; line-height: 1.3; }
.pr { display: flex; gap: 14px; font-weight: 700; font-variant-numeric: tabular-nums; white-space: nowrap; }
.pr span { min-width: 4.6em; text-align: right; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.swap-enter-active, .swap-leave-active { transition: opacity .15s; }
.swap-enter-from, .swap-leave-to { opacity: 0; }

@media (max-width: 760px) {
  .menu { columns: 1; }
  .group h3 { font-size: 1.7rem; }
  .tabs-scroll {
    margin-inline: calc(-1 * var(--gutter-l)) calc(-1 * var(--gutter-r));
    padding-inline: var(--gutter-l) var(--gutter-r);
  }
}
@media (prefers-reduced-motion: reduce) { .group { animation: none; } }
</style>
