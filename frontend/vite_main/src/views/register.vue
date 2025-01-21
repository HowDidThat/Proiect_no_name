<script>
import { ref, computed, defineAsyncComponent, toRaw} from "vue";
import { validatePassword } from "../utils/formUtils";
import { createAccount } from "../utils/backendCommunication";
import router from "../router/index";
export default {
  setup() {
    const username = ref("");
    const email = ref("");
    const institution = ref("");
    const year_of_study = ref("");
    const password = ref("");
    const repeat_password = ref("");
    const problems = ref([]);
    
    const visibleProblems = computed(() => {
      const data = toRaw(problems.value);
      //console.log(data.slice(0,2))
      return data.slice(0, 2);
    });

    const numberProblems = computed(()=>{
      if (problems.value.length)
        return problems.value.length;
      return 0
    })

    const handleCreateAccount = () => {
      problems.value = [];
      if (username.value.length < 4)
        problems.value.push({
          message: "Please select a username longer than 4 characters"
        });
      if (email.value.length < 5)
        problems.value.push({
          message: "Not a valid email adress"
        });
      if (institution.value.length < 3)
        problems.value.push({
          message: "Please use at least 3 charactets for the institution name"
        });
      const password_problems = ref([]);
      password_problems.value = validatePassword(password.value, repeat_password.value);

      password_problems.value.forEach(p => {
        problems.value.push({ message: p });
      });
      
      if (problems.value.length == 0)
      {
        console.log("Duck");
        create_account();
      }

    };

    const create_account = async() =>{
        const response = await createAccount(
          username.value,
          email.value,
          password.value,
          institution.value,
          year_of_study.value
        )
        problems.value = toRaw(problems.value);
        if (response === "ok") {
        router.push('/login');
    } else {
        const server_complaints = response;
        console.log('Server Complaints:', server_complaints); // Add this to inspect complaints
        
        if (Array.isArray(server_complaints)) {
            server_complaints.forEach(element => {
                console.log(element);
            });
            problems.value.push(server_complaints);
        } else {
            console.warn('Server complaints are not an array:', server_complaints);
            problems.value.push({message : server_complaints});
        }
    }
    const clone = toRaw(problems.value);
      problems.value = clone;
      console.log(Array(problems.value))
      };

    return {
      username,
      email,
      institution,
      year_of_study,
      password,
      repeat_password,
      handleCreateAccount,
      problems,
      visibleProblems,
      create_account,
      numberProblems
    };
  },
};
</script>

<template>
  <div class="from-container">
    <div class="w-full max-w-xs">
      <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <div class="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="username"
          >
            Username
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="username"
            type="text"
            v-model="username"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
            Email
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="email"
            type="text"
            v-model="email"
          />
        </div>
        <div class="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="institution"
          >
            Institution
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="institution"
            type="text"
            v-model="institution"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="year">
            Year of study
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="year"
            type="text"
            placeholder="0 if not applicable"
            v-model="year_of_study"
          />
        </div>
        <div class="mb-6">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="password"
          >
            Password
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="password"
            type="password"
            v-model="password"
            placeholder="******************"
          />
        </div>
        <div class="mb-6">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="repeat_password"
          >
            Repeat Password
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="repeat_password"
            type="password"
            v-model="repeat_password"
            placeholder="******************"
          />
        </div>
        
        <!-- Display only first 2 problems -->
        <ul class="text-red-500 text-sm mb-4">
          <li v-for="({message}, index) in visibleProblems" :key="index">
            {{ message }}
          </li>
          <!-- Show indication if there are more problems -->
          <li v-if="numberProblems > 2" class="text-gray-500 italic">
            ...and {{ numberProblems - 2 }} more issues to fix
          </li>
        </ul>

        <div class="flex items-center justify-between">
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click="handleCreateAccount"
          >
            Create account
          </button>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
          >
            Sign In
          </button>
        </div>
      </form>
      <p class="text-center text-gray-500 text-xs">
        &copy;2024 HDT software. All rights reserved.
      </p>
    </div>
  </div>
</template>

<style scoped>
.from-container {
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>