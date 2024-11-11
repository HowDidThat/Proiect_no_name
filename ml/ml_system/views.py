import os

from ninja import Router

from .schemas import PredictionSchema, SymptomsSchema
from .services.strategies import DiagnosisPredictionStrategy

ml_router = Router()
prediction_strategy = DiagnosisPredictionStrategy()


@ml_router.post('/predict', response=PredictionSchema)
def predict_disease(request, payload: SymptomsSchema):
    input_data = {'symptoms': payload.symptoms}
    predictions = prediction_strategy.predict(input_data)

    return {'predictions': predictions}


@ml_router.get('/train')
def train_model(request):
    from .ml_models.diagnosis_model import DiagnosisModel
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'symbipredict_2022.csv')

    diagnosis_model = DiagnosisModel(data_path)
    diagnosis_model.train_model()
    return {'message': 'Model trained successfully'}
