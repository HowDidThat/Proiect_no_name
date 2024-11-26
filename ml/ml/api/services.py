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

        return response.json()
    except requests.RequestException:
        return None