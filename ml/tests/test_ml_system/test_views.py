from django.test import TestCase
from unittest.mock import patch, Mock
import os
import pandas as pd

os.environ["NINJA_SKIP_REGISTRY"] = "1"


class TestMLViews(TestCase):
    def setUp(self):
        self.valid_symptoms = ['fever', 'cough']

    @patch('ml_system.views.DiagnosisPredictionStrategy')
    @patch('ml_system.views.CacheManager')
    def test_predict_disease_without_cache(self, mock_cache_manager, mock_strategy):
        mock_cache_manager.get_cached_predictions.return_value = None

        strategy_instance = Mock()
        strategy_instance.all_symptoms = ['fever', 'cough', 'headache']
        strategy_instance.predict.return_value = {'Disease1': 0.8, 'Disease2': 0.2}
        mock_strategy.return_value = strategy_instance

        mock_request = Mock()
        mock_request.auth = True

        class MockPayload:
            def __init__(self, symptoms):
                self.symptoms = symptoms

        payload = MockPayload(self.valid_symptoms)

        from ml_system.views import predict_disease

        response = predict_disease(mock_request, payload)

        self.assertIn('predictions', response)
        predictions = response['predictions']
        self.assertAlmostEqual(sum(predictions.values()), 100, places=1)

    @patch('ml_system.views.DiagnosisPredictionStrategy')
    @patch('ml_system.views.CacheManager')

    def test_predict_disease_with_cache(self, mock_cache_manager, mock_strategy):
        cached_predictions = {'Disease1': 75.0, 'Disease2': 25.0}
        mock_cache_manager.get_cached_predictions.return_value = cached_predictions

        mock_request = Mock()
        mock_request.auth = True

        class MockPayload:
            def __init__(self, symptoms):
                self.symptoms = symptoms

        payload = MockPayload(self.valid_symptoms)

        from ml_system.views import predict_disease

        response = predict_disease(mock_request, payload)

        self.assertIn('predictions', response)
        self.assertEqual(response['predictions'], cached_predictions)
        mock_strategy.return_value.predict.assert_not_called()

    @patch('ml_system.views.DiagnosisPredictionStrategy')
    def test_predict_disease_unauthorized(self, mock_strategy):
        mock_request = Mock()
        mock_request.auth = None

        class MockPayload:
            def __init__(self, symptoms):
                self.symptoms = symptoms

        payload = MockPayload(self.valid_symptoms)

        from ml_system.views import predict_disease

        response = predict_disease(mock_request, payload)

        self.assertEqual(response[0], 401)
        self.assertIn('error', response[1])

    @patch('ml_system.views.DiagnosisPredictionStrategy')
    @patch('ml_system.views.CacheManager')
    def test_predict_disease_with_quiz_id(self, mock_cache_manager, mock_strategy):
        mock_cache_manager.get_cached_predictions.return_value = None

        strategy_instance = Mock()
        strategy_instance.all_symptoms = ['fever', 'cough', 'headache']
        strategy_instance.predict.return_value = {'Disease1': 0.8, 'Disease2': 0.2}
        mock_strategy.return_value = strategy_instance

        mock_request = Mock()
        mock_request.auth = True

        class MockPayload:
            def __init__(self, symptoms, quiz_id):
                self.symptoms = symptoms
                self.quiz_id = quiz_id

        payload = MockPayload(self.valid_symptoms, 123)

        from ml_system.views import predict_disease

        with patch('ml_system.views.send_to_backend') as mock_send:
            response = predict_disease(mock_request, payload)

            self.assertIn('predictions', response)
            mock_send.assert_called_once()

    @patch('ml_system.views.DiagnosisPredictionStrategy')
    def test_predict_disease_validation_error(self, mock_strategy):
        strategy_instance = Mock()
        strategy_instance.validate_symptom_domain.side_effect = ValueError("Invalid symptom")
        mock_strategy.return_value = strategy_instance

        mock_request = Mock()
        mock_request.auth = True

        class MockPayload:
            def __init__(self, symptoms):
                self.symptoms = symptoms

        payload = MockPayload(['invalid_symptom'])

        from ml_system.views import predict_disease

        with self.assertRaises(ValueError):
            predict_disease(mock_request, payload)

    @patch('ml_system.ml_models.diagnosis_model.DiagnosisModel')
    def test_train_model(self, mock_diagnosis_model):
        mock_instance = Mock()
        mock_instance.train_model.return_value = {
            'training_time': 1.23,
            'train_accuracy': 0.95,
            'test_accuracy': 0.92,
            'cv_scores_mean': 0.93,
            'cv_scores_std': 0.02,
            'roc_auc_score': 0.96,
            'classification_report': 'Test Report',
            'top_features': [{'feature': 'fever', 'importance': 0.8}]
        }
        mock_diagnosis_model.return_value = mock_instance

        from ml_system.views import train_model

        mock_request = Mock()

        response = train_model(mock_request)

        self.assertIn('message', response)
        self.assertEqual(response['message'], 'Model trained successfully')
        self.assertIn('metrics', response)

        mock_diagnosis_model.assert_called_once()
        mock_instance.train_model.assert_called_once()

        print(f"Train model response: {response}")