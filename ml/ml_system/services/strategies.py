import os
import numpy as np
from typing import Dict, Any

from .repository import ModelRepository
from ml_system.services.decorators import log_execution_time


class PredictionStrategy:
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        pass

    def get_model_info(self) -> Dict[str, str]:
        pass


class DiagnosisPredictionStrategy(PredictionStrategy):
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(base_dir, '../../ml/saved_models')
        joblib_dir = os.path.join(base_dir, '../../ml/joblibs')
        self.model_repository = ModelRepository(model_dir, joblib_dir)
        self.model = None
        self.label_encoder = None
        self.all_symptoms = None
        self.symptom_severity = None

    @log_execution_time
    def load_model(self):
        try:
            self.model = self.model_repository.get_model('diagnosis_model')
            self.label_encoder = self.model_repository.get_joblib('label_encoder')
            self.all_symptoms = self.model_repository.get_joblib('all_symptoms')
            self.symptom_severity = self.model_repository.get_joblib('symptom_severity')
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Component not found: {str(e)}")

    def predict(self, features_df) -> Dict[str, float]:
        probabilities = self.model.predict_proba(features_df)[0]
        disease_names = self.label_encoder.inverse_transform(range(len(probabilities)))
        result = dict(zip(disease_names, probabilities))
        sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

        return sorted_result

    def validate_symptom_domain(self, symptoms):
        print("Severity symptoms", symptoms)
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