<template>
    <div class="container mx-auto px-4 py-8">
      <section 
        v-for="(item, index) in contentItems" 
        :key="index"
        class="flex flex-col md:flex-row items-center gap-8 py-12"
        :class="{ 'md:flex-row-reverse': index % 2 !== 0 }"
      >
        <div class="w-full md:w-1/2">
          <img 
            :src="`../assets/${item.imageName}`" 
            :alt="item.title"
            class="w-full rounded-lg shadow-lg"
          />
        </div>
        
        <div class="w-full md:w-1/2 space-y-4">
          <h2 class="text-3xl font-bold text-gray-800">{{ item.title }}</h2>
          <p class="text-lg text-black-600 leading-relaxed">{{ item.description }}</p>
         
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const contentItems = ref([
    {
      title: "Improve your skill",
      description: "",
      buttonText: "Explore Tours",
      imageWidth: 600,
      imageHeight: 400,
      imageName : "tests.webp"
    },
    {
      title: "Test your students",
      description: "",
      buttonText: "View Accommodations",
      imageWidth: 600,
      imageHeight: 400,
      imageName : "classroom.webp"
    },
    {
      title: "Challenge your friends",
      description: "",
      buttonText: "Meet Our Team",
      imageWidth: 600,
      imageHeight: 400,
      imageName : "tropy.webp"
    }
  ])
  </script>
