import axios from 'axios';
export class TokenVerifier {
    static async checkToken(token, refresh) {
        console.log("0");
        if (token == null && refresh == null)
            return { status: 401, new_token: null };
        try {
            console.log("1")
            const response = await axios({
                method: 'get',
                url: 'http://127.0.0.1:8000/api/auth/me',
                headers: {
                          'Content-Type': 'application/json',
                          'Authorization': `Bearer ${token}`
                      }
              });

          
            if (response.status == 200) {
                return { status: 200, new_token: null };
            }
        } catch (error) {
            
            try {
                console.log("2")
                const tokenRefresh = await axios({
                    method: 'get',
                    url: 'http://127.0.0.1:8000/api/auth/refresh',
                    headers: {
                              'Content-Type': 'application/json',
                              'Authorization': `Bearer ${token}`
                          }
                  });

                if (tokenRefresh.status == 200) {
                    
                    const new_token = tokenRefresh.data.refresh_token;
                    console.log("3");
                    return { status: 200, new_token: new_token };
                }
            } catch (refreshError) {
                console.log("4")
                return { status: 401, new_token: null };
            }
        }
        console.log("4")
        return { status: 401, new_token: null };
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
            let item = localStorage.getItem(element);
            if (item == null)
            {   
                let test = {};
                test["questions"] = this.getTest(token,element);
                test["completed"] = false;
                for (let i=0;i < test.length;i++)
                {
                    test["questions"][i]["answers"] = [];
                }
                localStorage.setItem(element,JSON.stringify(test));
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
