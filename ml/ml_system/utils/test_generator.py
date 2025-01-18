import random

from ml.ml.settings import DATA_PATH, SEVERITY_PATH
from ml_system.services.data_validator import DataValidator
from ml_system.services.strategies import DiagnosisPredictionStrategy

prediction_strategy = DiagnosisPredictionStrategy()
prediction_strategy.load_model()

import random
import json
import pandas as pd
from typing import List, Dict


class TestGenerator:
    def __init__(self, cleaned_symptoms_df: pd.DataFrame):
        self.df = cleaned_symptoms_df
        self.test_cases = []
        self.test_results = []
        self.all_symptoms = self.get_all_unique_symptoms()

    def get_all_unique_symptoms(self):
        symptoms = set()
        for col in self.df.columns[1:]:  # Exclude coloana Disease
            symptoms.update(self.df[col].dropna().unique())
        return [s for s in symptoms if isinstance(s, str) and s.strip()]

    def get_symptom_weights(self, disease: str) -> Dict[str, float]:
        disease_data = self.df[self.df['Disease'] == disease]
        symptom_counts = {}

        for col in self.df.columns[1:]:
            symptoms = disease_data[col].value_counts()
            for symptom in symptoms.index:
                if pd.notna(symptom) and isinstance(symptom, str):
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + symptoms[symptom]

        total = sum(symptom_counts.values())
        if total == 0:
            return {}
        weights = {symptom: count / total for symptom, count in symptom_counts.items()}
        return weights

    def get_expected_diseases(self, symptoms: List[str]) -> Dict[str, float]:
        disease_scores = {}

        for disease in self.df['Disease'].unique():
            disease_data = self.df[self.df['Disease'] == disease]
            score = 0
            matches = 0

            for symptom in symptoms:
                for col in self.df.columns[1:]:
                    if (disease_data[col] == symptom).any():
                        matches += 1
                        break

            if matches > 0:
                score = matches / len(symptoms)
                disease_scores[disease] = score

        total = sum(disease_scores.values())
        if total > 0:
            disease_scores = {
                disease: round((score / total) * 100, 2)
                for disease, score in disease_scores.items()
            }

        return dict(sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)[:3])

    def generate_variations(self, original_symptoms: List[str], n_variations: int = 2) -> List[List[str]]:
        variations = []
        for _ in range(n_variations):
            variation = original_symptoms.copy()

            n_add = random.randint(1, 3)
            additional_symptoms = random.sample([s for s in self.all_symptoms if s not in variation], n_add)
            variation.extend(additional_symptoms)

            if len(variation) > 3:
                n_remove = random.randint(1, min(2, len(variation) - 3))
                to_remove = random.sample(variation, n_remove)
                variation = [s for s in variation if s not in to_remove]

            variations.append(variation)
        return variations

    def generate_test_cases(self) -> List[Dict]:
        for disease in self.df['Disease'].unique():
            weights = self.get_symptom_weights(disease)
            if not weights:
                continue

            common_symptoms = sorted(weights.items(), key=lambda x: x[1], reverse=True)
            valid_symptoms = [s[0] for s in common_symptoms if isinstance(s[0], str) and s[0].strip()]

            if valid_symptoms:
                for n_symptoms in [3, 4, 5, 6]:
                    if len(valid_symptoms) >= n_symptoms:
                        # Cazul original cu n_symptoms simptome
                        self.test_cases.append({
                            'test_id': len(self.test_cases) + 1,
                            'symptoms': valid_symptoms[:n_symptoms],
                            'type': 'original'
                        })

                        variations = self.generate_variations(valid_symptoms[:n_symptoms])
                        for var in variations:
                            self.test_cases.append({
                                'test_id': len(self.test_cases) + 1,
                                'symptoms': var,
                                'type': 'variation'
                            })

        n_random_cases = 10
        for _ in range(n_random_cases):
            n_symptoms = random.randint(2, 7)
            random_symptoms = random.sample(self.all_symptoms, n_symptoms)
            self.test_cases.append({
                'test_id': len(self.test_cases) + 1,
                'symptoms': random_symptoms,
                'type': 'random'
            })

        return self.test_cases

    def run_tests(self, prediction_strategy) -> List[Dict]:
        if (prediction_strategy.model is None or
                prediction_strategy.label_encoder is None or
                prediction_strategy.all_symptoms is None or
                prediction_strategy.symptom_severity is None):
            prediction_strategy.load_model()

        for test_case in self.test_cases:
            try:
                expected_diseases = self.get_expected_diseases(test_case['symptoms'])

                features = prediction_strategy.preprocess_input({'symptoms': test_case['symptoms']})
                features_df = pd.DataFrame([features], columns=prediction_strategy.all_symptoms)
                predictions = prediction_strategy.predict(features_df)

                total = sum(predictions.values())
                predictions_in_percentages = {
                    disease: round((prob / total) * 100, 2)
                    for disease, prob in predictions.items()
                }

                top_3_predictions = dict(sorted(predictions_in_percentages.items(),
                                                key=lambda x: x[1],
                                                reverse=True)[:3])

                common_diseases = set(expected_diseases.keys()) & set(top_3_predictions.keys())
                match_score = len(common_diseases) / 3  # Câte din top 3 se potrivesc

                self.test_results.append({
                    'test_id': test_case['test_id'],
                    'type': test_case['type'],
                    'symptoms': test_case['symptoms'],
                    'expected_top_3': expected_diseases,
                    'predicted_top_3': top_3_predictions,
                    'match_score': match_score,
                    'common_diseases': list(common_diseases)
                })
            except Exception as e:
                print(f"Error processing test case {test_case['test_id']}: {str(e)}")
                continue

        return self.test_results

    def print_results(self):
        total_tests = len(self.test_results)
        perfect_matches = sum(1 for t in self.test_results if t['match_score'] == 1)
        partial_matches = sum(1 for t in self.test_results if 0 < t['match_score'] < 1)
        no_matches = sum(1 for t in self.test_results if t['match_score'] == 0)

        print("\n=== Test Results Summary ===")
        print(f"Total tests: {total_tests}")
        print(f"Perfect matches (all 3): {perfect_matches} ({(perfect_matches / total_tests) * 100:.2f}%)")
        print(f"Partial matches: {partial_matches} ({(partial_matches / total_tests) * 100:.2f}%)")
        print(f"No matches: {no_matches} ({(no_matches / total_tests) * 100:.2f}%)")

        print("\n=== Perfect Matches ===")
        for test in self.test_results:
            if test['match_score'] == 1:
                print(f"\nTest ID: {test['test_id']} ({test['type'].upper()})")
                print(f"Symptoms: {', '.join(test['symptoms'])}")
                print("Expected top 3:")
                for disease, prob in test['expected_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print("Predicted top 3:")
                for disease, prob in test['predicted_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print("-" * 50)

        print("\n=== Partial Matches ===")
        for test in self.test_results:
            if 0 < test['match_score'] < 1:
                print(f"\nTest ID: {test['test_id']} ({test['type'].upper()})")
                print(f"Symptoms: {', '.join(test['symptoms'])}")
                print("Expected top 3:")
                for disease, prob in test['expected_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print("Predicted top 3:")
                for disease, prob in test['predicted_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print(f"Common diseases: {', '.join(test['common_diseases'])}")
                print("-" * 50)

        print("\n=== No Matches ===")
        for test in self.test_results:
            if test['match_score'] == 0:
                print(f"\nTest ID: {test['test_id']} ({test['type'].upper()})")
                print(f"Symptoms: {', '.join(test['symptoms'])}")
                print("Expected top 3:")
                for disease, prob in test['expected_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print("Predicted top 3:")
                for disease, prob in test['predicted_top_3'].items():
                    print(f"  - {disease}: {prob}%")
                print("-" * 50)

        print("\n=== Symptom Count Distribution ===")
        symptom_counts = {}
        for test in self.test_results:
            n_symptoms = len(test['symptoms'])
            symptom_counts[n_symptoms] = symptom_counts.get(n_symptoms, 0) + 1

        for n_symptoms, count in sorted(symptom_counts.items()):
            print(f"\nTests with {n_symptoms} symptoms: {count}")
            tests_with_n = [t for t in self.test_results if len(t['symptoms']) == n_symptoms]
            perfect = sum(1 for t in tests_with_n if t['match_score'] == 1)
            partial = sum(1 for t in tests_with_n if 0 < t['match_score'] < 1)
            none = sum(1 for t in tests_with_n if t['match_score'] == 0)
            print(f"Perfect matches: {perfect} ({(perfect / count) * 100:.2f}%)")
            print(f"Partial matches: {partial} ({(partial / count) * 100:.2f}%)")
            print(f"No matches: {none} ({(none / count) * 100:.2f}%)")

    def save_results(self, output_path: str = "test_results.json"):
        results_to_save = {
            'summary': {
                'total_tests': len(self.test_results),
                'perfect_matches': sum(1 for t in self.test_results if t['match_score'] == 1),
                'partial_matches': sum(1 for t in self.test_results if 0 < t['match_score'] < 1),
                'no_matches': sum(1 for t in self.test_results if t['match_score'] == 0)
            },
            'detailed_results': self.test_results
        }

        with open(output_path, 'w') as f:
            json.dump(results_to_save, f, indent=4)


def run_model_tests(prediction_strategy, cleaned_symptoms_df):
    if (prediction_strategy.model is None or
            prediction_strategy.label_encoder is None or
            prediction_strategy.all_symptoms is None or
            prediction_strategy.symptom_severity is None):
        prediction_strategy.load_model()

    tester = TestGenerator(cleaned_symptoms_df)

    test_cases = tester.generate_test_cases()
    print(f"Generated {len(test_cases)} test cases")

    results = tester.run_tests(prediction_strategy)

    tester.print_results()

    tester.save_results()


validator = DataValidator()
cleaned_symptoms_df, cleaned_severity_df = validator.spec_validate_then_send(
    DATA_PATH, SEVERITY_PATH
)

run_model_tests(prediction_strategy, cleaned_symptoms_df)
