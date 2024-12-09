import axios from 'axios';
export class TokenVerifier {
    static async checkToken(token,refresh) {
        //if the tokens do not exist return false
        if (token == null || refresh == null)
            return {"status": 401, "new_token":null};
        
        let response =  await axios.get('http://127.0.0.1:8000/api/auth/me', {
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        //if the tokens does exist and is valid the page can continue
        if (response.status == 200)
            return {"status": 200, "new_token":null};
        
        //try refreshing the token
        let tokenRefresh =  await axios.get('http://127.0.0.1:8000/api/auth/refresh', {
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${refresh}`
            }
        });
        
        if (tokenRefresh.status == 200)
        {
            let new_token = response.data.refresh_token;
            return {"status":200, "new_token":new_token}
        }
        else
        {
            return {"status":401, "new_token":null}
        }
    }
}

export class CachedTestsVerifier{
    static async getTest(token,dificulty){
       
            try {
                const response = await axios.post('http://127.0.0.1:8000/api/auth/login', {
                    "title": "Quiz 000",
                    "description": "This test is auto-generated",
                    "quiz_type" : "std",
                    "difficulty": dificulty
                }, {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'application/json',
                        'uthorization' : `Bearer ${token}`
                    }
                });
                return response.data;
            } catch (error) {
                console.error('Authentication failed:', error.status);
                return 401;
    
            }
    }

    static async checkCashedTests(token) {
        let test_names = ["easy", "medium", "hard"];

        test_names.forEach((element) =>{
            let item = localStorage(element);
            if (item == null)
            {   
                let test = {};
                test["questions"] = this.getTest(token,element);
                test["completed"] = false;
                for (let i=0;i < length(test);i++)
                {
                    test["questions"][i]["answers"] = [];
                }
                localStorage.setItem(JSON.stringify(test));
            }
            
        })
    }

    static deleteStoredTests(){
        let test_names = ["easy", "medium", "hard"];
        test_names.forEach((element) =>{
            localStorage.setItem(element,"null");
        })
    }
}




export const {checkToken} = TokenVerifier;
export const {checkCashedTests} =  CachedTestsVerifier;
