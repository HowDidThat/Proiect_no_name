from ninja import Router
from typing import List
router = Router()

@router.post("/predict/diagnosis")
def predict_diagnosis(request, symptoms: List[str]):
    pass

@router.post("/predict/symptoms")
def predict_symptoms(request, diagnosis: str):
    pass

@router.post("/compute-similarity")
def compute_answer_similarity(request, user_answer: str, reference_symptom: str):
    pass