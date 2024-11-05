from abc import ABC, abstractmethod
from typing import Dict, Any

import numpy as np
from .strategies import PredictionStrategy

class MLPipeline(ABC):
    def __init__(self):
        self.preprocessor = None
        self.model = None
        self.postprocessor = None

    @abstractmethod
    def preprocess_data(self, data: Dict[str, Any]) -> np.ndarray:
        pass

    @abstractmethod
    def predict(self, features: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def postprocess_results(self, predictions: np.ndarray) -> Dict[str, Any]:
        pass


class DiagnosisPipeline:
    def __init__(self, prediction_strategy):
        self.prediction_strategy = prediction_strategy

    def preprocess_data(self, data: dict) -> np.ndarray:
        all_symptoms = ["fever", "cough", "fatigue", "shortness_of_breath"]
        vector = np.zeros(len(all_symptoms))

        for i, symptom in enumerate(all_symptoms):
            if symptom in data.get("symptoms", []):
                vector[i] = 1

        return vector


class SymptomPipeline(MLPipeline):
    def __init__(self, prediction_strategy: PredictionStrategy):
        super().__init__()
        self.prediction_strategy = prediction_strategy