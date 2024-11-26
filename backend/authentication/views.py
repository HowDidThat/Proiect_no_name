# views.py
import json
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse
from ninja import Router
from ninja.security import HttpBearer

from .models import User
from .schemas import (
    LoginSchema, UserSchema, ErrorSchema, RegisterSchema,
    MessageSchema, ValidationErrorResponse
)

auth_router = Router(tags=['Authentication'])


def set_auth_cookies(response: HttpResponse, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        'access_token',
        access_token,
        httponly=True,
        secure=True,
        #samesite='Lax',
        max_age=900,
        samesite='None',
        path='/',
        
    )
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        secure=True,
        #samesite='Lax',
        max_age=8640,
        samesite='None',
        path='/',
        
    
    )


def create_tokens(user_id: int) -> tuple[str, str]:
    access_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
        'type': 'access'
    }

    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token, refresh_token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            if not token:
                token = request.COOKIES.get('access_token')

            if not token:
                return None

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            request.user = user
            return token
        except (jwt.PyJWTError, User.DoesNotExist):
            return None


@auth_router.post("/register", response={201: MessageSchema, 400: ValidationErrorResponse})
def register(request, data: RegisterSchema):
    errors = []

    try:
        data.validate_all()
    except ValueError as e:
        if isinstance(e.args[0], list):
            errors.extend(e.args[0])
        else:
            message = str(e)
            if ': ' in message:
                field, msg = message.split(': ', 1)
                errors.append({"field": field, "message": msg})
            else:
                errors.append({"field": "general", "message": message})
        return 400, {"errors": errors}

    if User.objects.filter(username=data.username).exists():
        errors.append({"field": "username", "message": "Username already exists"})

    if User.objects.filter(email=data.email).exists():
        errors.append({"field": "email", "message": "Email already exists"})

    if errors:
        return 400, {"errors": errors}

    try:
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            institution=data.institution,
            year_of_study=data.year_of_study
        )
        access_token, refresh_token = create_tokens(user.id)
        response = HttpResponse(
            json.dumps({"message": "Registration successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token}),
            content_type='application/json',
            status=201
        )
        set_auth_cookies(response, access_token, refresh_token)
        
        return response

    except Exception as e:
        errors.append({"field": "general", "message": str(e)})
        return 400, {"errors": errors}


@auth_router.post("/login", response={200: MessageSchema, 401: ErrorSchema})
def login(request, credentials: LoginSchema):
    user = authenticate(
        username=credentials.username,
        password=credentials.password
    )

    if user is None:
        return 401, {"message": "Invalid credentials"}

    access_token, refresh_token = create_tokens(user.id)
    response = HttpResponse(
        json.dumps({"message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token}),
        content_type='application/json',
        status=200
    )
    set_auth_cookies(response, access_token, refresh_token)
    return response


@auth_router.post("/refresh", response={200: MessageSchema, 401: ErrorSchema})
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            refresh_token = auth_header.split(' ')[1]

    if not refresh_token:
        return 401, {"message": "Refresh token required"}

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload.get('type') != 'refresh':
            return 401, {"message": "Invalid token type"}

        user_id = payload.get('user_id')
        new_access_token, new_refresh_token = create_tokens(user_id)
        response = HttpResponse(
            json.dumps({"message": "Tokens refreshed"}),
            content_type='application/json',
            status=200
        )
        set_auth_cookies(response, new_access_token, new_refresh_token)
        return response

    except jwt.ExpiredSignatureError:
        return 401, {"message": "Refresh token expired"}
    except jwt.InvalidTokenError:
        return 401, {"message": "Invalid refresh token"}


@auth_router.post("/logout", response={200: MessageSchema})
def logout(request):
    response = HttpResponse(
        json.dumps({"message": "Logout successful"}),
        content_type='application/json',
        status=200
    )
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    return response


@auth_router.get("/me", response=UserSchema, auth=AuthBearer())
def get_current_user(request):
    return request.user
