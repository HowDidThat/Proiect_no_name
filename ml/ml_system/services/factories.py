from abc import ABC, abstractmethod
from sklearn.tree import DecisionTreeClassifier  # pentru ID3
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier


class ModelInterface(ABC):
    @abstractmethod
    def get_model(self):
        pass


class RandomForestEntropyModel(ModelInterface):
    def get_model(self):
        return RandomForestClassifier(
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


class RandomForestGiniModel(ModelInterface):
    def get_model(self):
        return RandomForestClassifier(
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
            criterion='gini'
        )


class ID3Model(ModelInterface):
    def get_model(self):
        return DecisionTreeClassifier(
            criterion='entropy',  # ID3 folosește entropy
            random_state=42,
            class_weight='balanced'
        )



class KNNModel(ModelInterface):
    def get_model(self):
        return KNeighborsClassifier(n_neighbors=5)


class ModelFactory:
    @staticmethod
    def get_model(model_type: str) -> ModelInterface:
        models = {
            'rf_entropy': RandomForestEntropyModel(),
            'rf_gini': RandomForestGiniModel(),
            'id3': ID3Model(),
            'knn': KNNModel()
        }

        if model_type not in models:
            raise ValueError(f"Model type {model_type} not supported. Choose from: {list(models.keys())}")

        return models[model_type].get_model()
