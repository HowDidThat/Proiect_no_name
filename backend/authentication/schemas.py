import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ninja import Schema


class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    institution: str
    year_of_study: int

    @staticmethod
    def validate_username(value: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', value):
            raise ValueError('Username must be 3-30 characters long and contain only letters, numbers, and underscores')
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValueError(e.messages[0])
        return value

    @staticmethod
    def validate_email(value: str) -> str:
        try:
            validate_email(value)
        except ValidationError:
            raise ValueError('Enter a valid email address')
        return value.strip()

    @staticmethod
    def validate_institution(value: str) -> str:
        if len(value.strip()) < 2:
            raise ValueError('Institution name must be at least 2 characters long')
        if len(value) > 255:
            raise ValueError('Institution name is too long')
        return value.strip()

    @staticmethod
    def validate_year_of_study(value: int) -> int:
        if not 1 <= value <= 7:
            raise ValueError('year_of_study: Year of study must be between 1 and 7')
        return value

    def validate_all(self):
        errors = []

        try:
            self.username = self.validate_username(self.username)
        except ValueError as e:
            errors.append({"field": "username", "message": str(e)})

        try:
            self.email = self.validate_email(self.email)
        except ValueError as e:
            errors.append({"field": "email", "message": str(e)})

        try:
            self.password = self.validate_password(self.password)
        except ValueError as e:
            errors.append({"field": "password", "message": str(e)})

        try:
            self.institution = self.validate_institution(self.institution)
        except ValueError as e:
            errors.append({"field": "institution", "message": str(e)})

        try:
            self.year_of_study = self.validate_year_of_study(self.year_of_study)
        except ValueError as e:
            errors.append({
                "field": "year_of_study",
                "message": str(e).split(': ')[1] if ': ' in str(e) else str(e)
            })

        if errors:
            raise ValueError(errors)


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


class ValidationErrorSchema(Schema):
    field: str
    message: str


class ValidationErrorResponse(Schema):
    errors: list[ValidationErrorSchema]


class MessageSchema(Schema):
    message: str
