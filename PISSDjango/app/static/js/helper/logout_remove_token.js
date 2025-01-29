// If the user wishes to leave, we should delete the token!
document.getElementById("logout").addEventListener('click', () => {
    localStorage.removeItem('authToken');
    console.log("Token was here, now not! :_)");
})