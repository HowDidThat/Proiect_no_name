<script>
import { defineComponent, onMounted, ref, computed } from "vue";
import { getAllDeseases, getAllSymptoms } from "../utils/backendCommunication";
import { crq } from "../utils/backendCommunication";
const quiz_type = ref("Random")
const random_quiz = ref(true)
const title = ref("")
const description = ref("")
const difficulty = ref("")
const diseases = ref({
  "Drug Reaction": "Drug Reaction",
  "Hepatitis B": "Hepatitis B",
  "Chronic cholestasis": "Chronic Cholestasis",
  "Dengue": "Dengue",
  "AIDS": "AIDS",
  "Hypothyroidism": "Hypothyroidism",
  "GERD": "GERD",
  "Hepatitis A": "Hepatitis A",
  "Varicose veins": "Varicose Veins",
  "Osteoarthritis": "Osteoarthritis",
  "Urinary tract infection": "Urinary Tract Infection",
  "Pneumonia": "Pneumonia",
  "Hepatitis C": "Hepatitis C",
  "Common Cold": "Common Cold",
  "Heart attack": "Heart Attack",
  "Dimorphic hemorrhoids (piles)": "Dimorphic Hemorrhoids (Piles)",
  "Migraine": "Migraine",
  "Tuberculosis": "Tuberculosis",
  "Peptic ulcer disease": "Peptic Ulcer Disease",
  "Typhoid": "Typhoid",
  "Chicken pox": "Chicken Pox",
  "Acne": "Acne",
  "Fungal infection": "Fungal Infection",
  "Hepatitis D": "Hepatitis D",
  "Alcoholic hepatitis": "Alcoholic Hepatitis",
  "Bronchial Asthma": "Bronchial Asthma",
  "Hyperthyroidism": "Hyperthyroidism",
  "Gastroenteritis": "Gastroenteritis",
  "Malaria": "Malaria",
  "Cervical spondylosis": "Cervical Spondylosis",
  "Diabetes": "Diabetes",
  "Psoriasis": "Psoriasis",
  "Hepatitis E": "Hepatitis E",
  "Paralysis (brain hemorrhage)": "Paralysis (Brain Hemorrhage)",
  "Allergy": "Allergy",
  "(vertigo) Paroxysmal Positional Vertigo": "Vertigo (Paroxysmal Positional Vertigo)",
  "Impetigo": "Impetigo",
  "Hypertension": "Hypertension",
  "Arthritis": "Arthritis",
  "Jaundice": "Jaundice",
  "Hypoglycemia": "Hypoglycemia"
})
const symptoms = ref({
  "itching": "Itching",
  "skin_rash": "Skin Rash",
  "nodal_skin_eruptions": "Nodal Skin Eruptions",
  "continuous_sneezing": "Continuous Sneezing",
  "shivering": "Shivering",
  "chills": "Chills",
  "joint_pain": "Joint Pain",
  "stomach_pain": "Stomach Pain",
  "acidity": "Acidity",
  "ulcers_on_tongue": "Ulcers on Tongue",
  "muscle_wasting": "Muscle Wasting",
  "vomiting": "Vomiting",
  "burning_micturition": "Burning Micturition",
  "spotting_urination": "Spotting Urination",
  "fatigue": "Fatigue",
  "weight_gain": "Weight Gain",
  "anxiety": "Anxiety",
  "cold_hands_and_feets": "Cold Hands and Feet",
  "mood_swings": "Mood Swings",
  "weight_loss": "Weight Loss",
  "restlessness": "Restlessness",
  "lethargy": "Lethargy",
  "patches_in_throat": "Patches in Throat",
  "irregular_sugar_level": "Irregular Sugar Level",
  "cough": "Cough",
  "high_fever": "High Fever",
  "sunken_eyes": "Sunken Eyes",
  "breathlessness": "Breathlessness",
  "sweating": "Sweating",
  "dehydration": "Dehydration",
  "indigestion": "Indigestion",
  "headache": "Headache",
  "yellowish_skin": "Yellowish Skin",
  "dark_urine": "Dark Urine",
  "nausea": "Nausea",
  "loss_of_appetite": "Loss of Appetite",
  "pain_behind_the_eyes": "Pain Behind the Eyes",
  "back_pain": "Back Pain",
  "constipation": "Constipation",
  "abdominal_pain": "Abdominal Pain",
  "diarrhoea": "Diarrhoea",
  "mild_fever": "Mild Fever",
  "yellow_urine": "Yellow Urine",
  "yellowing_of_eyes": "Yellowing of Eyes",
  "acute_liver_failure": "Acute Liver Failure",
  "fluid_overload": "Fluid Overload",
  "swelling_of_stomach": "Swelling of Stomach",
  "swelled_lymph_nodes": "Swelled Lymph Nodes",
  "malaise": "Malaise",
  "blurred_and_distorted_vision": "Blurred and Distorted Vision",
  "phlegm": "Phlegm",
  "throat_irritation": "Throat Irritation",
  "redness_of_eyes": "Redness of Eyes",
  "sinus_pressure": "Sinus Pressure",
  "runny_nose": "Runny Nose",
  "congestion": "Congestion",
  "chest_pain": "Chest Pain",
  "weakness_in_limbs": "Weakness in Limbs",
  "fast_heart_rate": "Fast Heart Rate",
  "pain_during_bowel_movements": "Pain During Bowel Movements",
  "pain_in_anal_region": "Pain in Anal Region",
  "bloody_stool": "Bloody Stool",
  "irritation_in_anus": "Irritation in Anus",
  "neck_pain": "Neck Pain",
  "dizziness": "Dizziness",
  "cramps": "Cramps",
  "bruising": "Bruising",
  "obesity": "Obesity",
  "swollen_legs": "Swollen Legs",
  "swollen_blood_vessels": "Swollen Blood Vessels",
  "puffy_face_and_eyes": "Puffy Face and Eyes",
  "enlarged_thyroid": "Enlarged Thyroid",
  "brittle_nails": "Brittle Nails",
  "swollen_extremeties": "Swollen Extremities",
  "excessive_hunger": "Excessive Hunger",
  "extra_marital_contacts": "Extra-Marital Contacts",
  "drying_and_tingling_lips": "Drying and Tingling Lips",
  "slurred_speech": "Slurred Speech",
  "knee_pain": "Knee Pain",
  "hip_joint_pain": "Hip Joint Pain",
  "muscle_weakness": "Muscle Weakness",
  "stiff_neck": "Stiff Neck",
  "swelling_joints": "Swelling Joints",
  "movement_stiffness": "Movement Stiffness",
  "spinning_movements": "Spinning Movements",
  "loss_of_balance": "Loss of Balance",
  "unsteadiness": "Unsteadiness",
  "weakness_of_one_body_side": "Weakness of One Body Side",
  "loss_of_smell": "Loss of Smell",
  "bladder_discomfort": "Bladder Discomfort",
  "foul_smell_of_urine": "Foul Smell of Urine",
  "continuous_feel_of_urine": "Continuous Feel of Urine",
  "passage_of_gases": "Passage of Gases",
  "internal_itching": "Internal Itching",
  "toxic_look_(typhos)": "Toxic Look (Typhos)",
  "depression": "Depression",
  "irritability": "Irritability",
  "muscle_pain": "Muscle Pain",
  "altered_sensorium": "Altered Sensorium",
  "red_spots_over_body": "Red Spots Over Body",
  "belly_pain": "Belly Pain",
  "abnormal_menstruation": "Abnormal Menstruation",
  "dischromic_patches": "Dischromic Patches",
  "watering_from_eyes": "Watering from Eyes",
  "increased_appetite": "Increased Appetite",
  "polyuria": "Polyuria",
  "family_history": "Family History",
  "mucoid_sputum": "Mucoid Sputum",
  "rusty_sputum": "Rusty Sputum",
  "lack_of_concentration": "Lack of Concentration",
  "visual_disturbances": "Visual Disturbances",
  "receiving_blood_transfusion": "Receiving Blood Transfusion",
  "receiving_unsterile_injections": "Receiving Unsterile Injections",
  "coma": "Coma",
  "stomach_bleeding": "Stomach Bleeding",
  "distention_of_abdomen": "Distention of Abdomen",
  "history_of_alcohol_consumption": "History of Alcohol Consumption",
  "blood_in_sputum": "Blood in Sputum",
  "prominent_veins_on_calf": "Prominent Veins on Calf",
  "palpitations": "Palpitations",
  "painful_walking": "Painful Walking",
  "pus_filled_pimples": "Pus-Filled Pimples",
  "blackheads": "Blackheads",
  "scurring": "Scarring",
  "skin_peeling": "Skin Peeling",
  "silver_like_dusting": "Silver-like Dusting",
  "small_dents_in_nails": "Small Dents in Nails",
  "inflammatory_nails": "Inflammatory Nails",
  "blister": "Blister",
  "red_sore_around_nose": "Red Sore Around Nose",
  "yellow_crust_ooze": "Yellow Crust Ooze",
  "prognosis": "Prognosis"
})
const questions = ref([])
const currentQuestionIndex = ref(0)
const diseaseSearch = ref('')
const symptomSearch = ref('')
import router from '../router';
export default defineComponent({
  setup() {


    const changeQuiz = () => {
      random_quiz.value = !random_quiz.value;
      quiz_type.value = quiz_type.value === "Random" ? "Custom" : "Random";
    }

    const create_quiz = async() => {
      console.log(title.value);
      console.log(description.value);
      console.log(difficulty.value);
      const token = $cookies.get("access_token");
      const response = await(crq(token,title.value,description.value,difficulty.value));
      console.log(response.data.id);
      router.push("/takeQuiz/"+response.data.id);

    }



    const currentQuestion = computed(() =>
      questions.value[currentQuestionIndex.value] || null
    )

    const addNewQuestion = () => {
      questions.value.push({
        id: Date.now(),
        selectedSymptoms: []
      });
      currentQuestionIndex.value = questions.value.length - 1;
    }

    const addSymptomToQuestion = (symptom) => {
      if (!currentQuestion.value) return;
      if (!currentQuestion.value.selectedSymptoms.includes(symptom)) {
        currentQuestion.value.selectedSymptoms.push(symptom);
      }
    }

    const removeSymptomFromQuestion = (symptom) => {
      if (!currentQuestion.value) return;
      currentQuestion.value.selectedSymptoms = 
        currentQuestion.value.selectedSymptoms.filter(s => s !== symptom);
    }

    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
      }
    }

    const nextQuestion = () => {
      if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++;
      }
    }

    const submitQuestions = () => {
      console.log('Submitting questions:', questions.value);

    }

    const filteredDiseases = computed(() => {
  const entries = Object.entries(diseases.value)
  return Object.fromEntries(
    entries.filter(([key, value]) => 
      value.toLowerCase().includes(diseaseSearch.value.toLowerCase())
    )
  )
})

