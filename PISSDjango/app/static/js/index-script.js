﻿async function sendDeactivationRequest(token) {
    const data = JSON.stringify({ token: token });


    //There may be an issue with url
    const response = await fetch('/api/disable_profile/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: data
    });


    if (response.status === 200) {
        return true;
    } else {
        return false;
    }
}

async function greet() {
    const token = localStorage.getItem("authToken");

    if (token) {
        try {
            const decoded = jwt_decode(token);
            const username = decoded.username || decoded.user_id;
            const greeting = document.getElementById("greeting");
            greeting.textContent = "Добре дошли, " + username + "!";
        } catch (e) {
            console.error("Error decoding token:", e);
        }
    } else {
        console.error("No token found");
    }

}

document.addEventListener('DOMContentLoaded', async function () {
    greet();

    let delete_button = document.getElementById("delete_acc_button");
    let confirmation_bt = document.getElementById("confirmation_container");
    confirmation_bt.style.display = "none";

    delete_button.addEventListener('click', function () {
        confirmation_bt.style.display = "inline-block";

        let token = localStorage.getItem("authToken");

        let permanent_delete_bt = document.getElementById("confirm_deletion_button");
        let stop_delete_bt = document.getElementById("stop_deletion_button");

        stop_delete_bt.addEventListener('click', function () {
            alert("Деактивиране на акаунт е отменено!");
            confirmation_bt.style.display = "none";
            return;
        });

        permanent_delete_bt.addEventListener('click', async function () {
            if (await sendDeactivationRequest(token)) {
                alert("Успешно изтрит профил!");
                localStorage.removeItem("authToken");
                window.location.href = '/static/html/main.html';
            } else {
                alert("Неуспешно изтрит профил! Моля, опитайте пак по-късно.");
                confirmation_bt.style.display = "none";
            }
        });
    });
});
