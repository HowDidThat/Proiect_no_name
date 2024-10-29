from typing import Any, Dict


class ModelRepository:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.model_cache = {}

    def get_model(self, model_id: str) -> Any:
        pass

    def save_model(self, model_id: str, model: Any) -> None:
        pass

    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        pass