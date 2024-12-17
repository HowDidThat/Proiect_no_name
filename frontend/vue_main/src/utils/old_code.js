
/*
const logBefore = beforeMethod((meta) => {
    console.log(`Attempting login for email: ${meta.args[0]}`);
    console.log(`Attempting login for password: ${meta.args[1]}`);
    console.log('Starting authentication request...');
});

const logAfter = afterMethod((meta) => {
    if (meta.data?.message == "Login successful") {
        console.log('Authentication successful');
    } else {
        console.log('Authentication completed without token');

    }
});
*/


/*
export const validatePassword = (email, password) => {
    if (email == "test@test.com" && password == "test") {
        return {
            exists: true,
            status: 200,
            token: "good_token"
        }
    }
    if (email == "cart@gmail.com" && password == "StrongPass9_") {
        return {
            exists: true,
            status: 200,
            token: "Zx8kT4vY2Mn9QpL6Wr3CbA1JsDfX5HqP"
        }
    }

    if (email == "jhon.doe12@gmail.com" && password == "KaolaHighScool23") {
        return {
            exists: true,
            status: 200,
            token: ""
        }
    }

    return {
        exists: false,
        status: 200,
        token: ""
    }
}
*/

/*

const logBeforeReg = beforeMethod((meta) => {
    const userData = meta.args[0];
    console.log(`Starting account creation for user: ${userData.name}`);
    console.log('Initiating registration request...');
});

const logAfterReg = afterMethod(async (meta) => {
    const result = await meta.result;
    if (result.message?.includes('bad request')) {
        //console.log('Registration failed: Bad request');
    } else {
        //console.log('Registration completed successfully');
    }
});
*/


/*
export const getUserData = (token) => {
    if (token === "good_token") {
        return {
            name: "Carol Smith",
            email: "carol.smt@hot.com",
            description: "Teacher at 'University of Lodon'.",
            testTaken: "101",
            picture: "/home/doom/Documents/GitHub/Symptom_Disease_Quiz_Application_for_Cardiology_Students_using_AI/frontend/vue_main/src/assets/BG.jpg",
            averageTestScore: 97.6,
            favoriteQuizType: "Classic",
            status: "200"
        }
    }
    return {
        status: "404"
    }
}
    */
/*
export const validateToken = (token) => {
    if (token == "fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4l") {
        return {
            name: "Carol Smith",
            email: "carol.smt@hot.com",
            description: "Teacher at 'University of Lodon'.",
            testTaken: "101",
            picture: "/home/doom/Documents/GitHub/Symptom_Disease_Quiz_Application_for_Cardiology_Students_using_AI/frontend/vue_main/src/assets/BG.jpg",
            averageTestScore: 97.6,
            FavoriteQuizType: "Classic",
        }
    } else {
        return {
            token: token,
            response: "Invalid token"
        }
    }

}
export const sendQuizData = (token, quiz) => {
    let payload = {
        "token": token,
        "quiz": quiz
    }
    console.log(payload)

}
    */
/*
export const getCompletedQuizData = (quizId) => {
    if (quizId == "1")
        return ([{
                text: "This is the first question",
                symptoms: ["Disentery", "Cancer", "Explosive t", "Melenoma"],
                diseases: ["Disease A", "Covid", "Red nose"],
                answer: ["Disease A", "Covid"],
                correct: ["Disease A", "Red nose"]
            }]

        )
    if (quizId == "2")
        return (
            [
                {
                    text: "This is the second question",
                    symptoms: ["D 2", "Thing 2", "Q2"],
                    diseases: ["Disease A", "Covid", "Red nose", "thing2", "thing3", "thing4"],
                    answer: ["Red nose", "thing3"],
                    correct: ["Disease A", "Red nose"]
                },
                {
                    text: "This is the first question",
                    symptoms: ["Disentery", "Cancer", "Explosive t", "Melenoma"],
                    diseases: ["Disease A", "Covid", "Red nose"],
                    answer: ["Disease A", "Covid"],
                    correct: ["Disease A", "Red nose"]
                }
            ]
        )
    return (-1)
}
*/
/*
export const getQuizIds = (token) => {
    if (token == "good_token")
        return ([
            {
                "id": "1",
                "date": "10/10/2020",
                "points": "5/10"
            },
            {
                "id": "2",
                "date": "25/01/2024",
                "points": "9/10"
            }
        ])
    return ([])
}
*/

/*
console.log("Test Case 1");
let result = validatePassword("kimmi@gmail.com", "Kimmoki12!");
console.log(result);
console.log(result.exists === true && result.token === "fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4l" ? "Pass" : "Fail");

console.log("Test Case 2");
result = validatePassword("unknown@gmail.com", "SomePassword!");
console.log(result);
console.log(result.exists === false && result.token === "" ? "Pass" : "Fail");
result = validatePassword("cart@gmail.com", "WrongPassword");
console.log(result);
console.log(result.exists === false && result.token === "" ? "Pass" : "Fail");
console.log("Test Case 4");
result = validatePassword("random@gmail.com", "123456");
console.log(result);
console.log(result.exists === false && result.token === "" ? "Pass" : "Fail");



console.log("Test Case 1");
result = validateToken("fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4l");
console.log(result);
console.log(
    result.name === "Carol Smith" &&
    result.email === "carol.smt@hot.com" &&
    result.description === "Teacher at 'University of Lodon'." &&
    result.testTaken === "fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4l" &&
    result.picture === "/home/doom/Documents/GitHub/Symptom_Disease_Quiz_Application_for_Cardiology_Students_using_AI/frontend/vue_main/src/assets/BG.jpg" &&
    result.averageTestScore === 97.6 &&
    result.FavoriteQuizType === "Classic"
    ? "Pass" : "Fail"
);

// Test Case 2: Invalid token with random string
console.log("Test Case 2");
result = validateToken("randomToken123");
console.log(result);
console.log(result.token === "randomToken123" && result.response === "Invalid token" ? "Pass" : "Fail");

// Test Case 3: Invalid token with empty string
console.log("Test Case 3");
result = validateToken("");
console.log(result);
console.log(result.token === "" && result.response === "Invalid token" ? "Pass" : "Fail");

// Test Case 4: Invalid token with similar but incorrect token
console.log("Test Case 4");
result = validateToken("fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4m"); // One character off
console.log(result);
console.log(result.token === "fK7zT9gLwM3XcV8pY6QsD2jN5RxBhP4m" && result.response === "Invalid token" ? "Pass" : "Fail");
*/


/*
function testPassword(password) {
    console.log(`Testing password: ${password}`);
    const result = validatePassword(password);
    console.log('Validation result:', result);
    console.log('------------------------');
}
testPassword("weak", "weak");
testPassword("Password123","asdeqwdasadqwdas");
testPassword("Password123!","Password123!");
testPassword("SuperStr0ng!Pass","kkkk");
testPassword("aaa123!A","dqwdaasd1wqsad");  
testPassword("Pass word","sadqw");
*/