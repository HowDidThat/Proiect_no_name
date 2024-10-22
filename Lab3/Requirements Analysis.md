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

### Possible Actors

### 1. Medical Student
- Primary user of the application
- Learning medicine through interactive quizzes and games
- Manages their own learning progress and performance
- Can access both basic and advanced features of the application

### 2. Administrator
- System maintainer and content manager
- Responsible for system functionality and content quality
- Monitors user activity and system performance
- Manages the medical knowledge base

### Use Case Scenarios

### 1. Registration and Authentication

#### UC1: Register New Account

**Actor:** Medical Student
**Description:** New user creates an account in the system
**Main Flow:**
1. User accesses the registration page
2. Enters required personal information (name, email, password)
3. System validates input data
4. System creates new account
5. System sends verification email
6. User verifies email address
   
**Alternative Flows:**
- Email already registered
- Invalid input data
- Verification email fails to send

#### UC2: Login

**Actor:** Medical Student, Administrator
**Description:** User authenticates to access the system
**Main Flow:**
1. User enters credentials
2. System validates credentials
3. System grants appropriate access level

**Alternative Flows:**
- Invalid credentials
- Forgotten password
- Account locked after multiple failed attempts

#### UC3: Change Password

**Actor:** Medical Student, Administrator
**Description:** User modifies their account password
**Main Flow:**
1. User selects change password option
2. Enters current password
3. Enters and confirms new password
4. System validates and updates password

**Alternative Flows:**
- Current password incorrect
- New password doesn't meet requirements

### 2. Quiz and Game Functionality

#### UC4: Take Quiz

**Actor:** Medical Student
**Description:** User participates in a medical knowledge quiz
**Main Flow:**
1. User selects quiz type (Disease to Symptoms or Symptoms to Disease)
2. Sets difficulty level
3. System presents questions
4. User provides answers
5. System provides immediate feedback
6. Progress is automatically saved

**Alternative Flows:**
- Quiz interruption
- Connection loss during quiz
- Time limit exceeded

#### UC5: Play Symptom-Disease Game

**Actor:** Medical Student
**Description:** User engages in interactive symptom-disease matching game
**Main Flow:**
1. User starts new game session
2. Sets difficulty level
3. System presents game scenario
4. User matches symptoms with diseases
5. System provides real-time feedback
6. Progress is saved automatically

**Alternative Flows:**
- Game interruption
- Connection issues
- Invalid matches

#### UC6: Review Answers

**Actor:** Medical Student
**Description:** User reviews their quiz/game performance
**Main Flow:**
1. User selects completed quiz/game
2. System displays questions and user's answers
3. Shows correct answers and explanations
4. Provides learning resources for missed questions
   
**Alternative Flows:**
- Session expired
- Data not available

### 3. Progress Tracking

#### UC7: Track Progress

**Actor:** Medical Student
**Description:** User monitors their learning progress
**Main Flow:**
1. User accesses progress dashboard
2. Views performance metrics
3. Analyzes strength/weakness areas
4. Reviews historical performance
   
**Alternative Flows:**
- No data available
- Incomplete metrics

#### UC8: View Statistics

**Actor:** Medical Student
**Description:** User views detailed performance statistics
**Main Flow:**
1. User selects statistics view
2. Chooses time period
3. Views various performance metrics
4. Can export statistics
   
**Alternative Flows:**
- No data for selected period
- Export failure

### 4. Administrative Functions

#### UC9: Manage Question Bank

**Actor:** Administrator
**Description:** Admin maintains and updates question database
**Main Flow:**
1. Admin accesses question bank
2. Can add/edit/delete questions
3. Manages difficulty levels
4. Updates answer keys

**Alternative Flows:**
- Validation errors
- Duplicate questions
- Import/export issues

#### UC10: Monitor User Activity

**Actor:** Administrator
**Description:** Admin tracks system usage and user performance
**Main Flow:**
1. Admin views activity dashboard
2. Monitors user engagement
3. Reviews system performance
4. Generates usage reports
   
**Alternative Flows:**
- Data inconsistencies
- System performance issues

#### UC11: Update Medical Content

**Actor:** Administrator
**Description:** Admin maintains medical information accuracy
**Main Flow:**
1. Reviews existing content
2. Updates medical information
3. Adds new content
4. Validates content accuracy
   
**Alternative Flows:**
- Version conflicts
- Content validation failures
 
  
    
