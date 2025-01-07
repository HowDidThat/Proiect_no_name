from ninja import Schema
from typing import List, Dict

class SymptomsSchema(Schema):
    symptoms: List[str]

class PredictionSchema(Schema):
    predictions: Dict[str, float]

class SymptomsListSchema(Schema):
    symptoms: Dict[str, str]

class DiseasesListSchema(Schema):
    diseases: Dict[str, str]
