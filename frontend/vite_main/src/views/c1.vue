<template>
    <div>    
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { Modal } from 'bootstrap'
  
  // If you need to programmatically control the modal
  onMounted(() => {
    const modal = new Modal(document.getElementById('exampleModal'))
    // You can now use modal.show() or modal.hide()
  })
  </script>