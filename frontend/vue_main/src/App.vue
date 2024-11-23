<template>
  <div id="app">
    <NavbarTemplate/>
    <div class="cie-wrapper">
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

</style>
