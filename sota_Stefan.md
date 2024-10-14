## How will our application structure look like

### 1. Web technologies

- Front End framework:
    - Vue.js: Easy to learn, good for small to medium projects
    - React: Popular, great for larger applications

- Tailwind CSS / SASS:
    - Tailwind CSS: Quick styling with pre-built classes
    - SASS: Adds features to CSS for better organization

### 2. AI / ML

- NLP for user input:
    - BERT or GPT-3: Advanced models for understanding text
    - Keyword extraction: Simpler option to find important words

- Disease prediction:
    - CNN: Good for image-based medical data
    - RNN: Works well with symptom sequences
    - ID3 tree: Simple and easy to understand

### 3. Backend

- Django Ninja Framework:
    - Combines Django features with FastAPI speed
    - Includes user management and admin panel

- Deployment options:
    - AWS: Cloud platform with many useful services
    - Serverless: Automatic scaling, pay for what you use
    - Service Oriented Architecture: Split app into separate services

### 4. Database

- PostgreSQL:
    - Good for structured data and complex queries

- MongoDB:
    - Flexible for changing data types

- Amazon DynamoDB:
    - Fast and scales automatically

### 5. DevOps

- Testing:
    - Unit tests: Check small parts of code
    - Integration tests: Make sure different parts work together

- CI/CD with GitHub Actions:
    - Automate testing and deployment

- Docker:
    - Package app and its environment together
    - Makes it easier to move between computers

Mobile app (if time allows):

- Use Kotlin for Android or Flutter for both iOS and Android
- Connect to the same backend as the web app

## Possible Obstacles:

- Bad datasets:
    - May need to clean and combine data from different sources

- Finding the best ML model:
    - Try different models and compare results

- Proper symptom extraction:
    - Create a list of common symptoms and their variations

- Real world use:
    - Remind users it's not a replacement for doctors
    - Consider adding a way to connect with real medical professionals