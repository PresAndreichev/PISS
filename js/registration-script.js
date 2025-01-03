﻿document.addEventListener('DOMContentLoaded', function () {
    const roles = document.querySelectorAll('input[name="role"]');
    const targetElement = document.getElementById('fn-field');
    const toggleClass = 'input-fn-disabled';

    roles.forEach(role => {
        role.addEventListener('change', function () {
            if (role.checked && role.value === '1') {
                targetElement.classList.remove(toggleClass);
            } else if (role.checked && (role.value === '2' || role.value === '3')) {
                targetElement.classList.add(toggleClass);
            }
        });
    });


    document.getElementById('register-form').addEventListener('submit', async function (event) {

        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const role = document.querySelector('input[name="role"]:checked').value;
        const fn = document.getElementById('fn').value;
        const email = document.getElementById('email').value;

        var isValidUsername = validateUsername(username)
        var isValidPW = validatePassword(password)
        var isValidFn = validateFn(role, fn);
        var isValidEmail = validateEmail(email);
    ;

        let isValid = isValidUsername && isValidPW && isValidFn && isValidEmail;

        if (isValid) {
            
            checkAvailability(username, password, role, email, fn);
        }

    });

    function validateUsername(username) {
        const userMinLen = 6;
        const userMaxLen = 12;


        inputCriteriaElements = document.getElementsByClassName('input-criteria');

        if (username.length < userMinLen || username.length > userMaxLen) {


            inputCriteriaElements[0].classList.add('input-error');
            inputCriteriaElements[0].classList.remove('input-criteria-right');
                     

            return false;
        }
        inputCriteriaElements[0].classList.add('input-criteria-right');
        inputCriteriaElements[0].classList.remove('input-error');
        return true;
    }

    function validatePassword(password) {
        const passwordPattern = /^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*[0-9])[A-Za-z0-9а-яА-Я]{10,}$/;
        inputCriteriaElements = document.getElementsByClassName('input-criteria');
        const passMinLen = 10;

        if ((!passwordPattern.test(password)) || password.length < passMinLen) {

            inputCriteriaElements[1].classList.add('input-error');
            inputCriteriaElements[1].classList.remove('input-criteria-right');

            return false;
        }
        inputCriteriaElements[1].classList.add('input-criteria-right');
        inputCriteriaElements[1].classList.remove('input-error');
        return true;
    }

    function validateEmail(email) {

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const inputCriteriaElements = document.getElementsByClassName('input-criteria');

        if (!emailPattern.test(email)) {
            inputCriteriaElements[2].classList.add('input-error');
            inputCriteriaElements[2].classList.remove('input-criteria-right');

            return false;
        }
    
        inputCriteriaElements[2].classList.add('input-criteria-right');
        inputCriteriaElements[2].classList.remove('input-error');
        return true;
    }

    function validateFn(role, fn) {

        const FnMinLen = 5;
        const FnMaxLen = 10;

        inputCriteriaElements = document.getElementsByClassName('input-criteria');

        if (role === '1' && (fn.length < FnMinLen || fn.length > FnMaxLen)) {

            inputCriteriaElements[3].classList.add('input-error');
            inputCriteriaElements[3].classList.remove('input-criteria-right');

            return false;
        }
        inputCriteriaElements[3].classList.add('input-criteria-right');
        inputCriteriaElements[3].classList.remove('input-error');
        return true;
    }

});

async function checkAvailability(username, password, role, email, fn) {

    const data = JSON.stringify({ username: username, password: password, role: role, email: email, fn: fn });

    try {
        const response = await fetch('../python/registration.py', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        responseJSON = await response.json();


        if (responseJSON.success) {
            alert('Регистрацията беше успешна!');
            window.location.href = '../html/register.html';

        } else {
            alert('Съществуващ потребител!');
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}