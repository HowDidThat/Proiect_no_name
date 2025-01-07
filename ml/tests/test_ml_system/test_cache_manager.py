from django.test import TestCase
from ml_system.utils.cache_manager import CacheManager
from ml_system.models import PredictionCache
import json


class TestCacheManager(TestCase):
    def setUp(self):
        self.test_symptoms = ['fever', 'cough']
        self.test_predictions = {'Flu': 0.8, 'Cold': 0.2}

    def test_calculate_symptoms_hash(self):
        hash1 = CacheManager.calculate_symptoms_hash(['fever', 'cough'])
        hash2 = CacheManager.calculate_symptoms_hash(['cough', 'fever'])
        self.assertEqual(hash1, hash2)

        hash3 = CacheManager.calculate_symptoms_hash(['headache', 'nausea'])
        self.assertNotEqual(hash1, hash3)

    def test_save_predictions_to_cache(self):
        CacheManager.save_predictions_to_cache(self.test_symptoms, self.test_predictions)

        cache_entry = PredictionCache.objects.first()
        self.assertIsNotNone(cache_entry)
        self.assertEqual(
            json.loads(cache_entry.predictions),
            self.test_predictions
        )

    def test_get_cached_predictions_exists(self):
        CacheManager.save_predictions_to_cache(self.test_symptoms, self.test_predictions)

        cached_predictions = CacheManager.get_cached_predictions(self.test_symptoms)
        self.assertEqual(cached_predictions, self.test_predictions)

    def test_get_cached_predictions_not_exists(self):
        cached_predictions = CacheManager.get_cached_predictions(['nonexistent'])
        self.assertIsNone(cached_predictions)

    def test_multiple_cache_entries(self):
        symptoms1 = ['fever', 'cough']
        symptoms2 = ['headache', 'nausea']
        predictions1 = {'Flu': 0.8, 'Cold': 0.2}
        predictions2 = {'Migraine': 0.9, 'Stress': 0.1}

        CacheManager.save_predictions_to_cache(symptoms1, predictions1)
        CacheManager.save_predictions_to_cache(symptoms2, predictions2)

        self.assertEqual(PredictionCache.objects.count(), 2)
        self.assertEqual(
            CacheManager.get_cached_predictions(symptoms1),
            predictions1
        )
        self.assertEqual(
            CacheManager.get_cached_predictions(symptoms2),
            predictions2
        )