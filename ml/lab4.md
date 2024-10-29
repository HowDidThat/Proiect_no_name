# Machine Learning Component

This machine learning component was developed as a dedicated module within the Django backend, following a Service-Oriented Architecture (SOA) integrated with Django's MTV (Model-Template-View) structure. The system is organized with a distinct service layer to handle machine learning logic, making use of design patterns for modularity and scalability.
## Design Patterns Implementation in ML System

### 1. Strategy

Used to encapsulate different prediction algorithms, allowing runtime switching between diagnosis prediction, symptom
prediction, and semantic similarity comparison strategies.

**Location**: `ml/services/strategies.py`

- `PredictionStrategy` (abstract base)
- `DiagnosisPredictionStrategy`, `SymptomPredictionStrategy`, `SemanticSimilarityStrategy` (concrete implementations)

### 2. Factory

Provides specialized factories for creating diagnosis and symptom prediction components independently, allowing the
system to create different types of predictive models with their specific configurations.

**Location**: `ml/services/factories.py`

- `ModelFactory` (abstract base)
- `DiagnosisModelFactory`, `SymptomModelFactory`, `ImageModelFactory` (concrete implementations)

### 3. Adapter

Adapts different pre-trained models (BERT, GPT) to a common interface, allowing usage of different models without
modifying the using code.

**Location**: `ml/services/adapters.py`

- `PreTrainedModelAdapter` (abstract base)
- `BERTModelAdapter`, `GPTModelAdapter` (concrete implementations)

### 4. Observer

Monitors model performance and behavior, with observers automatically notified when new predictions are made.

**Location**: `ml/services/monitors.py`

- `ModelMonitor` (abstract base)
- `PredictionMonitor`, `PerformanceMonitor` (concrete implementations)

### 5. Template Method

Defines the skeleton of ML processing algorithm in a method, letting subclasses override specific
steps while maintaining the overall structure.

**Location**: `ml/services/pipeline.py`

- `MLPipeline` (abstract base)
- `DiagnosisPipeline`, `SymptomPipeline` (concrete implementations)

### 6. Repository

Abstracts model storage and loading operations, providing a unified interface for accessing models
regardless of storage location.

**Location**: `ml/services/repository.py`

- `ModelRepository`

### 7. Singleton

Ensures a single instance of the repository exists throughout the application, managing centralized
access to ML models.

**Location**: `ml/services/repository.py` (within ModelRepository)

## Pattern Relationships

1. **Factory → Strategy**
    - Factory creates different prediction strategies

2. **Strategy → Pipeline**
    - Pipeline uses strategies for making predictions

3. **Adapter → Repository**
    - Repository uses adapters for loading different types of models

4. **Observer → Strategy**
    - Observers monitor the performance of prediction strategies
