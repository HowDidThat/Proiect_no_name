# Model driven development (MDD)

### User Stories

- Users should be able to register with email and password
- Users should be able to login with credentials
- System should validate user inputs

### Business Rules

- Email must be unique in the system
- Passwords must meet security requirements
- Passwords must be stored securely*

### Use cases

- User Registration
- User Login

### Platform Independent Model 

User 
- id: Identifier
- email: String
- password: String
- name: String


### Process Models

1. Registration

    - User submits registration form
    - System validates input
    - System checks email uniqueness
    - System creates user account
    - System generates verification token
    - System sends verification email

2. Login 
    - User submits login credentials
    - System validates input
    - *System verifies credentials*
    - System returns authentication token

### Platform specific model(PMS)

Frontend:
- Vue.js
- Vue Router
- Form Validation
- HTTP Client

