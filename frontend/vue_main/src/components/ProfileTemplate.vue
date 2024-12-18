<template>
<div>
<section class="px-4 py-5 gradient-custom" style=" border-radius: .5rem .5rem 0 0;">
    <div class="row d-flex justify-content-center">
      <div class="col col-md-9 col-lg-7 col-xl-6">
        <div class="card" style="border-radius: 15px;">
          <div class="card-body p-4">
            <div class="d-flex">
              <div class="flex-shrink-0">
                <img src="../assets/BG.jpg" alt="Generic placeholder image" class="img-fluid" style="width: 180px; border-radius: 10px;">
              </div>
              <div class="flex-grow-1 ms-3">
                
                <h5 class="mb-1">
                  <template v-if="editing">
                    <input type="text" class="form-control" v-model="userData.name">
                  </template>
                  <template v-else>
                    {{ userData.name }}
                  </template>
                </h5>

                <p class="mb-2 pb-1">
                  <template v-if="editing">
                    <input type="text" class="form-control" v-model="userData.description">
                  </template>
                  <template v-else>
                    {{ userData.description }}
                  </template>
                </p>
                <p class="mb-2 pb-1">
                  <template v-if="editing">
                    <input type="email" class="form-control" v-model="userData.email">
                  </template>
                  <template v-else>
                    {{ userData.email }}
                  </template>
                </p>
                <template v-if="editing">
                  <button class="btn btn-primary" @click="startEditing">Save</button>
                  </template>
                  <template v-else>
                    <button class="btn btn-primary" @click="startEditing">Edit</button>
                </template>

                <button class="btn btn-primary" style="margin-left: 20px;" @click="logOut">Log out</button>
                <div class="d-flex justify-content-start rounded-3 p-2 mb-2 bg-body-tertiary">
                  <div>
                    <p class="small text-muted mb-1">Quizes completed</p>
                    <p class="mb-0">{{ userData.testTaken }}</p>
                  </div>
                  <div class="px-3">
                    <p class="small text-muted mb-1">Average quiz points</p>
                    <p class="mb-0">{{ userData.averageTestScore}}</p>
                  </div>
                  <div>
                    <p class="small text-muted mb-1">Favorite quiz type</p>
                    <p class="mb-0">{{ userData.favoriteQuizType }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <br>
        <br>
        <div class="card">
            <div class="row quiz-info-row">
              <div class="col-3">Id</div>
              <div class="col-3">Title</div>
              <div class="col-3">Description</div>
              <div class="col-3"></div>
            </div>
            <div v-for="(quiz,index) in quizIds" :key="index">
              <div class="row quiz-info-row">
              <div class="col-3">{{ quiz.id }}</div>
              <div class="col-3">{{ quiz.title }}</div>
              <div class="col-3">{{ quiz.description }}</div>
              <div class="col-3">
                <!--<button @click="showQuizInfo(quiz.id)">Info</button>-->
              </div>
            </div>
          </div>
        </div>

        <br>
        <br>
        <template v-if="questions">
        <div class="card" style="border-radius: 15px">
        <div class="card-body p-5">
            <p class="question-info border-bottom pb-3">{{ questions[currentQuestion].text }}</p>
              <div class="d-flex">
                <div class="flex-shrink-0 question-card border-bottom pb-3">
                  <div class="symptoms column">
                    <div class="table-head">Symptoms</div>
                    <br>
                    <div v-for="(symptom, index) in questions[currentQuestion].symptoms" :key="index">
                      {{ symptom }}
                    </div>
                  </div>
                  <div class="diseases column">
                    <div class="table-head">Diseases</div>
                    <br>
                    <div
                      v-for="(disease, index) in questions[currentQuestion].diseases" :key="index"
                      class="d-flex justify-content-between align-items-center mb-2"
                    >
                      <template v-if="questions[currentQuestion].correct.includes(disease)">
                        <b class="disease correct">{{ disease }}</b>
                      </template>
                      <template v-else>
                        <div class="disease wrong">{{ disease }}</div>
                      </template>

                      <template
                        v-if="questions[currentQuestion].answer.includes(disease)">
                        <div >
                          <img class="checkbox" src="../assets/Checkmark.png" alt="Italian Trulli">
                        </div>
                      </template>
                      <template v-else>
                        <div >
                          <img class="checkbox" src="../assets/Checkbox.png" alt="Italian Trulli">
                        </div>  
                      </template>
                        
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="buttons-card">
              <div class="d-flex navigation-buttons">
                <button
                  class="btn btn-primary arrows"
                  v-on:click="choseQuestion(0)"
                >
                  &#60;&#60;
                </button>
                <button
                  class="btn btn-primary arrows"
                  v-on:click="choseQuestion(-2)"
                >
                  &#60;
                </button>
                <button
                  class="btn btn-primary arrows"
                  v-on:click="choseQuestion(-1)"
                >
                  &#62;
                </button>
                <button
                  class="btn btn-primary arrows"
                  v-on:click="choseQuestion(20)"
                >
                  &#62;&#62;
                </button>
              </div>
              <br />
              <br />
            </div>
            </div>

        </template>
      </div>
    </div>
  </section>
</div>
</template>

<script>

import { getUserInfo } from '@/utils/backendCommunication';
import { updateUserInfo } from '@/utils/backendCommunication'
import { getQuizInfo } from "@/utils/backendCommunication";
import { checkToken } from '@/utils/mop';

export default {
  name: 'ProfileTemplate',
  data(){
    return {
    userData: 
    {
      name: "Carol Smith",
      email: "carol.smt@hot.com",
      description: "Teacher at 'University of Lodon'.",
      testTaken: "101",
      picture:"/home/doom/Documents/GitHub/Symptom_Disease_Quiz_Application_for_Cardiology_Students_using_AI/frontend/vue_main/src/assets/BG.jpg",
      averageTestScore: 97.6,
      favoriteQuizType:"Classic",
    },
    editing: false,
    currentPage: 0,
    quizIds: null,
    quizData: null,
    questions: null,
    currentQuestion: 0,
    numberQuestions:2
    }  
  },
  methods:{
    startEditing(){
      this.editing = !this.editing
      updateUserInfo(this.userData)
    },
    logOut(){
      this.$cookie.set('token',"None",-1)
      this.$router.push({ path: 'login' })
    },
    showQuizInfo(quizId){
      //this.questions = getCompletedQuizData(quizId)
      console.log(this.questions)
      console.log(quizId)
      
    },
    choseQuestion(value) {
      switch (value) {
        case -1:
          this.currentQuestion = Math.min(
            this.currentQuestion + 1,
            this.numberQuestions - 1
          );
          break;
        case -2:
          this.currentQuestion = Math.max(this.currentQuestion - 1, 0);
          break;
        default:
          this.currentQuestion = Math.min(
            this.numberQuestions - 1,
            Math.max(0, value)
          );
      }

    },
    async setUserInfo(){
      let partial = await getUserInfo(this.$cookie.get("access_token"));
        console.log(partial.data);
        this.userData.name = partial.data.username
        this.userData.email = partial.data.email
        this.userData.description = "University: "+ partial.data.institution+ ", Year of study: " + partial.data.year_of_study
    },
    async setQuizInfo(){
      let partial = await getQuizInfo(this.$cookie.get("access_token"));
      this.quizIds = partial.data
    }
  
  },
  async mounted(){
    let tokenCheck = checkToken(this.$cookie.get("access_token"),this.$cookie.get("refresh_token"))
    if (tokenCheck["status"] === 200)
    {
      if (tokenCheck["new_token"] !== null)
        this.$cookie.set('access_token',tokenCheck["new_token"],1);
      this.setUserInfo()
      
    }
    else{
      this.$cookie.set("access_token", null, -1);
      this.$cookie.set("refresh_token", null, -1);
      this.$router.push({ path: 'login' });
    }

    },
   beforeMount() {
  
},
}
</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
  min-height: 100vh;
}

.quiz-info-row{
  text-align: center;
}
.column {
  width: 50%;
}
.question-card {
  width: 100%;
  display: flex;
}
.table-head{
  font-size:20px;
}

.buttons-card {
  width: 100%;
  
  border-radius: 20px;
}

.navigation-buttons {
  align-items: center;
  justify-content: center;
  display: flex;
}
.arrows {
  margin-left: 10px;
  margin-right: 10px;
}
.checkbox{
  height: 20px;
}

</style>