from typing import List, Dict
from .factories import ModelFactory

class MLSystemFacade:
    def __init__(
        self,
        diagnosis_factory: ModelFactory,
        symptom_factory: ModelFactory
    ):
        self.diagnosis_factory = diagnosis_factory
        self.symptom_factory = symptom_factory
        self.diagnosis_pipeline = None
        self.symptom_pipeline = None
        self.semantic_adapter = None

    def initialize_models(self) -> None:
        pass

    def predict_diagnosis(self, symptoms: List[str]) -> Dict[str, float]:
        pass

    def predict_symptoms(self, diagnosis: str) -> List[Dict[str, float]]:
        pass

    def compute_answer_similarity(self, user_answer: str, reference_symptom: str) -> float:
        pass