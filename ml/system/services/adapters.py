from abc import ABC, abstractmethod
import numpy as np

class PreTrainedModelAdapter(ABC):
    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def encode_text(self, text: str) -> np.ndarray:
        pass

    @abstractmethod
    def compute_similarity(self, text1: str, text2: str) -> float:
        pass

class BERTModelAdapter(PreTrainedModelAdapter):
    def __init__(self, model_name: str, device: str = 'cpu'):
        self.model_name = model_name
        self.device = device

class GPTModelAdapter(PreTrainedModelAdapter):
    def __init__(self, model_name: str, device: str = 'cpu'):
        self.model_name = model_name
        self.device = device