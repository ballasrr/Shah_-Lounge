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
  <header class="sticky top-[env(safe-area-inset-top,0px)] z-20 border-b border-line bg-ink/84 backdrop-blur-[10px]">
    <div class="shell flex items-center gap-6 py-3 phone:gap-3">
      <a class="flex items-center [&_svg]:block [&_svg]:h-[34px] [&_svg]:w-auto" href="#top" aria-label="Шах Lounge — на главную">
        <LogoWide />
      </a>
      <nav
        class="ml-auto flex gap-6 phone:absolute phone:inset-x-0 phone:top-full phone:m-0 phone:flex-col phone:gap-0 phone:border-b phone:border-line phone:bg-ink phone:pt-1.5 phone:pr-(--gutter-r) phone:pb-3.5 phone:pl-(--gutter-l) phone:transition-[clip-path,visibility] phone:duration-300 phone:ease-[cubic-bezier(.2,.7,.2,1)]"
        :class="open ? 'phone:[clip-path:inset(0)] phone:visible' : 'phone:[clip-path:inset(0_0_100%_0)] phone:invisible'"
        aria-label="Разделы"
      >
        <a
          v-for="l in links"
          :key="l.to"
          :href="l.to"
          class="text-[.92rem] font-medium text-mist transition-colors duration-200 hover:text-cream phone:border-b phone:border-line phone:py-2.5 phone:font-display phone:text-[1.9rem] phone:font-bold phone:text-cream phone:uppercase phone:last:border-b-0"
          @click="open = false"
        >{{ l.label }}</a>
      </nav>
      <UButton to="#book" class="phone:hidden" label="Забронировать" />
      <button
        class="ml-auto hidden size-11 cursor-pointer items-center justify-center rounded-xl border border-line bg-transparent text-cream phone:inline-flex"
        type="button"
        :aria-expanded="open"
        :aria-label="open ? 'Закрыть меню разделов' : 'Открыть меню разделов'"
        @click="open = !open"
      >
        <i
          class="relative block h-0.5 w-[18px] rounded-sm bg-current transition-[background-color] duration-250 before:absolute before:top-[-6px] before:left-0 before:block before:h-0.5 before:w-[18px] before:rounded-sm before:bg-current before:transition-transform before:duration-250 before:content-[''] after:absolute after:top-1.5 after:left-0 after:block after:h-0.5 after:w-[18px] after:rounded-sm after:bg-current after:transition-transform after:duration-250 after:content-['']"
          :class="open ? 'bg-transparent before:translate-y-1.5 before:rotate-45 after:-translate-y-1.5 after:-rotate-45' : ''"
        />
      </button>
    </div>
  </header>
</template>
