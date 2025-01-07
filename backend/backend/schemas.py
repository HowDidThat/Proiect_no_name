from typing import Dict

from ninja import Schema


class SymptomsListSchema(Schema):
    symptoms: Dict[str, str]

class DiseasesListSchema(Schema):
    diseases: Dict[str, str]


class ErrorResponseSchema(Schema):
    error: str
