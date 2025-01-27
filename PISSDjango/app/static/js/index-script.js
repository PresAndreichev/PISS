document.addEventListener('DOMContentLoaded', function () {

    greet();


});

function greet() {
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