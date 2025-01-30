function getCurrentUser(token) {
    if (token !== null) {
        try {
            const decoded = jwt_decode(token);
            const username = decoded.username || decoded.user_id;
            return username;
        } catch (e) {
            return undefined;
        }
    }
    return undefined;
}
function generateBackMenuButton(current_user) {
    const referedPage = current_user === undefined ? 'начално' : 'главно';
    const referedPageSite = current_user === undefined ? "/static/html/main.html" : "/static/html/index.html";
    const headerText = "Обратно към " + referedPage + " меню";
    const headerButton = document.querySelector('header > a');
    headerButton.textContent = headerText
    headerButton.setAttribute("href", referedPageSite);
}
async function changePW(oldPW, newPW, newPW_2, token) {
    if (oldPW == newPW) {
        alert("Новата парола не можа да съвпада със старата");
        return false;
    }
    else if (newPW != newPW_2) {
        alert("Новата парола не съвпада с потвърждението й");
        return false;
    }
    const stringifiedData = JSON.stringify({ token: token, current_password: oldPW, new_password: newPW });
    const response = await fetch('/api/change_password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: stringifiedData
    });
    const responseData = await response.json();
    return responseData.success;
}
async function executeChange(event) {
    event.preventDefault();
    const oldPW = document.getElementById('oldPW').value;
    const newPW = document.getElementById('newPW').value;
    const newPW_2 = document.getElementById('newPW_confirmation').value;
    const token = localStorage.getItem('authToken');
    if (await changePW(oldPW, newPW, newPW_2, token)) {
        alert("Успешно променена парола!");
    }
    else {
         alert("Неуспешно променена парола!");
    }
    document.getElementById('oldPW').textContent = "";
    document.getElementById('newPW').textContent = "";
    document.getElementById('newPW_confirmation').textContent = "";
}
document.addEventListener('DOMContentLoaded', async function () {
    const token = localStorage.getItem('authToken');
    let current_user = getCurrentUser(token);
    generateBackMenuButton(current_user);
    document.getElementById('changePasswordFrom')
        .addEventListener('submit', executeChange);
});