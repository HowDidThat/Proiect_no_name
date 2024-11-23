# Lab 4

The frontend architecture follows a Model-View-Controller (MVC) pattern, with a centralized communication layer implemented through a singleton adapter that manages all API interactions with the backend. This adapter serves as the single point of contact for data exchange, ensuring consistent and controlled access to the backend services. Quiz cards within the application are constructed using the composition pattern, allowing for flexible and modular creation of card components that can be easily assembled and modified. This compositional approach enables the dynamic generation of quiz cards with varying content types and interactive elements while maintaining a clean separation of concerns through the MVC structure.

# Core Architecture Pattern

- Implements Model-View-Controller (MVC)(MVVM) pattern
- Strict separation of concerns between data, presentation, and business logic

# Backend Communication Layer
- Singleton API Adapter

# Base card component as foundation
## Composition Pattern

- Question display
- Answer options
- Feedback presentation
- Progress indicators
- Interactive elements

### 1. MVC pattern (MVVM)
The main application frontend will be structured in a mvc fashion for separation of concerns
***Usage***
- User profiles
- Settings pages
- Data entry interfaces
- Quiz validation logic
The main application frontend will be structured in a mvc fashion for separation of concerns
### 2. Singleton pattern
```javaScript
class ApiService {
    async login(credentials){}
    async signup(userData){}
    async refreshToken(){}
    ...
}
```
***Usage***
- Maintains a single source of truth for API communication
- Centralizes authentication token management
- Ensures consistent headers and request configurations
- Prevents multiple instances from creating conflicting requests

### 3. Adapter pattern
```javaScript
    async getQuizzes(params = {}){}
    async getQuizById(quizId){}
    async createQuiz(quizData){}
    async updateQuiz(quizId, quizData){}
    async deleteQuiz(quizId){}
```
***Usage***
Creating a common denominator between the frontend and the backend APIs.
### 4. Composite pattern

The primary use for the composite pattern will be for creating the quiz and question cards providing a modular and scalable aproach for displaying the quiz.

***Usage***
- Quiz Structure Organization
- Question Types Hierarchy
- Navigation Structure
- Content Management
