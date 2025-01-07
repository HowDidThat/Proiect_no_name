<template>
  <div id="app">
    <NavbarTemplate/>
      <div>
      <router-view />
      </div>
  </div>
</template>

<script>

import NavbarTemplate from './components/NavbarTemplate.vue'

export default {
  name: 'App',
  components: {
    NavbarTemplate
  }
}
</script>


<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>