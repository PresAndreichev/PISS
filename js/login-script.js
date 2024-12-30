var role;

document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;

    let isValid = validateCredentials(username, password);

    if (isValid) {

        let isRegistered = await validateRegistration(username, password);

        if (isRegistered) {

            if (role == 1) {

                sessionStorage.setItem("username", username);
                sessionStorage.setItem("role", 1);
                window.location.href = '../html/student_index.html';

            } else if (role == 2) {

                sessionStorage.setItem("username", username);
                sessionStorage.setItem("role", 2);
                window.location.href = '../html/teacher_index.html';

            } else if (role == 3) {

                sessionStorage.setItem("username", username);
                sessionStorage.setItem("role", 3);
                window.location.href = '../html/admin_index.html';
            } else {

                alert("Невалидна роля!");
                window.location.href = '../html/login.html';
            }

        } else {
            alert("Нерегистриран потребител!");
        }
    }
});

function validateCredentials(username, password, email) {
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

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {

        alert("Невалидни входни данни");
        window.location.href = '../html/login.html';
    }

    return true;

}

async function validateRegistration(username, password, email) {

    const data = JSON.stringify({ username: username, password: password, email : email });

        const response = await fetch('../python/login.py', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

    const responseJSON = await response.json();

        if (responseJSON.success) {
            role = responseJSON.role;
            return true;

        } else {
            return false;
        }

}


