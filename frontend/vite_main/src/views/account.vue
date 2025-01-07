<script setup>
import { getUserInfo } from '../utils/backendCommunication';
import { ref, onMounted } from 'vue'
import { checkToken } from '../utils/mop';
import router from '../router';
const response = ref(null);
const user_data = ref({});
const user_tests = ref({});
onMounted(async () => {
  const token = $cookies.get("access_token");
  const r_token = $cookies.get("refresh_token");
  console.log(token);
  console.log(r_token);
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
  user_data.value.tests_completed = 100;
  user_data.value.average_score = 55.8;

});

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
     </div>
    </div>
    </div>
    </template>

<style scoped>
.user_info{
  margin-left: auto;
  margin-right: auto;
  width: 100%;

}

</style>