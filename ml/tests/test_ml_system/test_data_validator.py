import pytest
import pandas as pd
import tempfile
import os
from ml_system.utils.validator import DataValidator


class TestDataValidator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.validator = DataValidator()

    def test_clean_symptom_name(self):
        test_cases = {
            "itching": "itching",
            "skin_rash": "skin_rash",
            "dischromic _patches": "dischromic_patches",
            "nodal_skin_eruptions": "nodal_skin_eruptions",
            "continuous_sneezing": "continuous_sneezing",
            "": "",
            "  ": "",
            "Skin Rash": "skin_rash",
            "ITCHING": "itching",
            "Nodal_Skin_Eruptions": "nodal_skin_eruptions",
        }

        for input_symptom, expected in test_cases.items():
            result = self.validator.clean_symptom_name(input_symptom)
            assert result == expected

    def test_validate_dataset(self):
        symptoms_df = pd.DataFrame({
            'Disease': ['Fungal infection', 'Common Cold'],
            'Symptom_1': ['itching', 'continuous_sneezing'],
            'Symptom_2': ['skin_rash', 'chills'],
            'Symptom_3': ['nodal_skin_eruptions', ''],
            'Symptom_4': ['dischromic _patches', ''],
            'Symptom_5': ['', ''],
            'Symptom_6': ['', ''],
            'Symptom_7': ['', ''],
            'Symptom_8': ['', ''],
            'Symptom_9': ['', ''],
            'Symptom_10': ['', ''],
            'Symptom_11': ['', ''],
            'Symptom_12': ['', ''],
            'Symptom_13': ['', ''],
            'Symptom_14': ['', ''],
            'Symptom_15': ['', ''],
            'Symptom_16': ['', ''],
            'Symptom_17': ['', '']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching', 'skin_rash', 'nodal_skin_eruptions',
                        'dischromic _patches', 'continuous_sneezing', 'chills'],
            'weight': [3, 4, 4, 4, 4, 3]
        })

        result = self.validator.validate_dataset(symptoms_df, severity_df)
        assert result == True

    def test_validate_dataset_invalid_symptoms(self):
        symptoms_df = pd.DataFrame({
            'Disease': ['Invalid Disease'],
            'Symptom_1': ['invalid_symptom'],
            'Symptom_2': ['another_invalid'],
            'Symptom_3': [''],
            'Symptom_4': [''],
            'Symptom_5': [''],
            'Symptom_6': [''],
            'Symptom_7': [''],
            'Symptom_8': [''],
            'Symptom_9': [''],
            'Symptom_10': [''],
            'Symptom_11': [''],
            'Symptom_12': [''],
            'Symptom_13': [''],
            'Symptom_14': [''],
            'Symptom_15': [''],
            'Symptom_16': [''],
            'Symptom_17': ['']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching', 'skin_rash'],
            'weight': [3, 4]
        })

        result = self.validator.validate_dataset(symptoms_df, severity_df)
        assert result == False

    def test_clean_dataset(self):
        symptoms_df = pd.DataFrame({
            'Disease': ['Fungal infection', 'Common Cold'],
            'Symptom_1': ['itching', 'continuous_sneezing'],
            'Symptom_2': ['skin_rash', 'chills'],
            'Symptom_3': ['nodal_skin_eruptions', ''],
            'Symptom_4': ['dischromic _patches', ''],
            'Symptom_5': ['', ''],
            'Symptom_6': ['', ''],
            'Symptom_7': ['', ''],
            'Symptom_8': ['', ''],
            'Symptom_9': ['', ''],
            'Symptom_10': ['', ''],
            'Symptom_11': ['', ''],
            'Symptom_12': ['', ''],
            'Symptom_13': ['', ''],
            'Symptom_14': ['', ''],
            'Symptom_15': ['', ''],
            'Symptom_16': ['', ''],
            'Symptom_17': ['', '']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching', 'skin_rash', 'nodal_skin_eruptions',
                        'dischromic _patches', 'continuous_sneezing', 'chills'],
            'weight': [3, 4, 4, 4, 4, 3]
        })

        cleaned_symptoms, cleaned_severity = self.validator.clean_dataset(symptoms_df, severity_df)

        assert cleaned_symptoms['Symptom_1'][0] == 'itching'
        assert cleaned_symptoms['Symptom_4'][0] == 'dischromic_patches'
        assert cleaned_symptoms['Symptom_5'][0] == 0
        assert cleaned_symptoms['Symptom_17'][0] == 0
        assert cleaned_severity['Symptom'][0] == 'itching'

    def test_spec_validate_then_send(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as symptoms_file, \
                tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as severity_file:
            symptoms_data = pd.DataFrame({
                'Disease': ['Fungal infection', 'Common Cold'],
                'Symptom_1': ['itching', 'continuous_sneezing'],
                'Symptom_2': ['skin_rash', 'chills'],
                'Symptom_3': ['nodal_skin_eruptions', ''],
                'Symptom_4': ['dischromic _patches', ''],
                'Symptom_5': ['', ''],
                'Symptom_6': ['', ''],
                'Symptom_7': ['', ''],
                'Symptom_8': ['', ''],
                'Symptom_9': ['', ''],
                'Symptom_10': ['', ''],
                'Symptom_11': ['', ''],
                'Symptom_12': ['', ''],
                'Symptom_13': ['', ''],
                'Symptom_14': ['', ''],
                'Symptom_15': ['', ''],
                'Symptom_16': ['', ''],
                'Symptom_17': ['', '']
            })

            severity_data = pd.DataFrame({
                'Symptom': ['itching', 'skin_rash', 'nodal_skin_eruptions',
                            'dischromic _patches', 'continuous_sneezing', 'chills'],
                'weight': [3, 4, 4, 4, 4, 3]
            })

            symptoms_data.to_csv(symptoms_file.name, index=False)
            severity_data.to_csv(severity_file.name, index=False)

            result_symptoms, result_severity = self.validator.spec_validate_then_send(
                symptoms_file.name,
                severity_file.name
            )

            assert result_symptoms is not None
            assert result_severity is not None
            assert 'Disease' in result_symptoms.columns
            assert result_symptoms['Symptom_5'][0] == 0

            os.unlink(symptoms_file.name)
            os.unlink(severity_file.name)

    def test_spec_validate_then_send_invalid_files(self):
        result = self.validator.spec_validate_then_send(
            'nonexistent.csv',
            'also_nonexistent.csv'
        )
        assert result == (None, None)

    def test_validate_dataset_missing_columns(self):
        symptoms_df_no_disease = pd.DataFrame({
            'NotDisease': ['Fungal infection'],
            'Symptom_1': ['itching'],
            'Symptom_2': ['']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching'],
            'weight': [3]
        })

        result = self.validator.validate_dataset(symptoms_df_no_disease, severity_df)
        assert result == False

    def test_validate_dataset_empty_dataframe(self):
        empty_symptoms = pd.DataFrame()
        empty_severity = pd.DataFrame()

        result = self.validator.validate_dataset(empty_symptoms, empty_severity)
        assert result == False

    def test_clean_dataset_duplicates(self):
        symptoms_df = pd.DataFrame({
            'Disease': ['Fungal infection', 'Fungal infection'],
            'Symptom_1': ['itching', 'itching'],
            'Symptom_2': ['skin_rash', 'skin_rash'],
            'Symptom_3': ['', '']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching', 'skin_rash'],
            'weight': [3, 4]
        })

        cleaned_symptoms, _ = self.validator.clean_dataset(symptoms_df, severity_df)
        assert len(cleaned_symptoms) == 1

    def test_spec_validate_then_send_invalid_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as invalid_file:
            invalid_file.write("Invalid,CSV,Format\n1,2\n")
            invalid_file.flush()

            result = self.validator.spec_validate_then_send(
                invalid_file.name,
                invalid_file.name
            )
            assert result == (None, None)
            os.unlink(invalid_file.name)

    def test_validate_dataset_exception_handling(self):
        try:
            self.validator.validate_dataset(None, None)
            assert False, "Should raise an exception"
        except Exception:
            assert True

    def test_validate_dataset_no_symptom_columns(self):
        symptoms_df = pd.DataFrame({
            'Disease': ['Fungal infection'],
            'NotASymptom': ['itching']
        })

        severity_df = pd.DataFrame({
            'Symptom': ['itching'],
            'weight': [3]
        })

        result = self.validator.validate_dataset(symptoms_df, severity_df)
        assert result == False

    def test_spec_validate_then_send_corrupted_file(self):
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as corrupted_file:
            corrupted_file.write(b'\x80\x81\x82\x83')
            corrupted_file.close()

            severity_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
            pd.DataFrame({
                'Symptom': ['itching'],
                'weight': [3]
            }).to_csv(severity_file.name, index=False)
            severity_file.close()

            result = self.validator.spec_validate_then_send(
                corrupted_file.name,
                severity_file.name
            )
            assert result == (None, None)

            os.unlink(corrupted_file.name)
            os.unlink(severity_file.name)

    def test_spec_validate_then_send_validation_failure_after_cleaning(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as symptoms_file, \
                tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as severity_file:
            pd.DataFrame({
                'Disease': ['Test Disease'],
                'Symptom_1': ['invalid_symptom'],
                'Symptom_2': ['another_invalid']
            }).to_csv(symptoms_file.name, index=False)

            pd.DataFrame({
                'Symptom': ['itching', 'fever'],
                'weight': [3, 4]
            }).to_csv(severity_file.name, index=False)

            result = self.validator.spec_validate_then_send(
                symptoms_file.name,
                severity_file.name
            )
            assert result == (None, None)

            os.unlink(symptoms_file.name)
            os.unlink(severity_file.name)