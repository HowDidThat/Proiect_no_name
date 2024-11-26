import requests
from django.conf import settings

from .auth import ApiAuth
auth = ApiAuth()

def get_ml_prediction(symptoms: list) -> dict:
    try:

        response = requests.post(
            f"{settings.ML_API_URL}/predict",
            json={'symptoms': symptoms},
            headers={
                'Authorization': auth.create_token(),
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        return response.json()
    except requests.RequestException:
        return None
