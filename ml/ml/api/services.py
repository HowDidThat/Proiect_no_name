import requests
from django.conf import settings
from .auth import ApiAuth

auth = ApiAuth()


def send_to_backend(quiz_id: int, predictions: dict) -> dict:
    try:
        response = requests.post(
            f"{settings.BACKEND_API_URL}/quiz/{quiz_id}",
            json={'predictions': predictions},
            headers={
                'Authorization': auth.create_token(),
                'Content-Type': 'application/json'
            },
            timeout=10
        )

        try:
            return response.json()
        except ValueError:
            return None

    except requests.RequestException:
        return None


def send_symptoms_to_backend() -> list:
    try:
        response = requests.get(
            f"{settings.BACKEND_API_URL}/symptoms",
            headers={
                'Authorization': auth.create_token(),
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        return response.json().get('symptoms', [])
    except requests.RequestException:
        return []

def send_diseases_to_backend() -> list:
    try:
        response = requests.get(
            f"{settings.BACKEND_API_URL}/diseases",
            headers={
                'Authorization': auth.create_token(),
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        return response.json().get('diseases', [])
    except requests.RequestException:
        return []