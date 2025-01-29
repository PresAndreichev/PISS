// If the user has been authorized a login token, he won't be asked to login again while the token lasts
const token = localStorage.getItem("authToken");
if (token) {
    window.location.href="/static/html/index.html"
}