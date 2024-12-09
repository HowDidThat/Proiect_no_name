from random import random
from random import randint, sample
from typing import List, Dict

from backend.constants import ALL_SYMPTOMS


def generate_random_symptoms(num_symptoms: int) -> List[str]:
    return sample(ALL_SYMPTOMS, num_symptoms)


def generate_quiz_questions(ml_prediction_func) -> List[Dict]:
    MAX_ATTEMPTS = 10

    for _ in range(MAX_ATTEMPTS):
        questions = []
        all_diseases = set()

        for _ in range(5):
            num_symptoms = randint(1, 3)
            symptoms = generate_random_symptoms(num_symptoms)

            ml_response = ml_prediction_func(symptoms)

            if 'predictions' not in ml_response:
                continue

            relevant_diseases = {
                disease: prob
                for disease, prob in ml_response["predictions"].items()
                if prob > 0
            }

            all_diseases.update(relevant_diseases.keys())

            questions.append({
                "symptoms": symptoms,
                "diseases": relevant_diseases
            })

        if len(all_diseases) >= 5:
            return questions

    raise Exception("Could not generate quiz with enough unique diseases after maximum attempts")
