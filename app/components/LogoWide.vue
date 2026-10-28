<script setup lang="ts">
import { wideViewBox, widePaths } from '~/data/logo'
</script>

<template>
  <svg :viewBox="wideViewBox" aria-hidden="true">
    <path v-for="(p, i) in widePaths" :key="i" :d="p.d" :fill-rule="p.rule" fill="#e3000f" />
  </svg>
</template>
