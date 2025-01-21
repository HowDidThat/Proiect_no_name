import axios from "axios";
import { checkToken } from "./mop";
export class AccountService {
  //@logBeforeReg
  //@logAfterReg
  static async createAccount(
    username,
    email,
    password,
    institution,
    year_of_study
  ) {
    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/auth/register",
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          username: username,
          email: email,
          password: password,
          institution: institution,
          year_of_study: year_of_study,
        },
      });

      return "ok";
    } catch (error) {
      return error.response.data.errors[0].message;
    }
  }
}

export const { createAccount } = AccountService;

export class UserInfo {
  //@logBefore
  //@logAfter
  static async getUserInfo(token) {
    try {
      const response = await axios({
        method: "get",
        url: "http://127.0.0.1:8000/api/auth/me",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      return response;
    } catch (error) {
      console.error("Authentication failed:", error.message);
      return false;
    }
  }
}

export class QuizInfo {
  //@logBefore
  //@logAfter
  static async getQuizInfo(token) {
    try {
      console.log(token);
      return await axios.get("http://127.0.0.1:8000/api/quiz/", {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error("Authentication failed:", error.message);
      throw error;
    }
  }
}

export const { getUserInfo } = UserInfo;
export const { getQuizInfo } = QuizInfo;


export class CreateQuiz {
  static async crq(token, title,description,difficulty) {
    try {
      console.log(token);
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/quiz/create",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        data: {
          title : title,
          description : description,
          quiz_type : "dts",
          difficulty : difficulty,
        },
      })
      return response;
      ;
    } catch (error) {
      console.error("Authentication failed:", error.message);
      return "error"
    }
  }

  static async ccq(token, data) {
    try {
      console.log(data);
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/quiz/create/custom",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        data: {
          title: "default",
          description: "default",
          quiz_type: "default",
          difficulty: "easy",
          questions: data.map(symptoms => ({ symptoms }))
        },
      })
      return response;
      ;
    } catch (error) {
      console.error("Authentication failed:", error.message);
      return "error"
    }
  }


}

export const { crq } = CreateQuiz;

export const { ccq } = CreateQuiz;

export class GetQuiz {
  static async quizData(token, id) {
    try {
      console.log(token);
      const urlC = `http://127.0.0.1:8000/api/quiz/${id}`;
      console.log(urlC);
      const response = await axios({
        method: "get",
        url: urlC,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        }
      })
      return response;
    
    } catch (error) {
      console.error("Error failed:", error.message);
      return "error"
    }
  }
}

export const { quizData } = GetQuiz;



export class SubmitQuiz {
  static async sq(token, quizId,answers) {
    try {
      console.log(token);
      const response = await axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/quiz/${quizId}/submit`,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        data: {
          answers:[answers]
        },
      })
      return response;
      ;
    } catch (error) {
      console.error("Authentication failed:", error.message);
      return "error"
    }
  }
}

export const { sq } = SubmitQuiz;



export class UserTests {
  static async getUserTests(token) {
    try {
      console.log(token);
      const response = await axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/auth/results`,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        }
      })
      return response;
      ;
    } catch (error) {
      console.error("Authentication failed:", error.message);
      return "error"
    }
  }
}

export const { getUserTests } = UserTests;



export class AuthService {
  //@logBefore
  //@logAfter
  static async getToken(username, password) {
    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/api/auth/login",
        headers: {
          "Content-Type": "application/json",
        },
        data: {
          username: username,
          password: password,
        },
      });

      return response;
    } catch (error) {
      console.error("Authentication failed:", error.code);
      return 401;
    }
  }
}

export const { getToken } = AuthService;

export class QuizService {
  static async getAllDeseases(token) {
    try {
    //   const response = await axios({
    //     method: "get",
    //     url: "http://127.0.0.1:8000/api/quiz/diseases",
    //     headers: {
    //       "Content-Type": "application/json",
    //       Authorisation: `Bearer ${token}`,
    //     },
    //   });
    //   return response;
    return ["Desease 1", "Desease 2", "Desease 3", "Desease 4"];

    } catch (error){
        return "404";
    }
  }

  static async getAllSymptoms(token) {
    try {

    return ["Symptom 1", "Symptom 2", "Symptom 3", "Symptom 4"];
    } catch (error){
        return "404";
    }
  }
}
export const { getAllDeseases } = QuizService;
export const { getAllSymptoms } = QuizService;

