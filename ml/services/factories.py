from abc import ABC, abstractmethod
from typing import Dict, Any

from .strategies import PredictionStrategy
from .pipeline import MLPipeline
from .adapters import PreTrainedModelAdapter

class ModelFactory(ABC):
    @abstractmethod
    def create_prediction_strategy(self) -> PredictionStrategy:
        pass

    @abstractmethod
    def create_pipeline(self, strategy: PredictionStrategy) -> MLPipeline:
        pass

    @abstractmethod
    def create_semantic_adapter(self) -> PreTrainedModelAdapter:
        pass

class DiagnosisModelFactory(ModelFactory):
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config

class SymptomModelFactory(ModelFactory):
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config


class ImageModelFactory(ModelFactory):
    def __init__(self, model_config: Dict[str, Any]):
        self.model_config = model_config
