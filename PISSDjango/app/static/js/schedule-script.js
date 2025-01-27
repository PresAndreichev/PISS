document.addEventListener('DOMContentLoaded', async function () {

    const backButton = document.getElementById('back_button');
    const username = sessionStorage.getItem('username');

    if (username === null) {
        backButton.innerHTML = 'Към началното меню';
        backButton.href = '/static/html/main.html'; 
    } else {
        backButton.innerHTML = 'Към главното меню';
        backButton.href = '/static/html/index.html'; 
    }

});