const filteredSymptoms = computed(() => {
  const entries = Object.entries(symptoms.value)
  return Object.fromEntries(
    entries.filter(([key, value]) => 
      value.toLowerCase().includes(symptomSearch.value.toLowerCase())
    )
  )
})



    return {
      title,
      description,
      difficulty,
      filteredDiseases,
      currentQuestion,
      quiz_type,
      filteredSymptoms,
      random_quiz,
      diseases,
      symptoms,
      create_quiz,
      changeQuiz,
      addNewQuestion,
      addSymptomToQuestion,
      removeSymptomFromQuestion,
      previousQuestion,
      nextQuestion,
      submitQuestions,
      questions,
      currentQuestionIndex,
      diseaseSearch,
      symptomSearch
    }
  },
});
</script>

<template>
<div class="main-container">
    <div class = "quiz_info">
        <p class="quiz-type"> {{ quiz_type }}</p>
        <button @click = "changeQuiz" type="button" class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:outline-none  dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">Change quiz type</button>
    </div>

    <div class = "quiz-creation-container">
        <div class="random-quiz" v-if="random_quiz">
    <div class="w-full max-w-xs">
        <form class="w-full max-w-lg bg-white p-6 rounded-lg shadow-md">
            <div class="flex flex-wrap -mx-3 mb-6">
                <div class="w-full px-3 mb-6 md:mb-0">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-first-name">
                        Title
                    </label>
                    <input v-model="title" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="grid-first-name" type="text">
                </div>
                <div class="w-full px-3">
                    <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-last-name">
                        Description
                    </label>
                    <textarea v-model="description" class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-last-name" rows="5"></textarea>
                </div>
            </div>
            <div class="w-full px-3 mb-6 md:mb-0">
                <br />
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-state">
                    Difficulty
                </label>
                <div class="relative">
                    <select v-model="difficulty" class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-state">
                        <option>Easy</option>
                        <option>Medium</option>
                        <option>Hard</option>
                    </select>
                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                        </svg>
                    </div>
                </div>
            </div>
            <br>
            <div class="flex justify-center">
                <button @click="create_quiz" type="button" class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:outline-none dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2">
                    Create quiz
                </button>
            </div>
        </form>
    </div>
