import axios from 'axios';

export class AccountService {
    //@logBeforeReg
    //@logAfterReg
    static async createAccount(data) {
        try {
            data;
            const response = await fetch('http://127.0.0.1:8000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: data.name,
                    email: data.email,
                    password: data.password,
                    institution: "UAIC",
                    year_of_study: 2
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.log(errorData["errors"][0]["message"]);
                
                return {message: [errorData["errors"][0]["message"]]};
            }

            return await response.json();
        } catch (error) {
            console.error('Error during registration:', error.message);
            throw error;
        }
    }
}

export const {createAccount} = AccountService;



export class UserInfo {
    //@logBefore
    //@logAfter
    static async getUserInfo(token) {
        try {
            console.log(token)
            return await axios.get('http://127.0.0.1:8000/api/auth/me', {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
        } catch (error) {
            console.error('Authentication failed:', error.message);
            throw error;
        }
    }
}

export class QuizInfo {
    //@logBefore
    //@logAfter
    static async getQuizInfo(token) {
        try {
            console.log(token)
            return await axios.get('http://127.0.0.1:8000/api/quiz/', {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
        } catch (error) {
            console.error('Authentication failed:', error.message);
            throw error;
        }
    }
}

export const {getUserInfo} = UserInfo;
export const {getQuizInfo} = QuizInfo;


export class AuthService {
    //@logBefore
    //@logAfter
    static async getToken(email, password) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/auth/login', {
                username: email,
                password: password
            }, {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            return response;
        } catch (error) {
            console.error('Authentication failed:', error.status);
            return 401;

        }
    }
}

export const {getToken} = AuthService;
