import hashlib
import hmac

from django.conf import settings
from ninja.security import HttpBearer


class ApiAuth(HttpBearer):

    def authenticate(self, request, token):
        if not token:
            raise Exception("No authentication token provided")

        return token if self.verify_token(token) else None

    @staticmethod
    def create_token() -> str:
        return f"Bearer {settings.SHARED_SECRET_KEY}"

    @staticmethod
    def verify_token(token: str) -> bool:
        expected = settings.SHARED_SECRET_KEY.encode('utf-8')
        received = token.encode('utf-8')

        return hmac.compare_digest(
            hmac.new(expected, b'', hashlib.sha256).hexdigest(),
            hmac.new(received, b'', hashlib.sha256).hexdigest()
        )
