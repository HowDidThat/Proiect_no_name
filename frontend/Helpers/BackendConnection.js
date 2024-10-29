class ApiService {
    async login(credentials){}
    async signup(userData){}
    async refreshToken(){}
  
    async getUserProfile(){}
    async updateProfile(profileData){}
    async getUserStatistics(){}
  
    async getQuizzes(params = {}){}
    async getQuizById(quizId){}
    async createQuiz(quizData){}
    async updateQuiz(quizId, quizData){}
    async deleteQuiz(quizId){}
  
    async startQuizAttempt(quizId){}
    async submitQuizAttempt(quizId, attemptId, answers){}
    async getQuizResults(quizId, attemptId){}
    async getQuizStatistics(quizId){}
  

    handleError(error){}
    handleAuthResponse(response){}
    handleTokenExpiration(){}
  }
  
