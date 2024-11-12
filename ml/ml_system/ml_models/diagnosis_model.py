import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

class DiagnosisModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.label_encoder = None
        self.all_symptoms = None

    def load_and_preprocess_data(self):
        data = pd.read_csv(self.data_path)
        X = data.drop('prognosis', axis=1)
        y = data['prognosis']
        self.all_symptoms = X.columns.tolist()
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_model(self):
        X_train, X_test, y_train, y_test = self.load_and_preprocess_data()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'saved_models')

        joblib.dump(self.model, os.path.join(data_path,'diagnosis_model.joblib'))
        joblib.dump(self.label_encoder, os.path.join(data_path,'label_encoder.joblib'))

        joblib.dump(self.all_symptoms, os.path.join(data_path,'all_symptoms.joblib'))
