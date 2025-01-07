<script setup>
  import {ref} from 'vue'
  const isOpen = ref(false)
</script>

<template>
  <nav class="bg-gray-800">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo/Brand -->
        <div class="flex-shrink-0">
          <span class="text-white text-xl font-bold">Logo</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:block">
          <div class="ml-10 flex items-baseline space-x-4">
            <a href="#" class="text-white px-3 py-2 rounded-md text-sm font-medium">Home</a>
            <a href="/register" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Register</a>
            <a href="/login" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Login</a>
            <a href="/account" class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">User</a>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button 
            @click="isOpen = !isOpen" 
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none"
          >
            <svg 
              class="h-6 w-6" 
              :class="{'hidden': isOpen, 'block': !isOpen }" 
              stroke="currentColor" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg 
              class="h-6 w-6" 
              :class="{'block': isOpen, 'hidden': !isOpen }" 
              stroke="currentColor" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div :class="{'block': isOpen, 'hidden': !isOpen}" class="md:hidden">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <a href="#" class="text-white block px-3 py-2 rounded-md text-base font-medium">Home</a>
        <a href="/register" class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Register</a>
        <a href="/login" class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium">Login</a>
        <a href="/account" class="text-gray-300 hover:text-white block px-3 py-2 rounded-md text-base font-medium">User</a>
      </div>
    </div>
  </nav>
</template>
<style scoped>

</style>