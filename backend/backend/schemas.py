from typing import List

from ninja import Schema


class SymptomsListSchema(Schema):
    symptoms: List[str]


class DiseasesListSchema(Schema):
    diseases: List[str]


class ErrorResponseSchema(Schema):
    error: str
