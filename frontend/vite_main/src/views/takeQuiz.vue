<template>
  <div class="quiz-container">
    <div class="w-full max-w-2xl">
      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="flex justify-between mb-6">
          <h2 class="text-xl font-bold">Question {{ currentIndex + 1 }} of {{ questions.length }}</h2>
          <div class="text-sm text-gray-600">Time: {{ timer }}</div>
        </div>

        <!-- Symptoms Display -->
        <div class="mb-6">
          <h3 class="text-gray-700 font-bold mb-2">Symptoms:</h3>
          <div class="bg-gray-50 p-3 rounded">
            <span v-for="symptom in currentQuestion?.symptoms" 
                  :key="symptom"
                  class="inline-block bg-blue-100 rounded px-3 py-1 m-1">
              {{ symptom }}
            </span>
          </div>
        </div>

        <!-- Disease Selection -->
        <div class="mb-6">
          <h3 class="text-gray-700 font-bold mb-2">Select Diseases:</h3>
          <div class="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto">
            <div v-for="disease in diseases" 
                 :key="disease"
                 class="flex items-center">
              <input type="checkbox"
                     :id="disease"
                     :value="disease"
                     v-model="selectedDiseases"
                     class="mr-2">
              <label :for="disease">{{ disease }}</label>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex items-center justify-between mt-6">
          <button @click="previousQuestion"
                  :disabled="currentIndex === 0"
                  class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Previous
          </button>
          <button v-if="currentIndex < questions.length - 1"
                  @click="nextQuestion"
                  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Next
          </button>
          <button v-else
                  @click="submitAnswers"
                  class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import router from '../router'

export default {
  setup() {
    const questions = ref([])
    const currentIndex = ref(0)
    const selectedDiseases = ref([])
    const timer = ref('00:00')
    const answers = ref([])
    const route = useRoute()
    const quizId = ref(route.params.id)
    const currentQuestion = computed(() => 
      questions.value[currentIndex.value]
    )

    onMounted(async () => {
      try {
        const response = await fetch(`/api/questions/${quizId.value}`)
        questions.value = await response.json()
        startTimer()
      } catch (error) {
        console.error('Failed to fetch questions:', error)
      }
    })

    const startTimer = () => {
      let seconds = 0
      setInterval(() => {
        seconds++
        const minutes = Math.floor(seconds / 60)
        const remainingSeconds = seconds % 60
        timer.value = `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`
      }, 1000)
    }

    const previousQuestion = () => {
      if (currentIndex.value > 0) {
        saveCurrentAnswer()
        currentIndex.value--
        loadSavedAnswer()
      }
    }

    const nextQuestion = () => {
      if (currentIndex.value < questions.value.length - 1) {
        saveCurrentAnswer()
        currentIndex.value++
        loadSavedAnswer()
      }
    }

    const saveCurrentAnswer = () => {
      answers.value[currentIndex.value] = [...selectedDiseases.value]
    }

    const loadSavedAnswer = () => {
      selectedDiseases.value = answers.value[currentIndex.value] || []
    }

    const submitAnswers = async () => {
      saveCurrentAnswer()
      try {
        // Replace with your API endpoint
        await fetch('/api/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(answers.value)
        })
        router.push('/results')
      } catch (error) {
        console.error('Failed to submit answers:', error)
      }
    }

    return {
      questions,
      currentIndex,
      currentQuestion,
      selectedDiseases,
      timer,
      previousQuestion,
      nextQuestion,
      submitAnswers
    }
  }
}
</script>

<style scoped>
.quiz-container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f3f4f6;
}
</style>