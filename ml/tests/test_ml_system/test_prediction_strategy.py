# tests/test_ml_system/test_prediction_strategy.py

import pytest
from django.test import TestCase
import pandas as pd
import numpy as np
from ml_system.services.strategies import (
    DiagnosisPredictionStrategy,
    PredictionStrategy,
    SymptomPredictionStrategy,
    SemanticSimilarityStrategy
)
import os


@pytest.mark.django_db
class TestPredictionStrategy(TestCase):
    def test_base_prediction_strategy(self):
        strategy = PredictionStrategy()

        result = strategy.predict({})
        self.assertIsNone(result)

        info = strategy.get_model_info()
        self.assertIsNone(info)



@pytest.mark.django_db
class TestDiagnosisPredictionStrategy(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.strategy = DiagnosisPredictionStrategy()
        cls.strategy.load_model()

    def test_load_model_file_not_found(self):
        strategy = DiagnosisPredictionStrategy()

        original_paths = {
            'model_path': strategy.model_path,
            'label_encoder_path': strategy.label_encoder_path,
            'all_symptoms_path': strategy.all_symptoms_path,
            'symptom_severity_path': strategy.symptom_severity_path
        }

        for path_key in original_paths:
            setattr(strategy, path_key, 'invalid_path.joblib')

            with self.assertRaises(FileNotFoundError):
                strategy.load_model()

            setattr(strategy, path_key, original_paths[path_key])

    def test_get_model_info(self):
        info = self.strategy.get_model_info()

        self.assertIsInstance(info, dict)

        self.assertEqual(info["model_type"], "RandomForestClassifier")
        self.assertEqual(
            info["description"],
            "Model for disease prediction based on symptoms"
        )

        self.assertEqual(set(info.keys()), {"model_type", "description"})

    def test_load_model_success(self):
        self.assertIsNotNone(self.strategy.model)
        self.assertIsNotNone(self.strategy.label_encoder)
        self.assertIsNotNone(self.strategy.all_symptoms)
        self.assertIsNotNone(self.strategy.symptom_severity)

    def test_validate_symptom_domain_valid(self):
        valid_symptoms = list(self.strategy.symptom_severity.keys())[:2]
        try:
            self.strategy.validate_symptom_domain(valid_symptoms)
        except ValueError:
            self.fail("validate_symptom_domain a ridicat ValueError neașteptat")

    def test_validate_symptom_domain_invalid(self):
        with self.assertRaises(ValueError):
            self.strategy.validate_symptom_domain(['invalid_symptom'])

    def test_preprocess_input_valid_symptoms(self):
        test_symptoms = list(self.strategy.symptom_severity.keys())[:2]
        input_data = {'symptoms': test_symptoms}
        result = self.strategy.preprocess_input(input_data)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.strategy.all_symptoms))
        for symptom in test_symptoms:
            if symptom in self.strategy.all_symptoms:
                idx = self.strategy.all_symptoms.index(symptom)
                self.assertGreater(result[idx], 0)

    def test_preprocess_input_empty_symptoms(self):
        input_data = {'symptoms': []}
        result = self.strategy.preprocess_input(input_data)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.strategy.all_symptoms))
        self.assertTrue(all(v == 0 for v in result))

    def test_predict_valid_input(self):
        features = np.zeros(len(self.strategy.all_symptoms))
        features_df = pd.DataFrame([features], columns=self.strategy.all_symptoms)

        predictions = self.strategy.predict(features_df)

        self.assertIsInstance(predictions, dict)
        self.assertTrue(len(predictions) > 0)
        total_prob = sum(predictions.values())
        self.assertAlmostEqual(total_prob, 1.0, places=5)

    def test_get_model_info(self):
        info = self.strategy.get_model_info()

        self.assertIsInstance(info, dict)
        self.assertIn('model_type', info)
        self.assertIn('description', info)
        self.assertEqual(info['model_type'], 'RandomForestClassifier')

@pytest.mark.django_db
class TestSymptomPredictionStrategy(TestCase):
    def test_symptom_prediction_strategy_init(self):
        model_path = "test_model_path"
        top_k = 10
        strategy = SymptomPredictionStrategy(model_path, top_k)

        self.assertEqual(strategy.model_path, model_path)
        self.assertEqual(strategy.top_k, top_k)


@pytest.mark.django_db
class TestSemanticSimilarityStrategy(TestCase):
    def test_semantic_similarity_strategy_init(self):
        model_path = "test_model_path"
        similarity_threshold = 0.9
        strategy = SemanticSimilarityStrategy(model_path, similarity_threshold)

        self.assertEqual(strategy.model_path, model_path)
        self.assertEqual(strategy.similarity_threshold, similarity_threshold)


