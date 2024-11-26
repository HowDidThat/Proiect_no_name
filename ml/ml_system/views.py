import os

from ninja import Router

from .schemas import PredictionSchema, SymptomsSchema
from .services.strategies import DiagnosisPredictionStrategy
from ml.api.auth import ApiAuth
from ml.api.services import send_to_backend

ml_router = Router()
prediction_strategy = DiagnosisPredictionStrategy()


# @ml_router.post('/predict', response=PredictionSchema)
# def predict_disease(request, payload: SymptomsSchema):
#     input_data = {'symptoms': payload.symptoms}
#     predictions = prediction_strategy.predict(input_data)
#
#     return {'predictions': predictions}

@ml_router.post('/predict', response=PredictionSchema, auth=ApiAuth())
def predict_disease(request, payload: SymptomsSchema):
    if not request.auth:
        return 401, {"error": "Unauthorized request. Please provide a valid token"}

    input_data = {'symptoms': payload.symptoms}
    print("Received input data:", input_data)
    predictions = prediction_strategy.predict(input_data)

    if hasattr(payload, 'quiz_id'):
        send_to_backend(payload.quiz_id, predictions)

    return {'predictions': predictions}

@ml_router.get('/train')
def train_model(request):
    from .ml_models.diagnosis_model import DiagnosisModel
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'symbipredict_2022.csv')

    diagnosis_model = DiagnosisModel(data_path)
    diagnosis_model.train_model()
    return {'message': 'Model trained successfully'}
