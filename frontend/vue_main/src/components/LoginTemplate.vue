<template>
    <div>
        <section class="vh-100 gradient-custom">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card bg-dark text-white" style="border-radius: 1rem;">
          <div class="card-body p-5 text-center">
          
            <div class="mb-md-5 mt-md-4 pb-5">

              <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
              <form @submit.prevent = handleSubmit>
              <div data-mdb-input-init class="form-outline form-white mb-4">
                <label class="form-label" for="typeTextX">Email</label>
                <input type="text" id="typeTextX" class="form-control form-control-lg" v-model="formData.email"/>
              </div>

              <div data-mdb-input-init class="form-outline form-white mb-4">
                <label class="form-label" for="typePasswordX">Password</label>
                <input type="password" id="typePasswordX" class="form-control form-control-lg" v-model="formData.password"/>
              </div>
              <div class="errors" v-if="invalidLoginInfo">
                Wrong email or password
              </div>
              <br> 
              <button data-mdb-button-init data-mdb-ripple-init class="btn btn-outline-light btn-lg px-5" type="submit">Login</button>
              
              </form>
              
              <br>
              <br>
              <p class="small mb-5 pb-lg-2"><a class="text-white-50" href="#!">Forgot password?</a></p>
            </div>

            <div>
              <p class="mb-0">Don't have an account? <a href="/register" class="text-white-50 fw-bold">Sign Up</a>
              </p>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</section>
    </div>
</template>

<script>

import { getToken } from '@/utils/backendCommunication';
export default {
    name: "LoginTemplate",
    data() {
      return {
        formData:{
          email:"",
          password: ""
        },
        invalidLoginInfo: false
      }
    },
    methods:{
      async handleSubmit(){
        let t = await getToken(this.formData.email,this.formData.password)
        if (t == 401)
        {
          this.invalidLoginInfo = true
        }
        else
        {
          this.set_cookies(t.data.access_token,t.data.refresh_token);
          this.$router.push({ path: 'profile' });          
        }

      },
      set_cookies(at,rt){
        this.$cookie.set('access_token',at,1);
        this.$cookie.set('refresh_token',rt,30);
      },
      login(){
        let acces_token = this.$cookie.get('acces_token')
        let refresh_token = this.$cookie.get('refresh_token')
        if (acces_token !== null && refresh_token !== null)
          this.$router.push({ path: 'profile' })
      }
    },
    beforeMount() {
      this.login()
    },

  }

</script>

  
<style scoped>
.gradient-custom {
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}
</style>
