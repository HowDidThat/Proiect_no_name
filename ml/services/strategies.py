from abc import ABC, abstractmethod
from typing import Dict, Any

class PredictionStrategy(ABC):
    @abstractmethod
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, float]:
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        pass

class DiagnosisPredictionStrategy(PredictionStrategy):
    def __init__(self, model_path: str, threshold: float = 0.5):
        self.model_path = model_path
        self.threshold = threshold

class SymptomPredictionStrategy(PredictionStrategy):
    def __init__(self, model_path: str, top_k: int = 5):
        self.model_path = model_path
        self.top_k = top_k

class SemanticSimilarityStrategy(PredictionStrategy):
    def __init__(self, model_path: str, similarity_threshold: float = 0.8):
        self.model_path = model_path
        self.similarity_threshold = similarity_threshold