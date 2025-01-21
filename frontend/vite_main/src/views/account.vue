<script setup>
import { getUserInfo } from '../utils/backendCommunication';
import { ref, onMounted ,computed} from 'vue'
import { checkToken } from '../utils/mop';
import { getUserTests } from '../utils/backendCommunication';
import router from '../router';
const response = ref(null);
const user_data = ref({});

const itemsPerPage = 6
const currentPage = ref(1)

const totalItems = ref(0) ;// computed(() => testResults.value.length)
const totalPages = ref(0) ;//computed(() => Math.ceil(totalItems.value / itemsPerPage))

const startIndex = ref(0) ;//computed(() => (currentPage.value - 1) * itemsPerPage)
const endIndex = ref(0) ;//computed(() => startIndex.value + itemsPerPage)
const testResults = ref([]);
const quizId = ref('');

onMounted(async () => {
  const token = $cookies.get("access_token");
  const r_token = $cookies.get("refresh_token");

  const mop_response = await checkToken(token,r_token);

  if (mop_response.status == 200 && mop_response.new_token !== null)
  {
    $cookies.set("access_token",response.data["access_token"],1800);
    console.log("Token refreshed");
  }
  else if (mop_response.status == 401){
    $cookies.remove("access_token");
    $cookies.remove("refresh_token");
    router.push("/login")
  }
  response.value = await(getUserInfo(token));
  user_data.value.email = response.value.data.email;
  user_data.value.username = response.value.data.username;
  user_data.value.institution = response.value.data.institution;
  user_data.value.year_of_study = response.value.data.year_of_study;
  user_data.value.tests_completed = 10;
  user_data.value.average_score = 0;

  let testVar = await getUserTests(token) 
  testResults.value = testVar.data.results;
  testResults.value.sort((a, b) => new Date(b.completed_at) - new Date(a.completed_at));

  totalItems.value = testResults.value.length;
  totalPages.value = Math.ceil(totalItems.value / itemsPerPage);
  startIndex.value = (currentPage.value - 1) * itemsPerPage;
  endIndex.value = startIndex.value + itemsPerPage;

  user_data.value.tests_completed = testResults.value.length
  
  let totalPoints = 0;
  testResults.value.forEach(element => {
    totalPoints = totalPoints + element.score;
  });
  if (user_data.value.tests_completed != 0)
    user_data.value.average_score = Number(totalPoints / user_data.value.tests_completed).toFixed(2)
});


const paginatedResults = computed(() => {
  return testResults.value.slice(startIndex.value, endIndex.value)
})

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    // Update indexes when page changes
    startIndex.value = (currentPage.value - 1) * itemsPerPage
    endIndex.value = startIndex.value + itemsPerPage
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    // Update indexes when page changes
    startIndex.value = (currentPage.value - 1) * itemsPerPage
    endIndex.value = startIndex.value + itemsPerPage
  }
}

const goToPage = (page) => {
  currentPage.value = page
  // Update indexes when page changes
  startIndex.value = (currentPage.value - 1) * itemsPerPage
  endIndex.value = startIndex.value + itemsPerPage
}

const displayedPages = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

const quizName = (name) =>{
  if (name != undefined)
    return name;
  return "Unnamed";
}

const toReadableDate = (oldDate) =>{
  const date = new Date(oldDate);
  return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }).format(date);
}

const logout = () =>{
  $cookies.set("access_token","",-1);
  $cookies.set("refresh_token","",-1);
  router.push("/login");
}

const goToQuiz = () => {
  if (quizId.value) {
    router.push(`/takeQuiz/${quizId.value}`)
  }
}

</script>

<template>
    <div class="">
    <div class="user_info max-w-4xl bg-white overflow-hidden shadow rounded-lg border">
     <div class="px-4 py-5 sm:px-6">
       <h3 class="text-lg leading-6 font-medium text-gray-900">
         User Profile
       </h3>
     </div>
     <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
       <div class="grid grid-cols-2 gap-4">
         <dl class="sm:divide-y sm:divide-gray-200">
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Username</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.username }}
             </dd>
           </div>
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Email</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.email }}
             </dd>
           </div>
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Institution</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.institution }}
             </dd>
           </div>
         </dl>
         <dl class="sm:divide-y sm:divide-gray-200">
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Year of Study</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.year_of_study }}
             </dd>
           </div>
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Tests Completed</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.tests_completed }}
             </dd>
           </div>
           <div class="py-3 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
             <dt class="text-sm font-medium text-gray-500">Average Score</dt>
             <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
               {{ user_data.average_score }}%
             </dd>
           </div>
         </dl>
        </div>
        <div class="flex gap-4 mt-4">
     <!-- Navigation button -->
     <router-link 
       to="/quiz" 
       class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors duration-200 shadow-sm"
     >
       Create quiz
     </router-link>

     <input
     v-model="quizId"
     type="number"
     class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
     placeholder="Enter quiz ID"
   />

   <!-- Dynamic navigation button -->
   <button
     @click="goToQuiz"
     class="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 transition-colors duration-200 shadow-sm"
   >
     Go to Quiz
   </button>

     <!-- Function button -->
     <button 
       @click="logout" 
       class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors duration-200 shadow-sm"
     >
       Log out
     </button>
   </div>
     </div>
    </div>
    </div>

    <div class="user_info max-w-4xl mt-8 bg-white shadow rounded-lg border">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Test Results
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Completed at
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Points
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="test in paginatedResults" :key="test">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ test.quiz_id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                Quiz {{ test.quiz_id }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ toReadableDate(test.completed_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ Number(test.score.toFixed(2)) }}
              </td>
            </tr>
          </tbody>
        </table>
  
        <div class="px-4 py-3 border-t border-gray-200 sm:px-6">
          <div class="flex items-center justify-between">
            <div class="flex-1 flex justify-between sm:hidden">
              <button 
                @click="previousPage" 
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
              >
                Previous
              </button>
              <button 
                @click="nextPage" 
                :disabled="currentPage >= totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                :class="{ 'opacity-50 cursor-not-allowed': currentPage >= totalPages }"
              >
                Next
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Showing
                  <span class="font-medium">{{ startIndex + 1 }}</span>
                  to
                  <span class="font-medium">{{ Math.min(endIndex, totalItems) }}</span>
                  of
                  <span class="font-medium">{{ totalItems }}</span>
                  results
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button
                    @click="previousPage"
                    :disabled="currentPage === 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                    :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
                  >
                    <span class="sr-only">Previous</span>
                    ←
                  </button>
                  <button
                    v-for="page in displayedPages"
                    :key="page"
                    @click="goToPage(page)"
                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium"
                    :class="page === currentPage ? 'bg-blue-50 border-blue-500 text-blue-600 z-10' : 'text-gray-500 hover:bg-gray-50'"
                  >
                    {{ page }}
                  </button>
                  <button
                    @click="nextPage"
                    :disabled="currentPage >= totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                    :class="{ 'opacity-50 cursor-not-allowed': currentPage >= totalPages }"
                  >
                    <span class="sr-only">Next</span>
                    →
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

</template>

<style scoped>
.user_info{
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  margin-top: 20px;
}

</style>