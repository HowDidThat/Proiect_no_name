import pytest
from unittest.mock import Mock, patch
from typing import List, Dict
from ml_system.services.facade import MLSystemFacade
from ml_system.services.factories import ModelFactory


class TestMLSystemFacade:
    def setup_method(self):
        self.diagnosis_factory = Mock(spec=ModelFactory)
        self.symptom_factory = Mock(spec=ModelFactory)
        self.facade = MLSystemFacade(
            diagnosis_factory=self.diagnosis_factory,
            symptom_factory=self.symptom_factory
        )

    def test_initialization(self):
        assert self.facade.diagnosis_factory == self.diagnosis_factory
        assert self.facade.symptom_factory == self.symptom_factory
        assert self.facade.diagnosis_pipeline is None
        assert self.facade.symptom_pipeline is None
        assert self.facade.semantic_adapter is None

    def test_initialize_models(self):
        mock_diagnosis_strategy = Mock()
        mock_symptom_strategy = Mock()
        mock_diagnosis_pipeline = Mock()
        mock_symptom_pipeline = Mock()

        self.diagnosis_factory.create_prediction_strategy.return_value = mock_diagnosis_strategy
        self.symptom_factory.create_prediction_strategy.return_value = mock_symptom_strategy
        self.diagnosis_factory.create_pipeline.return_value = mock_diagnosis_pipeline
        self.symptom_factory.create_pipeline.return_value = mock_symptom_pipeline

        self.facade.initialize_models()

        self.diagnosis_factory.create_prediction_strategy.assert_called_once()
        self.symptom_factory.create_prediction_strategy.assert_called_once()
        self.diagnosis_factory.create_pipeline.assert_called_once()
        self.symptom_factory.create_pipeline.assert_called_once()

    def test_predict_diagnosis(self):
        test_symptoms = ["fever", "cough"]
        expected_predictions = {"Flu": 0.8, "Cold": 0.2}

        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = expected_predictions
        self.facade.diagnosis_pipeline = mock_pipeline

        result = self.facade.predict_diagnosis(test_symptoms)

        assert result == expected_predictions
        mock_pipeline.predict.assert_called_once_with(test_symptoms)

    def test_predict_diagnosis_initializes_models_if_needed(self):
        test_symptoms = ["fever", "cough"]
        expected_predictions = {"Flu": 0.8, "Cold": 0.2}

        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = expected_predictions

        self.diagnosis_factory.create_pipeline.return_value = mock_pipeline

        result = self.facade.predict_diagnosis(test_symptoms)

        self.diagnosis_factory.create_prediction_strategy.assert_called_once()
        assert result == expected_predictions

    def test_predict_symptoms(self):
        test_diagnosis = "Flu"
        expected_symptoms = [
            {"symptom": "fever", "probability": 0.9},
            {"symptom": "cough", "probability": 0.7}
        ]

        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = expected_symptoms
        self.facade.symptom_pipeline = mock_pipeline

        result = self.facade.predict_symptoms(test_diagnosis)

        assert result == expected_symptoms
        mock_pipeline.predict.assert_called_once_with(test_diagnosis)

    def test_predict_symptoms_initializes_models_if_needed(self):
        test_diagnosis = "Flu"
        expected_symptoms = [
            {"symptom": "fever", "probability": 0.9},
            {"symptom": "cough", "probability": 0.7}
        ]

        mock_pipeline = Mock()
        mock_pipeline.predict.return_value = expected_symptoms

        self.symptom_factory.create_pipeline.return_value = mock_pipeline

        result = self.facade.predict_symptoms(test_diagnosis)

        self.symptom_factory.create_prediction_strategy.assert_called_once()
        assert result == expected_symptoms

    def test_compute_answer_similarity(self):
        user_answer = "high temperature"
        reference_symptom = "fever"
        expected_similarity = 0.85

        mock_adapter = Mock()
        mock_adapter.compute_similarity.return_value = expected_similarity
        self.facade.semantic_adapter = mock_adapter

        result = self.facade.compute_answer_similarity(user_answer, reference_symptom)

        assert result == expected_similarity
        mock_adapter.compute_similarity.assert_called_once_with(user_answer, reference_symptom)

    def test_compute_answer_similarity_without_adapter(self):

        user_answer = "high temperature"
        reference_symptom = "fever"

        with pytest.raises(ValueError) as exc_info:
            self.facade.compute_answer_similarity(user_answer, reference_symptom)
        assert "Semantic adapter not initialized" in str(exc_info.value)

    def test_facade_with_invalid_factories(self):
        with pytest.raises(TypeError):
            MLSystemFacade(None, None)

    def test_facade_with_missing_factories(self):
        with pytest.raises(TypeError):
            MLSystemFacade()