# Lab 4

The frontend architecture follows a Model-View-Controller (MVC) pattern, with a centralized communication layer implemented through a singleton adapter that manages all API interactions with the backend. This adapter serves as the single point of contact for data exchange, ensuring consistent and controlled access to the backend services. Quiz cards within the application are constructed using the composition pattern, allowing for flexible and modular creation of card components that can be easily assembled and modified. This compositional approach enables the dynamic generation of quiz cards with varying content types and interactive elements while maintaining a clean separation of concerns through the MVC structure.

# Core Architecture Pattern

- Implements Model-View-Controller (MVC) pattern
- Strict separation of concerns between data, presentation, and business logic

# Backend Communication Layer
- Singleton API Adapter

Single instance managed through static factory
Centralized point for all API communications
Handles authentication and request/response lifecycle
Implements retry and error handling strategies

# Composition Pattern

## Base card component as foundation
## Specialized components through composition:

- Question display
- Answer options
- Feedback presentation
- Progress indicators
- Interactive elements



