from typing import List, Tuple, Optional, Set, Dict
import pandas as pd
from .data_validator import DataValidator


class DataLoader:
    def __init__(self, data_path: str, severity_path: str):
        self.data_path = data_path
        self.severity_path = severity_path
        self.validator = DataValidator()
        print(self.data_path, self.severity_path)

    def extract_unique_symptoms(self, df: pd.DataFrame) -> List[str]:
        symptom_columns = [col for col in df.columns if col.startswith('Symptom_')]

        all_unique_symptoms: Set[str] = set()
        for col in symptom_columns:
            all_unique_symptoms.update(df[col].unique())

        all_unique_symptoms.discard(0)
        all_unique_symptoms.discard('')

        return sorted(list(all_unique_symptoms))

    def format_text(self, text: str) -> str:
        return ' '.join(word.capitalize() for word in text.replace('_', ' ').split())

    def create_formatted_dict(self, items: List[str]) -> Dict[str, str]:
        return {item: self.format_text(item) for item in items}

    def load_and_validate_data(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        cleaned_symptoms_df, cleaned_severity_df = self.validator.spec_validate_then_send(
            self.data_path, self.severity_path
        )
        if cleaned_symptoms_df is None or cleaned_severity_df is None:
            raise ValueError("Failed to load and validate data")

        all_symptoms = self.extract_unique_symptoms(cleaned_symptoms_df)
        all_diseases = list(cleaned_symptoms_df['Disease'].unique())

        symptoms_dict = self.create_formatted_dict(all_symptoms)
        diseases_dict = self.create_formatted_dict(all_diseases)

        return symptoms_dict, diseases_dict
