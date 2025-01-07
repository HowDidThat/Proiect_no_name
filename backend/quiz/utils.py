from heapq import nlargest, nsmallest
from random import randint, sample
from typing import List, Dict

from backend.constants import ALL_SYMPTOMS


def generate_random_symptoms(num_symptoms: int) -> List[str]:
    if num_symptoms < 1:
        raise ValueError("Number of symptoms must be at least 1")

    return sample(ALL_SYMPTOMS, num_symptoms)


def get_top_and_bottom_diseases(disease_dict: Dict[str, float],
                                top_n: int = 2, random_bottom: int = 4) -> Dict[str, float]:
    top_diseases = dict(nlargest(top_n, disease_dict.items(), key=lambda x: x[1]))

    bottom_10 = dict(nsmallest(10, disease_dict.items(), key=lambda x: x[1]))
    random_bottom_diseases = dict(sample(list(bottom_10.items()), random_bottom))

    result_diseases = {**top_diseases, **random_bottom_diseases}
    return result_diseases


def generate_quiz_questions(ml_prediction_func) -> List[Dict]:
    MAX_ATTEMPTS = 10

    try:
        for attempt in range(MAX_ATTEMPTS):
            questions = []
            all_diseases = set()

            for _ in range(5):
                num_symptoms = randint(1, 3)
                symptoms = generate_random_symptoms(num_symptoms)

                ml_response = ml_prediction_func(symptoms)

                if not ml_response or 'predictions' not in ml_response:
                    continue

                relevant_diseases = {
                    disease: prob
                    for disease, prob in ml_response["predictions"].items()
                    if prob > 0
                }

                if not relevant_diseases:
                    continue

                selected_diseases = get_top_and_bottom_diseases(relevant_diseases)

                all_diseases.update(selected_diseases.keys())

                questions.append({
                    "symptoms": symptoms,
                    "diseases": selected_diseases
                })

            if len(questions) == 5 and len(all_diseases) >= 5:
                return questions

        raise Exception("Could not generate quiz with enough unique diseases after maximum attempts")

    except Exception as e:
        raise Exception("Failed to generate questions") from e
