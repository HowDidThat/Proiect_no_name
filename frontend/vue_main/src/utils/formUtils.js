export const validatePassword = (password, confirmPassword) => {
    // Initialize validation flags and error messages
    const validationRules = {
        minLength: {
            test: password.length >= 8,
            message: "Password must be at least 8 characters long"
        },
        uppercase: {
            test: /[A-Z]/.test(password),
            message: "Password must contain at least one uppercase letter"
        },
        lowercase: {
            test: /[a-z]/.test(password),
            message: "Password must contain at least one lowercase letter"
        },
        number: {
            test: /\d/.test(password),
            message: "Password must contain at least one number"
        },
        specialChar: {
            // eslint-disable-next-line
            test: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(password),
            message: "Password must contain at least one special character"
        },
        noSpaces: {
            test: !/\s/.test(password),
            message: "Password must not contain spaces"
        },
        consecutive: {
            test: !/(.)\1{2,}/.test(password),
            message: "Password must not contain three or more consecutive identical characters"
        },
        samePassword:{
            test: password == confirmPassword,
            message: "Passwords do not match"
        }
    };

    const errors = [];

    for (const rule in validationRules) {
        if (!validationRules[rule].test) {
            errors.push(validationRules[rule].message);
        } 
    }
    return  errors;
}

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