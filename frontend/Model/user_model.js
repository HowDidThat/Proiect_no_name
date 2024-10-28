class userModel{
    username
    email 
    password
    firstName 
    lastName
    role 
    quizzesTaken 
    quizzesCreated 
    async getUserProfile(userId) {}
    async updateProfile(userId, userData) {}
    async getQuizHistory(userId) {}
    async updatePreferences(userId, preferences) {}
    
}