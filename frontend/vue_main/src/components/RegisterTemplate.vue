<template>
  <div>
    <section class="vh-100 gradient-custom">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-12 col-md-8 col-lg-6 col-xl-5">
            <div class="card bg-dark text-white" style="border-radius: 1rem;">
              <div class="card-body p-5 text-center">
              <form @submit.prevent = handleSubmit>  
                <div class="mb-md-5 mt-md-4 pb-5">

                  <h2 class="fw-bold mb-2 text-uppercase">Register</h2>
                  <p class="text-white-50 mb-5">Create your account</p>

                  <div data-mdb-input-init class="form-outline form-white mb-4">
                    <label class="form-label" for="typeName">Full Name</label>
                    <input type="text" id="typeName" class="form-control form-control-lg" v-model="formData.name"/>
                  </div>

                  <div data-mdb-input-init class="form-outline form-white mb-4">
                    <label class="form-label" for="typeEmailX">Email</label>
                    <input type="email" id="typeEmailX" class="form-control form-control-lg" v-model="formData.email"/>
                  </div>

                  <div data-mdb-input-init class="form-outline form-white mb-4">
                    <label class="form-label" for="typePasswordX">Password</label>
                    <input type="password" id="typePasswordX" class="form-control form-control-lg" v-model="formData.password"/>
                  </div>
                  <div data-mdb-input-init class="form-outline form-white mb-4">
                    <label class="form-label" for="typeConfirmPasswordX">Confirm Password</label>
                    <input type="password" id="typeConfirmPasswordX" class="form-control form-control-lg" v-model="formData.confirmPassword"/>
                  </div>
                  
                  <div class="errors" v-for="problem in problems" :key="problem">
                    {{ problem }}
                  </div>

                  <br>
                  <button data-mdb-button-init data-mdb-ripple-init class="btn btn-outline-light btn-lg px-5" type="submit">
                    Register
                  </button>

                  <div class="d-flex justify-content-center text-center mt-4 pt-1">
                    <a href="#!" class="text-white"><i class="fab fa-facebook-f fa-lg"></i></a>
                    <a href="#!" class="text-white"><i class="fab fa-twitter fa-lg mx-4 px-2"></i></a>
                    <a href="#!" class="text-white"><i class="fab fa-google fa-lg"></i></a>
                  </div>
                </div>
              </form>
                <div>
                  <p class="mb-0">Already have an account? 
                    <a href="/login" class="text-white-50 fw-bold">Sign In</a>
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
import { validatePassword } from '@/utils/formUtils'
import { createAccount } from '@/utils/backendCommunication';
export default {
  name: "RegisterTemplate",
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      problems:[],
      formRespose:null
    }
  },
  methods: {
  async handleSubmit() {
    this.problems = validatePassword(this.formData.password, this.formData.confirmPassword);
    if (this.problems.length === 0) {
      try {
        this.formResponse = await createAccount(this.formData);
        console.log(this.formResponse.message);
        if (this.formResponse.message == "Registration successful")
          this.$router.push({ path: 'login' });
        else
          this.problems=this.formResponse.message;

      } catch (error) {
        console.error('Account creation failed', error);
      }
    }
  },
}


}

</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}

.errors {
  color:#d8363a;
  font-size: 14px;
}
</style>