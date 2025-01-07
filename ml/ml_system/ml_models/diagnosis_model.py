from ..utils.validator import DataValidator

import os
import time
import logging
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib

from ..utils.decorators import log_execution_time


class DiagnosisModel:
    def __init__(self, data_path: str, severity_path: str = None):
        self.data_path = data_path
        self.severity_path = severity_path
        self.model = None
        self.label_encoder = None
        self.all_symptoms = None
        self.symptom_severity = None
        self.scaler = MinMaxScaler()
        self.validator = DataValidator()
        self.logger = logging.getLogger(__name__)

    def create_severity_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        symptom_columns = [col for col in df.columns if col.startswith('Symptom_')]

        all_unique_symptoms = set()
        for col in symptom_columns:
            all_unique_symptoms.update(df[col].unique())
        if 0 in all_unique_symptoms:
            all_unique_symptoms.remove(0)

        all_unique_symptoms = list(all_unique_symptoms)

        symptoms_df = pd.DataFrame(0, index=df.index, columns=all_unique_symptoms)

        for col in symptom_columns:
            for idx, symptom in df[col].items():
                if symptom != 0:
                    severity = self.symptom_severity.get(symptom, 0)
                    symptoms_df.at[idx, symptom] = severity

        df = df.drop(columns=symptom_columns)

        df = pd.concat([df, symptoms_df], axis=1)

        print("DataFrame after severity replacement (first 5 rows):")
        print(df.head())

        self.all_symptoms = all_unique_symptoms

        return df

    def apply_severity_weights(self, X: pd.DataFrame) -> pd.DataFrame:
        return X

    def load_and_preprocess_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
        transformed_df, severity_df = self.validator.spec_validate_then_send(
            self.data_path,
            self.severity_path
        )

        if transformed_df is None:
            raise ValueError("Failed to validate and clean the dataset")

        self.symptom_severity = dict(zip(
            severity_df['Symptom'],
            severity_df['weight']
        ))

        self.diseases = list(transformed_df['Disease'].unique())

        transformed_df = self.create_severity_matrix(transformed_df)

        X = transformed_df.drop('Disease', axis=1)
        y = transformed_df['Disease']

        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)

        X_normalized = pd.DataFrame(
            self.scaler.fit_transform(X),
            columns=X.columns
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X_normalized, y_encoded,
            test_size=0.3,
            random_state=42,
            stratify=y_encoded
        )

        return X_train, X_test, y_train, y_test

    @log_execution_time
    def train_model(self) -> Dict[str, Any]:
        X_train, X_test, y_train, y_test = self.load_and_preprocess_data()

        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            min_samples_split=8,
            min_samples_leaf=3,
            max_features='sqrt',
            class_weight='balanced',
            random_state=42,
            n_jobs=-1,
            bootstrap=True,
            max_samples=0.8,
            criterion='entropy'
        )

        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=cv, scoring='accuracy')

        start_time = time.time()
        self.model.fit(X_train, y_train)
        training_time = time.time() - start_time

        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)

        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        metrics = {
            "training_time": training_time,
            "train_accuracy": accuracy_score(y_train, y_pred_train),
            "test_accuracy": accuracy_score(y_test, y_pred_test),
            "cv_scores_mean": cv_scores.mean(),
            "cv_scores_std": cv_scores.std(),
            "roc_auc_score": roc_auc_score(y_test, y_pred_proba, multi_class='ovr'),
            "classification_report": classification_report(
                y_test, y_pred_test,
                target_names=self.label_encoder.classes_
            ),
            "top_features": feature_importance.head(10).to_dict('records')
        }

        self.logger.info(f"\nTraining Results:")
        self.logger.info(f"Training Time: {training_time:.2f} seconds")
        self.logger.info(f"Train Accuracy: {metrics['train_accuracy']:.4f}")
        self.logger.info(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
        self.logger.info(
            f"Cross-validation Score: {metrics['cv_scores_mean']:.4f} (+/- {metrics['cv_scores_std'] * 2:.4f})")
        self.logger.info(f"ROC AUC Score: {metrics['roc_auc_score']:.4f}")

        self.logger.info("\nTop 10 Most Important Symptoms:")
        for feature in metrics['top_features']:
            self.logger.info(f"- {feature['feature']}: {feature['importance']:.4f}")

        self.save_model()

        return metrics

    def save_model(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, 'saved_models')
        os.makedirs(model_dir, exist_ok=True)

        components = {
            'diagnosis_model.joblib': self.model,
            'label_encoder.joblib': self.label_encoder,
            'all_symptoms.joblib': self.all_symptoms,
            'symptom_severity.joblib': self.symptom_severity,
            'scaler.joblib': self.scaler
        }

        for filename, component in components.items():
            joblib.dump(component, os.path.join(model_dir, filename))
            self.logger.info(f"Saved {filename}")
