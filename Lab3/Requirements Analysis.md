# Requirements Analysis: Medical Student Quiz App

## Major Components

### 1. User Interface (UI)

#### 1.1 Web Application (To be implemented this semester)

- **Technology**: Vue.js
- **Description**: The primary interface for users to access quizzes, view progress, and manage their profiles via web
  browsers.
- **Key Features**:
    - Responsive design for various screen sizes
    - Interactive quiz-taking interface
    - Progress tracking and statistics dashboard
    - User profile management

#### 1.2 Mobile Application (Maybe implemented this semester)

- **Technology**: Kotlin for Android
- **Description**: A native mobile application providing on-the-go access to quizzes and user data.
- **Key Features**:
    - Offline quiz-taking capability
    - Push notifications for new quizzes and reminders
    - Touch-optimized interface

#### 1.3 Admin Interface (To be implemented this semester)

- **Technology**: Django Admin Panel
- **Description**: A backend interface for administrators to manage the application's content and users.
- **Key Features**:
    - Quiz creation and management
    - User account administration
    - System settings configuration

### 2. Backend Services

#### 2.1 API Service (To be implemented this semester)

- **Technology**: Django Ninja
- **Description**: Handles all backend logic and data management, serving as the bridge between the UI and the database.
- **Key Features**:
    - RESTful API endpoints for quiz, user, and statistics data
    - Authentication and authorization handling
    - Integration with AI model for answer evaluation

#### 2.2 Authentication System (To be implemented this semester)

- **Technology**: Django Auth
- **Description**: Manages user authentication and authorization across the application.
- **Key Features**:
    - User registration and login
    - Password reset functionality
    - Role-based access control

#### 2.3 AI Model (To be implemented this semester)

- **Technology**: Either custom-built using PyTorch/TensorFlow or AWS SageMaker (decision pending based on project progress)
- **Description**: Provides intelligent features for quiz evaluation and personalized learning.
- **Key Features**:
    - Automated answer evaluation
    - Personalized quiz recommendations (future implementation)
- **Implementation Options**:
    1. **Custom PyTorch/TensorFlow Solution**:
       - Develop models using PyTorch or TensorFlow frameworks
       - Train models on custom hardware or cloud-based GPU instances
       - Deploy models as part of the main application or as separate microservices
    2. **AWS SageMaker Solution**:
       - Utilize SageMaker's built-in algorithms or develop custom models
       - Use SageMaker's notebook instances for model development and training
       - Deploy models as SageMaker endpoints for real-time inference
       - Leverage SageMaker's AutoML capabilities for model optimization

- **Decision Criteria**: The choice between these options will depend on the project's progress, performance requirements, and resource availability.

### 3. Data Management

#### 3.1 Database (To be implemented this semester)

- **Technology**: PostgreSQL
- **Description**: Stores all application data, including user information, quiz content, and performance statistics.
- **Key Features**:
    - Efficient data storage and retrieval
    - Support for complex queries for statistics and reporting
    - Data backup and recovery mechanisms

#### 3.2 Content Management System (Maybe implemented this semester)

- **Description**: Allows for the creation, editing, and organization of quiz content.
- **Key Features**:
    - Quiz creation interface for administrators
    - Version control for quiz questions

### 4. External Integrations

#### 4.1 Email Service (To be implemented this semester)

- **Description**: Handles all email communications from the application to users.
- **Key Features**:
    - User registration confirmation
    - Password reset emails
    - Notifications for new quizzes or important updates

#### 4.2 Analytics System (Maybe implemented this semester)

- **Description**: Provides detailed insights into user behavior and application performance.
- **Key Features**:
    - User engagement metrics
    - Quiz performance analytics
    - System usage statistics

### 5. AWS Integration (To be implemented throughout the semester)

