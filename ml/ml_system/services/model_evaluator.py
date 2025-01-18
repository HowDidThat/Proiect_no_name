import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List, Dict


class ModelEvaluator:
    def __init__(self):
        self.results = {}

    def add_model_results(self, model_type: str, metrics: Dict):
        self.results[model_type] = metrics

    def compare_accuracies(self):
        accuracies = {
            model_type: {
                'Test Accuracy': results['test_accuracy'],
                'Train Accuracy': results['train_accuracy']
            }
            for model_type, results in self.results.items()
        }

        df = pd.DataFrame(accuracies).T

        plt.figure(figsize=(10, 6))
        df.plot(kind='bar')
        plt.title('Model Accuracy Comparison')
        plt.ylabel('Accuracy Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return df

    def print_summary_table(self):
        summary = {
            model_type: {
                'Train Accuracy': f"{results['train_accuracy']:.4f}",  # Adăugăm Train Accuracy

                'Test Accuracy': f"{results['test_accuracy']:.4f}",
                'Training Time': f"{results['training_time']:.2f}s",
                'CV Score': f"{results['cv_scores_mean']:.4f} (±{results['cv_scores_std']:.4f})",
                'ROC AUC': f"{results['roc_auc_score']:.4f}"
            }
            for model_type, results in self.results.items()
        }

        return pd.DataFrame(summary).T

    def plot_feature_importance(self, model_type: str):
        if model_type not in self.results or 'top_features' not in self.results[model_type]:
            print(f"Feature importance not available for {model_type}")
            return

        features = self.results[model_type]['top_features']

        plt.figure(figsize=(10, 6))
        plt.bar(
            [f['feature'] for f in features],
            [f['importance'] for f in features]
        )
        plt.xticks(rotation=45)
        plt.title(f'Top Features Importance - {model_type}')
        plt.tight_layout()
        plt.show()
