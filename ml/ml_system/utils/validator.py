import os
import time
import logging
from typing import Tuple, Dict, Any, List, Optional
from datetime import datetime

import pandas as pd


class DataValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validated_files = {}

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('data_validation.log', mode='w')
        file_handler.setFormatter(formatter)

        self.logger.handlers = []
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def clean_symptom_name(self, symptom: str) -> str:
        if pd.isna(symptom) or not str(symptom).strip():
            return ''

        cleaned = str(symptom).lower().strip()

        replacements = {
            ' ': '_',
            '__': '_',
            ' _': '_',
            '_ ': '_',
        }

        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)

        return cleaned.strip('_')

    def validate_dataset(self, symptoms_df: pd.DataFrame, severity_df: pd.DataFrame) -> bool:
        try:
            self.logger.info("=== Start dataset validation ===")

            if 'Disease' not in symptoms_df.columns:
                self.logger.error("Validation failed: 'Disease' column is missing in the symptoms dataset")
                return False
            else:
                self.logger.info("'Disease' column exists")

            symptom_columns = [col for col in symptoms_df.columns if col.startswith('Symptom_')]
            if not symptom_columns:
                self.logger.error("Validation failed: No columns starting with 'Symptom_' found")
                return False
            else:
                self.logger.info(f"Symptom columns found: {symptom_columns}")

            valid_symptoms = set(severity_df['Symptom'].apply(self.clean_symptom_name))
            self.logger.info(f"Valid symptoms from severity: {valid_symptoms}")

            invalid_symptoms = set()
            for col in symptom_columns:
                symptoms = symptoms_df[col].dropna().unique()
                for symptom in symptoms:
                    if symptom and self.clean_symptom_name(symptom) not in valid_symptoms:
                        invalid_symptoms.add(symptom)

            if invalid_symptoms:
                self.logger.error(
                    f"Validation failed: Invalid symptoms found not present in severity dataset: {sorted(invalid_symptoms)}")
                return False
            else:
                self.logger.info("All symptoms in the dataset are present in the severity dataset")

            self.logger.info("=== Dataset validation successful ===")
            return True

        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}", exc_info=True)
            return False

    def clean_dataset(self, symptoms_df: pd.DataFrame, severity_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.logger.info("=== Start dataset cleaning ===")

        symptoms_df = symptoms_df.copy()
        severity_df = severity_df.copy()

        self.logger.info("Cleaning symptom names in severity dataset...")
        severity_df['Symptom'] = severity_df['Symptom'].apply(self.clean_symptom_name)
        self.logger.info("Symptom names in severity dataset have been cleaned successfully")

        symptom_columns = [col for col in symptoms_df.columns if col.startswith('Symptom_')]

        self.logger.info("Replacing missing values with empty strings in symptoms dataset...")
        symptoms_df[symptom_columns] = symptoms_df[symptom_columns].fillna('')
        self.logger.info("Missing values have been replaced with empty strings")

        def log_symptom_diff(original_symptom: str) -> str:
            cleaned_symptom = self.clean_symptom_name(original_symptom)
            if cleaned_symptom != original_symptom.strip():
                self.logger.info(f"Symptom changed from '{original_symptom.strip()}' to '{cleaned_symptom}'")
            return cleaned_symptom

        self.logger.info("Cleaning symptom names in the symptoms dataset, logging differences...")
        for col in symptom_columns:
            symptoms_df[col] = symptoms_df[col].apply(log_symptom_diff)

        self.logger.info("Replacing empty strings with 0 in symptoms dataset...")
        symptoms_df[symptom_columns] = symptoms_df[symptom_columns].replace('', 0)
        self.logger.info("Empty strings have been replaced with 0")

        self.logger.info("Checking for duplicate rows in the symptoms dataset (considering 'Disease' and symptoms)...")
        initial_count = symptoms_df.shape[0]
        subset_columns = ['Disease'] + symptom_columns

        duplicates_mask = symptoms_df.duplicated(subset=subset_columns, keep=False)
        if duplicates_mask.any():
            duplicate_rows = symptoms_df[duplicates_mask].copy()
            duplicate_rows = duplicate_rows.reset_index(drop=True)
            duplicate_rows.insert(0, 'RowNumber', duplicate_rows.index + 1)
        else:
            self.logger.info("No duplicates found before removal")

        symptoms_df = symptoms_df.drop_duplicates(subset=subset_columns, keep='first')
        final_count = symptoms_df.shape[0]
        duplicates_removed = initial_count - final_count

        if duplicates_removed > 0:
            self.logger.info(
                f"{duplicates_removed} duplicate rows have been removed. Total rows remaining: {final_count}")
        else:
            self.logger.info("No duplicate rows were removed. The dataset is unique")

        self.logger.info("=== Cleaning completed successfully ===")
        return symptoms_df, severity_df


    def spec_validate_then_send(self, symptoms_path: str, severity_path: str) -> Tuple[
        Optional[pd.DataFrame], Optional[pd.DataFrame]]:

        self.logger.info("=== Start spec_validate_then_send process ===")
        try:
            self.logger.info(f"Symptoms file: {symptoms_path}")
            self.logger.info(f"Severity file: {severity_path}")

            if not os.path.exists(symptoms_path) or not os.path.exists(severity_path):
                self.logger.error("One or both files do not exist. Operation cannot continue")
                return None, None
            else:
                self.logger.info("Files exist. Continuing...")

            try:
                symptoms_df = pd.read_csv(symptoms_path)
                severity_df = pd.read_csv(severity_path)
                self.logger.info(
                    f"Data loaded successfully: symptoms_df: {symptoms_df.shape}, severity_df: {severity_df.shape}")
            except Exception as e:
                self.logger.error(f"Error loading files: {str(e)}", exc_info=True)
                return None, None

            self.logger.info("Cleaning the datasets before validation...")
            cleaned_symptoms_df, cleaned_severity_df = self.clean_dataset(symptoms_df, severity_df)
            self.logger.info("Datasets have been cleaned successfully")

            self.logger.info("Validating datasets after cleaning...")
            if not self.validate_dataset(cleaned_symptoms_df, cleaned_severity_df):
                self.logger.error("Validation failed after cleaning. Stopping the operation")
                return None, None
            else:
                self.logger.info("Validation succeeded after cleaning")

            self.validated_files[symptoms_path] = datetime.now()
            self.validated_files[severity_path] = datetime.now()
            self.logger.info("Files have been marked as validated")

            self.logger.info("=== spec_validate_then_send process completed successfully ===")
            return cleaned_symptoms_df, cleaned_severity_df

        except Exception as e:
            self.logger.error(f"Error in validation process: {str(e)}", exc_info=True)
            return None, None
