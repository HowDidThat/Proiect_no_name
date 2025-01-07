<script>
import {ref} from "vue";
import { getToken } from '../utils/backendCommunication';
import router from "../router/index";
export default{
  setup(){
    const username = ref("");
    const password = ref("");
    const invalid_credentials = ref(false);
    const handleSubmit = async() => {
     
      const response = await getToken(username.value,password.value);
      if (response == 401){
        invalid_credentials.value = true;
        console.log("Not ok");
      }
      else{
        console.log("ok");
        if ($cookies.get("access_token") == null)
          $cookies.remove("access_token")
        if ($cookies.get("refresh_token") == null)
          $cookies.remove("refresh_token")
        
        $cookies.set("access_token",response.data["access_token"],1800);
        $cookies.set("refresh_token",response.data["refresh_token"],365*24*3600);
        router.push('/account')
      }
    }
    return {
      username,
      password,
      handleSubmit,
      invalid_credentials
    }

  }
}

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
            v-model = "username"
            placeholder="Username"
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
            class="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            id="password"
            type="password"
            v-model = "password"
            placeholder="******************"
          />
        
          <div v-if="invalid_credentials">
          <p class="text-red-500 text-xs italic">Invalid username or password</p>
        </div>
        </div>

        <div class="flex items-center justify-between">
          <p></p>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click = "handleSubmit"
          >
            Sign In
          </button>
          <p></p>
          
            <a class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="/register">
                Create Account
            </a>
                
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
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>