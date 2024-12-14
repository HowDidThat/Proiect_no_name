from hashlib import sha256
from ml_system.models import PredictionCache
import json

class CacheManager:
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