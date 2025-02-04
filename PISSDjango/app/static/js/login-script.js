﻿document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    sessionStorage.clear(); //for when user return to the screen from Излизане

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    let isValid = validateCredentials(username, password);

    if (isValid) {
        let isRegistered = await validateRegistration(username, password);

        if (isRegistered) {
            const role = sessionStorage.getItem('role');
            if (role == "1" || role == "2") {
                window.location.href = '/static/html/index.html';
            }
        }
    } else {
        alert("Невалидни входни данни!");
    }
});

function validateCredentials(username, password) {
    const userMinLen = 6;
    const userMaxLen = 12;

    if (username.length < userMinLen || username.length > userMaxLen) {
        return false;
    }

    const passwordPattern = /^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*[0-9])[A-Za-z0-9а-яА-Я]{10,}$/;
    const passMinLen = 10;

    if ((!passwordPattern.test(password)) || password.length < passMinLen) {
        return false;
    }

    return true;

}

async function validateRegistration(username, password, email) {

    const data = JSON.stringify({ username: username, password: password, email: email});

        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

    const responseJSON = await response.json();
        
        if (response.ok && responseJSON.success) {
            //localStorage is persistent even after closing browser (for tokens), while session is only valid for current tab
            localStorage.setItem("authToken", responseJSON.token);
            sessionStorage.setItem("role", responseJSON.role);
            return true;

        } else {
            return false;
        }
}


