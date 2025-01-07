import os
from typing import List

import pandas as pd
from ninja import Router

from ml import settings
from .schemas import PredictionSchema, SymptomsSchema, SymptomsListSchema, DiseasesListSchema
from .services.strategies import DiagnosisPredictionStrategy
from .utils.decorators import log_execution_time, clean_and_validate_data
from ml.api.auth import ApiAuth

from ml.api.services import send_to_backend

ml_router = Router()
prediction_strategy = DiagnosisPredictionStrategy()

from .utils.cache_manager import CacheManager

CacheManager.initialize_cache(settings.DATA_PATH, settings.SEVERITY_PATH)

@ml_router.post('/predict', response=PredictionSchema, auth=ApiAuth())
@log_execution_time
@clean_and_validate_data
def predict_disease(request, payload: SymptomsSchema):
    if prediction_strategy.model is None or prediction_strategy.label_encoder is None or prediction_strategy.all_symptoms is None or prediction_strategy.symptom_severity is None:
        prediction_strategy.load_model()

    if not request.auth:
        return 401, {"error": "Unauthorized request. Please provide a valid token"}

    input_data = {'symptoms': payload.symptoms}
    symptoms = input_data.get('symptoms', [])

    prediction_strategy.validate_symptom_domain(symptoms)

    cached_predictions = CacheManager.get_cached_predictions(symptoms)
    if cached_predictions:
        return {'predictions': cached_predictions}


    features = prediction_strategy.preprocess_input({'symptoms': symptoms})
    features_df = pd.DataFrame([features], columns=prediction_strategy.all_symptoms)

    predictions = prediction_strategy.predict(features_df)

    total = sum(predictions.values())
    predictions_in_percentages = {
        disease: round((prob / total) * 100, 2) for disease, prob in predictions.items()
    }

    CacheManager.save_predictions_to_cache(symptoms, predictions_in_percentages)

    if hasattr(payload, 'quiz_id'):
        send_to_backend(payload.quiz_id, predictions_in_percentages)

    return {'predictions': predictions_in_percentages}



@ml_router.get('/train')
def train_model(request):
    from .ml_models.diagnosis_model import DiagnosisModel
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'dataset.csv')
    severity_data_path = os.path.join(base_dir, 'data', 'Symptom-severity.csv')
    diagnosis_model = DiagnosisModel(data_path, severity_data_path)
    response = diagnosis_model.train_model()
    return {'message': 'Model trained successfully', 'metrics': response}


@ml_router.get('/symptoms', response=SymptomsListSchema)
@log_execution_time
def get_symptoms(request):
    symptoms = CacheManager.get_symptoms()
    return {'symptoms': symptoms}

@ml_router.get('/diseases', response=DiseasesListSchema)
@log_execution_time
def get_diseases(request):
    diseases = CacheManager.get_diseases()
    return {'diseases': diseases}