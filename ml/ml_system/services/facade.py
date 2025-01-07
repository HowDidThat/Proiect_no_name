from typing import List, Dict
from .factories import ModelFactory


class MLSystemFacade:
    def __init__(
            self,
            diagnosis_factory: ModelFactory,
            symptom_factory: ModelFactory
    ):
        if not isinstance(diagnosis_factory, ModelFactory) or not isinstance(symptom_factory, ModelFactory):
            raise TypeError("Invalid factory types")

        self.diagnosis_factory = diagnosis_factory
        self.symptom_factory = symptom_factory
        self.diagnosis_pipeline = None
        self.symptom_pipeline = None
        self.semantic_adapter = None

    def initialize_models(self) -> None:
        diagnosis_strategy = self.diagnosis_factory.create_prediction_strategy()
        symptom_strategy = self.symptom_factory.create_prediction_strategy()

        self.diagnosis_pipeline = self.diagnosis_factory.create_pipeline(diagnosis_strategy)
        self.symptom_pipeline = self.symptom_factory.create_pipeline(symptom_strategy)

    def predict_diagnosis(self, symptoms: List[str]) -> Dict[str, float]:
        if not self.diagnosis_pipeline:
            self.initialize_models()
        return self.diagnosis_pipeline.predict(symptoms)

    def predict_symptoms(self, diagnosis: str) -> List[Dict[str, float]]:
        if not self.symptom_pipeline:
            self.initialize_models()
        return self.symptom_pipeline.predict(diagnosis)

    def compute_answer_similarity(self, user_answer: str, reference_symptom: str) -> float:
        if not self.semantic_adapter:
            raise ValueError("Semantic adapter not initialized")
        return self.semantic_adapter.compute_similarity(user_answer, reference_symptom)