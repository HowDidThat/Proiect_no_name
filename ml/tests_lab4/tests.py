# tests.py

import unittest
from unittest.mock import Mock, patch
from django.test import TestCase
import numpy as np

from services.strategies import DiagnosisPredictionStrategy, SymptomPredictionStrategy
from services.pipeline import DiagnosisPipeline, SymptomPipeline
from services.adapters import BERTModelAdapter, GPTModelAdapter
from services.facade import MLSystemFacade
from services.factories import DiagnosisModelFactory, SymptomModelFactory


class TestPredictionStrategies(unittest.TestCase):
    def setUp(self):
        self.diagnosis_strategy = DiagnosisPredictionStrategy(
            model_path="models/diagnosis.pkl",
            threshold=0.5
        )

    def test_diagnosis_strategy_initialization(self):
        self.assertEqual(self.diagnosis_strategy.model_path, "models/diagnosis.pkl")
        self.assertEqual(self.diagnosis_strategy.threshold, 0.5)

    def test_diagnosis_strategy_get_model_info(self):
        info = self.diagnosis_strategy.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertIn('model_path', info)
        self.assertEqual(info['model_path'], "models/diagnosis.pkl")

    def test_diagnosis_strategy_predict(self):
        input_data = {"symptoms": ["fever", "cough"]}
        result = self.diagnosis_strategy.predict(input_data)

        self.assertIsInstance(result, dict)
        for value in result.values():
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)


class TestMLPipeline(unittest.TestCase):
    def setUp(self):
        self.strategy = Mock(spec=DiagnosisPredictionStrategy)
        self.pipeline = DiagnosisPipeline(prediction_strategy=self.strategy)

    def test_pipeline_initialization(self):
        self.assertIsNotNone(self.pipeline.prediction_strategy)

    def test_preprocess_data(self):
        input_data = {"symptoms": ["fever", "cough"]}
        result = self.pipeline.preprocess_data(input_data)
        self.assertIsInstance(result, np.ndarray)


class TestBERTAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = BERTModelAdapter(model_name="bert-base-uncased")

    def test_adapter_initialization(self):
        self.assertEqual(self.adapter.model_name, "bert-base-uncased")
        self.assertEqual(self.adapter.device, "cpu")

    def test_compute_similarity(self):
        text1 = "fever"
        text2 = "high temperature"
        similarity = self.adapter.compute_similarity(text1, text2)

        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0)
        self.assertLessEqual(similarity, 1)


if __name__ == '__main__':
    unittest.main()