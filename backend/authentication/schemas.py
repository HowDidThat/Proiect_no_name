from ninja import Schema
from typing import Optional


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    token: str


class UserSchema(Schema):
    id: int
    username: str
    email: str
    institution: str
    year_of_study: int


class ErrorSchema(Schema):
    message: str
