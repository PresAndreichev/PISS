
document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    sessionStorage.clear(); //for when user return to the screen from Излизане

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    let isValid = validateCredentials(username, password);

    if (isValid) {

        var role;
        let isRegistered = await validateRegistration(username, password);
        
        if (isRegistered) {

            if (role == 1 || role == 2) {

                sessionStorage.setItem("username", username);
                sessionStorage.setItem("role", role);
                sessionStorage.setItem("password", password);
                window.location.href = '../html/index.html';

            } else {

                alert("Невалидна роля!");
                window.location.href = '../html/login.html';
            }

        } else {
            alert("Нерегистриран потребител!");
        }
    }
});

function validateCredentials(username, password) {
    const userMinLen = 6;
    const userMaxLen = 12;

    if (username.length < userMinLen || username.length > userMaxLen) {

        alert("Невалидни входни данни");
        window.location.href = '../html/login.html';
    }

    const passwordPattern = /^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*[0-9])[A-Za-z0-9а-яА-Я]{10,}$/;
    const passMinLen = 10;

    if ((!passwordPattern.test(password)) || password.length < passMinLen) {

        alert("Невалидни входни данни");
        window.location.href = '../html/login.html';
    }

    return true;

}

async function validateRegistration(username, password, email) {

    const data = JSON.stringify({ username: username, password: password, email : email });

        const response = await fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

    const responseJSON = await response.json();

        if (response.ok && responseJSON.success) {
            localStorage.setItem("authToken", responseJSON.token);
            role = responseJSON.role;
            window.location.href = '../html/index.html';
            return true;

        } else {
            return false;
        }

}


