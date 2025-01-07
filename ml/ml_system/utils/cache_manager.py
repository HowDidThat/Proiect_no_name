from hashlib import sha256
from typing import List

from ml_system.models import PredictionCache
import json

from .data_loader import DataLoader


class CacheManager:
    _symptoms_cache = None
    _diseases_cache = None

    @staticmethod
    def initialize_cache(data_path: str, severity_path: str):
        data_loader = DataLoader(data_path, severity_path)
        symptoms, diseases = data_loader.load_and_validate_data()
        CacheManager.set_symptoms(symptoms)
        CacheManager.set_diseases(diseases)

    @staticmethod
    def set_symptoms(symptoms: List[str]):
        CacheManager._symptoms_cache = symptoms

    @staticmethod
    def set_diseases(diseases: List[str]):
        CacheManager._diseases_cache = diseases

    @staticmethod
    def get_symptoms() -> List[str]:
        if CacheManager._symptoms_cache is None:
            raise ValueError("Symptoms cache not initialized")
        return CacheManager._symptoms_cache

    @staticmethod
    def get_diseases() -> List[str]:
        if CacheManager._diseases_cache is None:
            raise ValueError("Diseases cache not initialized")
        return CacheManager._diseases_cache


    @staticmethod
    def calculate_symptoms_hash(symptoms: list) -> str:
        symptoms_sorted = sorted(symptoms)
        symptoms_str = ",".join(symptoms_sorted)
        return sha256(symptoms_str.encode()).hexdigest()

    @staticmethod
    def get_cached_predictions(symptoms: list) -> dict | None:
        symptoms_hash = CacheManager.calculate_symptoms_hash(symptoms)
        cache_entry = PredictionCache.objects.filter(symptoms_hash=symptoms_hash).first()
        return json.loads(cache_entry.predictions) if cache_entry else None

    @staticmethod
    def save_predictions_to_cache(symptoms: list, predictions: dict) -> None:
        symptoms_hash = CacheManager.calculate_symptoms_hash(symptoms)
        predictions_json = json.dumps(predictions)
        PredictionCache.objects.create(
            symptoms_hash=symptoms_hash,
            predictions=predictions_json
        )