
# Design Patterns in Medical Quiz Application

## Core Patterns from Django Ninja (Built-in)

### 1. Decorator Pattern
Used by Django Ninja for route declarations and endpoint definitions
```python
@api.get("/quizzes")
def list_quizzes(request):
    return {"quizzes": [...]}
```

### 2. Schema Pattern (Data Transfer Object)
- Handles data validation and serialization
- Defines the structure of requests/responses
```python
class QuizSchema(Schema):
    id: int
    title: str
    quiz_type: str
    difficulty: str
```

## Application-Specific Patterns

### 1. Singleton Pattern (ConfigurationManager)
**Purpose**: Ensures single instance for application configuration
```python
class ConfigurationManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
**Usage**:
- Quiz settings management (time limits, passing scores)
- Email template configurations
- Global application settings

### 2. Factory Pattern (QuizFactory)
**Purpose**: Creates different types of quizzes without exposing creation logic
```python
class DiseaseToSymptomsQuizFactory(QuizFactory):
    def create_quiz(self, difficulty: str) -> Quiz:
        return Quiz(
            title=f"Disease to Symptoms - {difficulty}",
            quiz_type=QuizType.DISEASE_TO_SYMPTOMS,
            difficulty=difficulty
        )
```
**Usage**:
- Creating Disease-to-Symptoms quizzes
- Creating Symptoms-to-Disease quizzes
- Extensible for new quiz types

### 3. Strategy Pattern (QuizEvaluator)
**Purpose**: Defines family of algorithms for quiz evaluation
```python
class BasicEvaluationStrategy(QuizEvaluationStrategy):
    def evaluate(self, user_answers: dict, correct_answers: dict) -> float:
        # Basic exact match evaluation
        pass

class KeywordEvaluationStrategy(QuizEvaluationStrategy):
    def evaluate(self, user_answers: dict, correct_answers: dict) -> float:
        # Keyword-based evaluation for medical terms
        pass
```
**Usage**:
- Different evaluation methods for different question types
- Exact match evaluation for simple questions
- Keyword-based evaluation for medical terminology
- Extensible for new evaluation methods

### 4. Bridge Pattern (QuizRenderer)
**Purpose**: Separates abstraction from implementation for quiz display
```python
class QuizRepresentation:
    def __init__(self, renderer: QuizRendererBase):
        self.renderer = renderer

class BasicQuizRenderer(QuizRendererBase):
    def render_question(self, question: Dict):
        # Basic text rendering
        pass
```
**Usage**:
- Different quiz display formats (web, mobile)
- Various question presentation styles
- Support for different UI requirements

### 5. Facade Pattern (QuizSystemFacade)
**Purpose**: Provides simplified interface to complex quiz system
```python
class QuizSystemFacade:
    def start_quiz(self, user_id: int, quiz_type: str, difficulty: str) -> Dict:
        # Handles all complexity of starting a quiz
        pass

    def submit_quiz(self, user_id: int, quiz_id: int, answers: Dict) -> Dict:
        # Manages quiz submission process
        pass
```
**Usage**:
- Simplifies quiz operations for API layer
- Coordinates between different components
- Manages quiz lifecycle

### 6. Observer Pattern (ProgressTracker)
**Purpose**: Tracks and notifies about quiz progress changes
```python
class ProgressSubject:
    def notify(self, user_id: int, quiz_id: int, progress: float):
        for observer in self._observers:
            observer.update(user_id, quiz_id, progress)
```
**Usage**:
- Track user progress
- Achievement monitoring
- Statistical analysis
