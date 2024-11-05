from abc import ABC, abstractmethod
from typing import Dict, Any

class PredictionStrategy(ABC):
    @abstractmethod
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        pass

class DiagnosisPredictionStrategy:
    def __init__(self, model_path: str, threshold: float = 0.5):
        self.model_path = model_path
        self.threshold = threshold

    def predict(self, input_data: dict) -> dict:
        return {
            "pneumonia": 0.8,
            "flu": 0.2
        }

    def get_model_info(self) -> dict:
        return {
            "model_path": self.model_path,
            "threshold": str(self.threshold),
            "model_type": "diagnosis"
        }

class SymptomPredictionStrategy(PredictionStrategy):
    def __init__(self, model_path: str, top_k: int = 5):
        self.model_path = model_path
        self.top_k = top_k

class SemanticSimilarityStrategy(PredictionStrategy):
    def __init__(self, model_path: str, similarity_threshold: float = 0.8):
        self.model_path = model_path
        self.similarity_threshold = similarity_threshold