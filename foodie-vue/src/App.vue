<script setup lang="ts">
// Dark mode by default — matches our design system
document.documentElement.classList.add('dark')
</script>

<template>
  <router-view />
</template>

<style>
#app {
  min-height: 100vh;
}
</style>
