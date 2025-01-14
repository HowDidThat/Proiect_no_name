<script setup>
import Navbar from './views/Navbar.vue';
</script>

<template>
  <Navbar/>
  <router-view/>
</template>

<style scoped>
.content_div{
  width: 100vw;
  height: 100vh;
}
</style>
