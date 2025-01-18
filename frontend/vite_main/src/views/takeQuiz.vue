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
              {{ aaaaa(dictSymptoms,symptom) }}
            </span>
          </div>
        </div>

        <!-- Disease Selection -->
        <div class="mb-6">
          <h3 class="text-gray-700 font-bold mb-2">Select Diseases:</h3>
          <div class="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto">
            <div v-for="disease in currentQuestion?.diseases" 
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
import { quizData } from '../utils/backendCommunication';
import { aaaaa } from '../utils/formatChenger';
import { getRandomDiseases } from '../utils/formatChenger';
import { sq } from '../utils/backendCommunication';
import { toRaw } from 'vue';
export default {
  setup() {
    const questions = ref([])
    const currentIndex = ref(0)
    const selectedDiseases = ref([])
    const timer = ref('00:00')
    const answers = ref([])
    const route = useRoute()
    const quizId = ref(route.params.id)
    const dictDiseases = ref({
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
    const dictSymptoms = ref({
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

    const currentQuestion = computed(() => 
      questions.value[currentIndex.value]
    )

    onMounted(async () => {
      
        const token = $cookies.get("access_token");
        const response = await quizData(token,quizId.value);
        let temp = response.data.questions;
        console.log(temp);
        //questions.value = response.data.questions;
        for (let q in temp){
      
           let d = temp[q].diseases;
           let s = temp[q].symptoms;
           questions.value.push({"diseases":d, "symptoms":s});
          }
        startTimer();
      })
    const startTimer = () => {
      let seconds = 300
      setInterval(() => {
        if (seconds == 0)
          submitAnswers();
        seconds--
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
      const token = $cookies.get("access_token");
      let answerDict = {};
      for (let i in answers.value)
        {
         
         answerDict["Question"+i] = toRaw(answers.value[i]);
         
        }
      console.log(answerDict);
      const response = await sq(token,quizId.value,answerDict);
      console.log(response);
      router.push("/account");
    }

    return {
      questions,
      currentIndex,
      currentQuestion,
      selectedDiseases,
      timer,
      aaaaa,
      dictDiseases,
      dictSymptoms,
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