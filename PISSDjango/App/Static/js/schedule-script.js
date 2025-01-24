document.addEventListener('DOMContentLoaded', async function () {

    const backButton = document.getElementById('back_button');
    const username = sessionStorage.getItem('username');

    if (username === null) {
        backButton.innerHTML = 'Към началното меню';
        backButton.href = 'main.html'; 
    } else {
        backButton.innerHTML = 'Към главното меню';
        backButton.href = 'index.html'; 
    }

});