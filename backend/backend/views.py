from ninja import Router

from .api.services import get_ml_diseases, get_ml_symptoms
from .schemas import SymptomsListSchema, DiseasesListSchema, ErrorResponseSchema

main_router = Router(tags=["Main"])


@main_router.get("/symptoms", response={200: SymptomsListSchema, 400: ErrorResponseSchema})
def get_symptoms_list(request):
    try:
        symptoms = get_ml_symptoms()
        return 200, {"symptoms": symptoms}
    except Exception as e:
        return 400, {"error": str(e)}


@main_router.get("/diseases", response={200: DiseasesListSchema, 400: ErrorResponseSchema})
def get_diseases_list(request):
    try:
        diseases = get_ml_diseases()
        return 200, {"diseases": diseases}
    except Exception as e:
        return 400, {"error": str(e)}
