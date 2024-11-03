from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from ninja import Router
from ninja.security import HttpBearer

from .models import User
from .schemas import LoginSchema, TokenSchema, UserSchema, ErrorSchema

auth_router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            request.user = user
            return token
        except (jwt.PyJWTError, User.DoesNotExist):
            return None


def create_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


@auth_router.post("/login", response={200: TokenSchema, 401: ErrorSchema})
def login(request, credentials: LoginSchema):
    user = authenticate(
        username=credentials.username,
        password=credentials.password
    )

    if user is None:
        return 401, {"message": "Invalid credentials"}

    token = create_token(user.id)
    return 200, {"token": token}


@auth_router.get("/me", response=UserSchema, auth=AuthBearer())
def get_current_user(request):
    return request.user
