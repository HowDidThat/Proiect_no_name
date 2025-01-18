import os
import joblib
from typing import Any, Dict


class ModelRepository:
    def __init__(self, storage_path: str, joblib_path: str):
        self.storage_path = storage_path
        self.joblib_path = joblib_path
        self.model_cache = {}
        self.joblib_cache = {}

    def clean_directories(self):
        for file in os.listdir(self.storage_path):
            file_path = os.path.join(self.storage_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Error: {e}')

        for file in os.listdir(self.joblib_path):
            file_path = os.path.join(self.joblib_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Error: {e}')

    def get_model(self, model_id: str) -> Any:
        if model_id not in self.model_cache:
            model_path = os.path.join(self.storage_path, f"{model_id}.joblib")
            self.model_cache[model_id] = joblib.load(model_path)
        return self.model_cache[model_id]

    def save_model(self, model_id: str, model: Any) -> None:
        self.clean_directories()
        model_path = os.path.join(self.storage_path, f"{model_id}.joblib")
        joblib.dump(model, model_path)
        self.model_cache[model_id] = model

    def get_joblib(self, joblib_id: str) -> Any:
        if joblib_id not in self.joblib_cache:
            joblib_path = os.path.join(self.joblib_path, f"{joblib_id}.joblib")
            self.joblib_cache[joblib_id] = joblib.load(joblib_path)
        return self.joblib_cache[joblib_id]

    def save_joblib(self, joblib_id: str, data: Any) -> None:
        joblib_path = os.path.join(self.joblib_path, f"{joblib_id}.joblib")
        joblib.dump(data, joblib_path)
        self.joblib_cache[joblib_id] = data
