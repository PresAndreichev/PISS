


document.addEventListener('DOMContentLoaded', function () {

    greet();

   
});

function greet() {

    const username = sessionStorage.getItem("username");

    const greeting = document.getElementById("greeting");

    greeting.textContent = "Добре дошли, " + username + "!";

}

