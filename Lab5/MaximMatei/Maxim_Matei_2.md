# Model driven development (MDD)

### User Stories

- Users should be able to view their personal information
- Users should be able to edit their profile details
- Users should be able to upload a profile picture

### Business Rules

- Email addresses must be unique
- Certain fields are mandatory (name, email)
- Data must comply with privacy regulations

### Use cases

Primary Use Cases:
- View Profile
- Edit Profile
- Upload Photo

### Platform Independent Model 

User 
- id: Identifier
- email: String
- description: String
- testTaken: String
- picture: URL
- averageTestScore: Number
- FavoriteQuizType: Striing

### Process Models

1. View profile

    - User requests profile page
    - System authenticates request
    - System retrieves user data
    - System displays information

2. Profile update photo 
    - User selects photo
    - System validates format/size
    - System processes image
    - System stores image
    - System updates profile

### Platform specific model(PMS)

Frontend:
- Vue.js
- Vue Router
- Form Validation
- HTTP Client

