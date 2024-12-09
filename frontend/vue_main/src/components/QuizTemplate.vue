<template>
  <div>
    <section
      class="vh-100 px-4 py-5 gradient-custom"
      style="border-radius: 0.5rem 0.5rem 0 0"
    >

    <div v-if ="creating_quiz" class="quiz_creation_part">
    <form @submit.prevent="createQuiz" class="challenge-form">
      <div class="form-group">
        <label for="name">Quiz name:</label>
        <input 
          type="text" 
          id="name" 
          v-model="quiz_info.name" 
          required 
          placeholder="Enter quiz info"
        >
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea 
          id="description" 
          v-model="quiz_info.description" 
          required 
          placeholder="Describe the usage of the quiz"
          rows="4"
        ></textarea>
      </div>

      <div class="form-group">
        <label>Quiz type:</label>
        <div class="difficulty-options">
          <label>
            <input 
              type="radio" 
              v-model="quiz_info.type" 
              value="std" 
            >Symptom -> Disease
          </label>
          <label>
            <input 
              type="radio" 
              v-model="quiz_info.type" 
              value="dts"
            >Disease -> Symptom
          </label>
        </div>
      </div>

      <div class="form-group">
        <label>Difficulty:</label>
        <div class="difficulty-options">
          <label>
            <input 
              type="radio" 
              v-model="quiz_info.difficulty" 
              value="easy" 
            > Easy
          </label>
          <label>
            <input 
              type="radio" 
              v-model="quiz_info.difficulty" 
              value="medium"
            > Medium
          </label>
          <label>
            <input 
              type="radio" 
              v-model="quiz_info.difficulty" 
              value="hard"
            > Hard
          </label>
        </div>
      </div>

      <button type="submit" class="submit-btn">Create Challenge</button>
    </form>
    </div>
    <div v-if = "!creating_quiz" class="quiz_part">
      <div class="row d-flex justify-content-center">
        <div class="col col-md-9 col-lg-7 col-xl-6">
          <div class="card" style="border-radius: 15px">
            <div class="card-body p-5">
            <p class="question-info border-bottom pb-3">{{ questions[currentQuestion].text }}</p>
              <div class="d-flex">
                <div class="flex-shrink-0 border-bottom pb-3">
                  <div class="symptoms column">
                    <div class="column-name">Symptoms</div>
                    <div
                      v-for="(symptom, index) in questions[currentQuestion].symptoms" :key="index"
                    >
                      {{ symptom }}
                    </div>
                  </div>
                  <div class="diseases column">
                    <div class="column-name">Diseases</div>
                    <div
                      v-for="(disease, index) in questions[currentQuestion]
                        .diseases"
                      :key="index"
                      class="d-flex justify-content-between align-items-center mb-2"
                    >
                      <span>{{ disease }}</span>
                      <template
                        v-if="
                          !questions[currentQuestion].answer.includes(disease)
                        "
                      >
                        <button
                          class="btn btn-primary ms-2"
                          v-on:click="addMatch(disease)"
                        >
                          Match
                        </button>
                      </template>
                      <template v-else>
                        <button
                          class="btn btn-primary ms-2"
                          v-on:click="addMatch(disease)"
                        >
                          Unmatch
                        </button>
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
              <div class="d-flex navigation-buttons">
              <button
                class="btn btn-primary arrows"
                data-toggle="modal"
                data-target="#exampleModal"
              >
                Submit
              </button>
              </div>
              <br />
              <br />
            </div>
          </div>
        </div>
      </div>
    </div>
    </section>
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">You sure?</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">Submitting the quiz.</div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-primary"
              data-dismiss="modal"
              v-on:click="submitQuiz()"
            >
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import "@/css/quiz.css";
import { sendQuizData } from "@/utils/backendCommunication";
import { getQuizInfo } from "@/utils/backendCommunication";
export default {
  name: "QuizTemplate",
  data() {
    return {
      creating_quiz : true,
      quiz_info:{
        name:"",
        description:"",
        type:"",
        difficulty:""
      },
      questions: [
        {
          text:"This is a test for the question field",
          symptoms: ["Disentery", "Cancer", "Explosive t", "Melenoma"],
          diseases: ["Disease A", "Covid", "Red nose"],
          answer: [],
        },
        {
          text:"This is a test for the question field two",  
          symptoms: ["D 2", "Thing 2", "Q2"],
          diseases: [
            "Disease A",
            "Covid",
            "Red nose",
            "thing2",
            "thing3",
            "thing4    ",
          ],
          answer: [],
        },
      ],
      currentQuestion: 0,
      numberQuestions: 2,
    };
  },
  async mounted(){
    try {
    let partial = await getQuizInfo(this.$cookie.get("access_token"));
    console.log(partial.data);

  } catch (error) {
    console.error("Error fetching user data:", error);    
    //this.$router.push({ path: 'login' });
  }
  },
  methods: {
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
      this.updateQuestionInfo();
    },
    updateQuestionInfo() {
      this.currentQuestionDetails = this.questions[this.currentQuestion];
      console.log(this.currentQuestion);
    },
    addMatch(disease) {
      const currentQuestion = this.questions[this.currentQuestion];
      if (currentQuestion.answer.includes(disease)) {
        currentQuestion.answer = currentQuestion.answer.filter(
          (item) => item !== disease
        );
      } else {
        currentQuestion.answer.push(disease);
      }
    },
    submitQuiz() {
      const token = this.$cookie.get("token");
      sendQuizData(token, this.questions);
      this.$router.push({ path: "profile" });
    },
    createQuiz(){
      console.log(this.quiz_info);
      this.creating_quiz = false;
      


    }
  },
};
</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(to right, #ee7724, #d8363a, #dd3675, #b44593);
}

.question-card {
  width: 800px;
  height: 400px;
  margin: auto;

  background-color: white;
  border-radius: 5%;
}

.navigation-buttons {
  align-items: center;
  justify-content: center;
  display: flex;
  margin-top:10px;
}
.arrows {
  margin-left: 10px;
  margin-right: 10px;
}

.card {
  background: white;
}

.flex-shrink-0 {
  width: 100%;
  display: flex;
}
.column {
  width: 50%;
}

.buttons-card {
  width: 100%;

  border-radius: 20px;
}
.question-info{
    font-size: 20px;
    border-bottom:2cm;
}

.column-name{
  font-size: x-large;
  margin-bottom:2ch;
}

</style>