- **Description**: Utilize select AWS services to enhance scalability, reliability, and functionality of the application.
- **Key AWS Services**:
    - **Amazon S3**: For storing static assets and backup data
    - **Amazon EC2**: For hosting the application backend and API service
    - **Amazon RDS**: For managing the database, using either PostgreSQL or MariaDB
    - **AWS Lambda**: For serverless computing, handling tasks like email sending and data processing
    - **Amazon SES**: For sending transactional emails
    - **Amazon CloudWatch**: For monitoring application performance and logs
    - **Amazon Comprehend**: For natural language processing tasks in quiz content analysis, if required
    - **Amazon API Gateway**: For managing API endpoints and integrations
    - **Amazon CloudFormation**: For infrastructure as code and automated deployment
 
## Use Case 

### 1. Actors
- **Medical Student**
  - Main user of the application
  - Focuses on learning and practicing medical diagnosis
  - Tracks their progress and performance

- **Administrator**
  - Manages the system content and users
  - Monitors system usage and maintains quality

## 2. Scenarios

### 2.1 User Authentication

#### UC1: Register
- **Primary Actor:** Medical Student
- **Preconditions:** None
- **Main Flow:**
  1. Student selects "Register" option
  2. System displays registration form
  3. Student enters required information:
     - Full name
     - Email address
     - Password
     - Academic institution
     - Year of study
  4. System validates the information
  5. System creates new account
  6. System sends verification email

- **Alternative Flows:**
  - Email already registered
  - Invalid email format
  - Password doesn't meet requirements
  - Registration form incomplete

#### UC2: Login
- **Primary Actor:** Medical Student, Administrator
- **Preconditions:** User has registered account
- **Main Flow:**
  1. User enters email and password
  2. System validates credentials
  3. System grants access to appropriate interface

- **Alternative Flows:**
  - Invalid credentials
  - Forgotten password
  - Account locked

### 2.2 Core Quiz Functionality

#### UC3: Take Quiz
- **Primary Actor:** Medical Student
- **Preconditions:** User is logged in
- **Main Flow:**
  1. Student selects "Take Quiz" option
  2. System presents difficulty level selection
  3. Student chooses quiz type:
     - Disease to Symptoms
     - Symptoms to Disease
  4. System presents quiz questions
  5. Student submits answers
  6. System provides immediate feedback
  7. System saves progress

- **Alternative Flows:**
  - Quiz interrupted
  - Connection lost
  - Time limit exceeded

### 2.3 Progress Tracking

#### UC4: Track Progress
- **Primary Actor:** Medical Student
- **Preconditions:** User has completed quizzes
- **Main Flow:**
  1. Student accesses progress dashboard
  2. System displays:
     - Overall performance metrics
     - Quiz completion rates
     - Accuracy statistics
     - Time-based progress
  3. Student can filter results by:
     - Time period
     - Quiz type
     - Difficulty level

- **Alternative Flows:**
  - No data available
  - Export statistics
  - Reset progress view

### 2.4 Administrative Functions

#### UC5: Manage Question Bank
- **Primary Actor:** Administrator
- **Preconditions:** Admin is logged in
- **Main Flow:**
  1. Admin accesses question management interface
  2. System displays current question bank
  3. Admin can:
     - Add new questions
     - Edit existing questions
     - Review question statistics
     - Manage difficulty levels
  4. System validates changes
  5. System updates question bank

- **Alternative Flows:**
  - Validation errors
  - Duplicate questions
  - Batch updates

#### UC6: Monitor User Activity
- **Primary Actor:** Administrator
- **Preconditions:** Admin is logged in
- **Main Flow:**
  1. Admin accesses monitoring dashboard
  2. System displays:
     - Active users
     - Usage patterns
     - Performance metrics
     - System health indicators
  3. Admin can generate reports
  4. System allows filtering and analysis

- **Alternative Flows:**
  - Export reports
  - Flag suspicious activity
  - System alerts

## 3. Relationships

### Include Relationships
- Take Quiz **includes** Set Difficulty Level
- Take Quiz **includes** Save Progress
- Track Progress **includes** View Statistics

### Extend Relationships
- Take Quiz **extended by** Disease to Symptoms Quiz
- Take Quiz **extended by** Symptom to Diseases Quiz
- Take Quiz **extended by** Review Answers
- Login **extended by** Change Password
