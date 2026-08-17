<template>
  <router-view />
</template>

<script setup lang="ts">
</script>

<style>
:root {
  --primary-color: #0077B6;
  --primary-light: #00C9D1;
  --text-primary: #1a1a1a;
  --text-secondary: #666;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: var(--text-primary);
  background: #f5f7fa;
}

#app {
  min-height: 100vh;
}
</style>