</div>
        <div class="custom-quiz" v-if="!random_quiz">
            <div class="container mx-auto p-4">
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h1 class="text-2xl mb-4">Medical Questionnaire Builder</h1>
      
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div>
          <h2 class="text-lg mb-2">Diseases</h2>
          <input 
            v-model="diseaseSearch" 
            placeholder="Search diseases..." 
            class="w-full p-2 mb-2 border rounded"
          />
          <ul class="border p-2 rounded h-48 overflow-y-auto">
            <li v-for="(value, key) in filteredDiseases" 
                :key="key" 
                @click="addDiseaseToQuestion(key)"
                class="cursor-pointer hover:bg-gray-100 p-1">
                {{ value }}
            </li>
            </ul>
        </div>
        <div>
          <h2 class="text-lg mb-2">Symptoms</h2>
          <input 
            v-model="symptomSearch" 
            placeholder="Search symptoms..." 
            class="w-full p-2 mb-2 border rounded"
          />
          <ul class="border p-2 rounded h-48 overflow-y-auto">
            <li v-for="(value, key) in filteredSymptoms" 
                :key="key"
                @click="addSymptomToQuestion(key)"
                class="cursor-pointer hover:bg-gray-100 p-1">
                {{ value }}
            </li>
            </ul>
        </div>
      </div>


      <div class="mb-6">
        <div class="flex justify-between mb-4">
          <button @click="addNewQuestion" 
                  class="bg-blue-500 text-white px-4 py-2 rounded">
            Add New Question
          </button>
          <div>
            <button @click="previousQuestion" 
                    :disabled="currentQuestionIndex === 0"
                    class="bg-gray-500 text-white px-4 py-2 rounded mr-2">
              Previous
            </button>
            <button @click="nextQuestion" 
                    :disabled="currentQuestionIndex === questions.length - 1"
                    class="bg-gray-500 text-white px-4 py-2 rounded">
              Next
            </button>
          </div>
        </div>


        <div v-if="currentQuestion" class="border p-4 rounded bg-gray-50">
        <h3 class="text-lg mb-2">Question {{ currentQuestionIndex + 1 }}</h3>
        <div class="mb-4">
            <h4 class="mb-2">Selected Items:</h4>
            <div class="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto p-2">
                <span v-for="symptom in currentQuestion.selectedSymptoms"
                :key="symptom"
                class="bg-blue-100 px-2 py-1 rounded flex items-center justify-between">
            {{ symptoms[symptom] }}
            <button @click="removeSymptomFromQuestion(symptom)"
                    class="ml-2 text-red-500">×</button>
                </span>
            </div>
        </div>
        </div>
      </div>

      <button @click="submitQuestions" 
              :disabled="!questions.length"
              class="bg-green-500 text-white px-4 py-2 rounded">
        Submit Questions
      </button>
    </div>
  </div>
        </div>
    </div>  
</div>
</template>



<style scoped>
.toggle-div{
    display:flex;
    width : 50vw;
    align-self: center;
}

.centered-button{
    display : flex;
    align-items: center;
    align-content: center;
    align-self: center;
    width:100vw;
}
.main-container{
    display: grid; 
  place-items: center; 
 
}
.quiz-type{
    
  font-size: 2rem;
  text-align: center;

}

</style>
