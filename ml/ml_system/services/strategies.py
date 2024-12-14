import os
import joblib
import numpy as np
from typing import Dict, Any
import pandas as pd

from ..utils.decorators import log_execution_time


class PredictionStrategy:
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        pass

    def get_model_info(self) -> Dict[str, str]:
        pass


class DiagnosisPredictionStrategy(PredictionStrategy):
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.all_symptoms = None
        self.symptom_severity = None
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_dir = os.path.join(base_dir, 'ml_models', 'saved_models')
        self.model_path = os.path.join(self.model_dir, 'diagnosis_model.joblib')
        self.label_encoder_path = os.path.join(self.model_dir, 'label_encoder.joblib')
        self.all_symptoms_path = os.path.join(self.model_dir, 'all_symptoms.joblib')
        self.symptom_severity_path = os.path.join(self.model_dir, 'symptom_severity.joblib')


    @log_execution_time
    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model file not found. Please train the model first")
        if not os.path.exists(self.label_encoder_path):
            raise FileNotFoundError("Label encoder file not found. Please train the model first")
        if not os.path.exists(self.all_symptoms_path):
            raise FileNotFoundError("All symptoms file not found. Please train the model first")
        if not os.path.exists(self.symptom_severity_path):
            raise FileNotFoundError("Symptom severity file not found. Please train the model first")

        self.model = joblib.load(self.model_path)
        self.label_encoder = joblib.load(self.label_encoder_path)
        self.all_symptoms = joblib.load(self.all_symptoms_path)
        self.symptom_severity = joblib.load(self.symptom_severity_path)

    def predict(self, features_df) -> Dict[str, float]:
        probabilities = self.model.predict_proba(features_df)[0]
        disease_names = self.label_encoder.inverse_transform(range(len(probabilities)))
        result = dict(zip(disease_names, probabilities))
        sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

        return sorted_result

    def validate_symptom_domain(self, symptoms):
        severity_symptoms = self.symptom_severity.keys()
        for symptom in symptoms:
            norm_symptom = symptom.lower().replace(" ", "_")
            if norm_symptom not in severity_symptoms:
                raise ValueError(f"Invalid symptom: {symptom}")

    def preprocess_input(self, input_data: Dict[str, Any]) -> np.ndarray:
        input_symptoms = [s.lower().replace(" ", "_") for s in input_data.get('symptoms', [])]
        input_vector = np.zeros(len(self.all_symptoms))
        for symptom in input_symptoms:
            if symptom in self.all_symptoms:
                index = self.all_symptoms.index(symptom)
                input_vector[index] = self.symptom_severity[symptom]
        return input_vector

    def get_model_info(self) -> Dict[str, str]:
        return {
            "model_type": "RandomForestClassifier",
            "description": "Model for disease prediction based on symptoms"
        }


class SymptomPredictionStrategy(PredictionStrategy):
    def __init__(self, model_path: str, top_k: int = 5):
        self.model_path = model_path
        self.top_k = top_k


class SemanticSimilarityStrategy(PredictionStrategy):
    def __init__(self, model_path: str, similarity_threshold: float = 0.8):
        self.model_path = model_path
        self.similarity_threshold = similarity_threshold
