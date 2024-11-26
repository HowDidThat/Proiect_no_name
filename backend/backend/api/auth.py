from ninja.security import HttpBearer
from django.conf import settings
import hmac
import hashlib



class ApiAuth(HttpBearer):
    def authenticate(self, request, token):
        print("gggggg", token)
        if not token:
            raise Exception("No authentication token provided")

        return token if self.verify_token(token) else None

    def create_token(self) -> str:
        return f"Bearer {settings.SHARED_SECRET_KEY}"

    def verify_token(self, token: str) -> bool:
        expected = settings.SHARED_SECRET_KEY.encode('utf-8')
        received = token.encode('utf-8')

        return hmac.compare_digest(
            hmac.new(expected, b'', hashlib.sha256).hexdigest(),
            hmac.new(received, b'', hashlib.sha256).hexdigest()
        )