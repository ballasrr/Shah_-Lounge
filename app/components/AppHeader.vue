<script setup lang="ts">
const open = ref(false)
const links = [
  { to: '#menu', label: 'Меню' },
  { to: '#zones', label: 'Атмосфера' },
  { to: '#book', label: 'Бронь' },
  { to: '#contacts', label: 'Контакты' }
]
</script>

<template>
  <header class="top" :class="{ open }">
    <div class="wrap bar">
      <a class="logo" href="#top" aria-label="Шах Lounge — на главную">
        <LogoWide />
      </a>
      <nav class="links" aria-label="Разделы">
        <a v-for="l in links" :key="l.to" :href="l.to" @click="open = false">{{ l.label }}</a>
      </nav>
      <UButton to="#book" class="book-btn" label="Забронировать" />
      <button
        class="burger"
        type="button"
        :aria-expanded="open"
        :aria-label="open ? 'Закрыть меню разделов' : 'Открыть меню разделов'"
        @click="open = !open"
      >
        <i />
      </button>
    </div>
  </header>
</template>

<style scoped>
.top {
  position: sticky;
  top: env(safe-area-inset-top, 0px);
  z-index: 20;
  background: rgba(19, 15, 17, .84);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
}
.bar { display: flex; align-items: center; gap: 24px; padding-block: 12px; }
.logo { display: flex; align-items: center; }
.logo :deep(svg) { height: 34px; width: auto; display: block; }
.links { display: flex; gap: 24px; margin-left: auto; }
.links a { text-decoration: none; color: var(--muted); font-size: .92rem; font-weight: 500; transition: color .2s; }
.links a:hover { color: var(--fg); }

.burger {
  display: none;
  margin-left: auto;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: transparent;
  color: var(--fg);
  cursor: pointer;
  align-items: center;
  justify-content: center;
}
.burger i, .burger i::before, .burger i::after {
  display: block;
  width: 18px;
  height: 2px;
  background: currentColor;
  border-radius: 2px;
  position: relative;
  transition: transform .25s, background .25s;
}
.burger i::before, .burger i::after { content: ""; position: absolute; left: 0; }
.burger i::before { top: -6px; }
.burger i::after { top: 6px; }
.open .burger i { background: transparent; }
.open .burger i::before { transform: translateY(6px) rotate(45deg); }
.open .burger i::after { transform: translateY(-6px) rotate(-45deg); }

@media (max-width: 760px) {
  .bar { gap: 12px; }
  .burger { display: inline-flex; }
  .book-btn { display: none; }
  .links {
    position: absolute;
    left: 0;
    right: 0;
    top: 100%;
    flex-direction: column;
    gap: 0;
    margin: 0;
    background: var(--ink);
    border-bottom: 1px solid var(--line);
    padding: 6px var(--gutter-r) 14px var(--gutter-l);
    clip-path: inset(0 0 100% 0);
    visibility: hidden;
    transition: clip-path .3s cubic-bezier(.2, .7, .2, 1), visibility .3s;
  }
  .open .links { clip-path: inset(0 0 0 0); visibility: visible; }
  .links a {
    font-family: var(--display);
    font-weight: 700;
    font-size: 1.9rem;
    text-transform: uppercase;
    color: var(--fg);
    padding: 10px 0;
    border-bottom: 1px solid var(--line);
  }
  .links a:last-child { border-bottom: 0; }
}
</style>
