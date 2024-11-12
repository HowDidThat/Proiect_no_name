from abc import ABC, abstractmethod
from typing import Dict


class ModelMonitor(ABC):
    @abstractmethod
    def update(self, metrics: Dict[str, float]) -> None:
        pass


class PredictionMonitor(ModelMonitor):
    def __init__(self):
        self.prediction_history = []


class PerformanceMonitor(ModelMonitor):
    def __init__(self):
        self.performance_metrics = {}
