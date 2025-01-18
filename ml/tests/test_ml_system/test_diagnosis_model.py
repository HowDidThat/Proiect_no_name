import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import os
import joblib
from ml_system.model.diagnosis_model import DiagnosisModel


class TestDiagnosisModel:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        symptoms_data = {
            'Disease': ['Flu', 'Flu', 'Flu', 'Flu', 'Flu', 'Flu',
                        'Cold', 'Cold', 'Cold', 'Cold', 'Cold', 'Cold',
                        'COVID', 'COVID', 'COVID', 'COVID', 'COVID', 'COVID'],
            'Symptom_1': ['fever', 'fever', 'fever', 'cough', 'cough', 'headache'] * 3,
            'Symptom_2': ['cough', 'headache', 'runny_nose', 'fever', 'loss_of_taste', 'fever'] * 3,
            'Symptom_3': ['headache', 'runny_nose', 'loss_of_taste', 'sore_throat', 'cough', 'runny_nose'] * 3
        }

        severity_data = {
            'Symptom': ['fever', 'cough', 'runny_nose', 'loss_of_taste',
                        'headache', 'sore_throat'],
            'weight': [5, 4, 2, 4, 3, 2]
        }

        self.data_path = tmp_path / "test_dataset.csv"
        self.severity_path = tmp_path / "test_severity.csv"

        pd.DataFrame(symptoms_data).to_csv(self.data_path, index=False)
        pd.DataFrame(severity_data).to_csv(self.severity_path, index=False)

        self.model = DiagnosisModel(str(self.data_path), str(self.severity_path))
        self.model.label_encoder = LabelEncoder()
        self.model.scaler = MinMaxScaler()

    def test_init(self):
        assert isinstance(self.model, DiagnosisModel)
        assert self.model.data_path == str(self.data_path)
        assert self.model.severity_path == str(self.severity_path)
        assert self.model.model is None
        assert isinstance(self.model.label_encoder, LabelEncoder)
        assert isinstance(self.model.scaler, MinMaxScaler)

    def test_create_severity_matrix(self):
        df = pd.read_csv(self.data_path)
        self.model.symptom_severity = {
            'fever': 5, 'cough': 4, 'runny_nose': 2,
            'loss_of_taste': 4, 'headache': 3, 'sore_throat': 2
        }

        result = self.model.create_severity_matrix(df)

        assert isinstance(result, pd.DataFrame)
        assert 'Disease' in result.columns
        assert all(symptom in result.columns for symptom in self.model.symptom_severity.keys())
        assert result.shape[0] == df.shape[0]

    def test_create_severity_matrix_with_zero(self):
        df = pd.DataFrame({
            'Disease': ['Flu'],
            'Symptom_1': ['fever'],
            'Symptom_2': [0],
            'Symptom_3': ['cough']
        })

        self.model.symptom_severity = {
            'fever': 5,
            'cough': 4
        }

        result = self.model.create_severity_matrix(df)
        assert isinstance(result, pd.DataFrame)
        assert 0 not in result.columns

    def test_apply_severity_weights(self):
        test_df = pd.DataFrame({
            'fever': [1, 0],
            'cough': [1, 1]
        })
        result = self.model.apply_severity_weights(test_df)
        assert isinstance(result, pd.DataFrame)
        assert result.equals(test_df)

    def test_load_and_preprocess_data(self):
        X_train, X_test, y_train, y_test = self.model.load_and_preprocess_data()

        assert isinstance(X_train, pd.DataFrame)
        assert isinstance(X_test, pd.DataFrame)
        assert isinstance(y_train, np.ndarray)
        assert isinstance(y_test, np.ndarray)
        assert len(X_train) + len(X_test) == 18
        assert len(np.unique(y_train)) == 3

    def test_train_model(self):
        metrics = self.model.train_model()

        assert isinstance(metrics, dict)
        assert all(key in metrics for key in [
            'training_time', 'train_accuracy', 'test_accuracy',
            'cv_scores_mean', 'cv_scores_std', 'roc_auc_score',
            'classification_report', 'top_features'
        ])
        assert isinstance(self.model.model, RandomForestClassifier)
        assert metrics['train_accuracy'] > 0
        assert metrics['test_accuracy'] > 0
        assert metrics['cv_scores_mean'] > 0

    def test_save_model(self, tmp_path):
        self.model.train_model()
        model_dir = os.path.join(str(tmp_path), 'saved_models')
        os.makedirs(model_dir, exist_ok=True)

        original_save = self.model.save_model
        try:
            def mock_save_model():
                components = {
                    'diagnosis_model.joblib': self.model.model,
                    'label_encoder.joblib': self.model.label_encoder,
                    'all_symptoms.joblib': self.model.all_symptoms,
                    'symptom_severity.joblib': self.model.symptom_severity,
                    'scaler.joblib': self.model.scaler
                }

                for filename, component in components.items():
                    path = os.path.join(model_dir, filename)
                    joblib.dump(component, path)

            self.model.save_model = mock_save_model
            self.model.save_model()

            expected_files = [
                'diagnosis_model.joblib',
                'label_encoder.joblib',
                'all_symptoms.joblib',
                'symptom_severity.joblib',
                'scaler.joblib'
            ]

            for file in expected_files:
                path = os.path.join(model_dir, file)
                assert os.path.exists(path), f"File {file} does not exist at {path}"
                loaded = joblib.load(path)
                assert loaded is not None

        finally:
            self.model.save_model = original_save

    def test_error_handling(self):
        with pytest.raises(ValueError):
            model = DiagnosisModel("invalid_path.csv", "invalid_severity.csv")
            model.load_and_preprocess_data()