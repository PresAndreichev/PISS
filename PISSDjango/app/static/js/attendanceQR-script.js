navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(function(stream) {
        const video = document.getElementById('video');
        video.srcObject = stream;
        video.setAttribute("playsinline", true);
        video.play();
    })
    .catch(function(err) {
        console.error("Error accessing the camera: ", err);
    });

const video = document.getElementById('video');
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

function scanQRCode() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.height = video.videoHeight;
        canvas.width = video.videoWidth;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, canvas.width, canvas.height);

        if (code) {
            console.log("QR Code detected: ", code.data);
            sendQRDataToServer(code.data);
        }
    }
    requestAnimationFrame(scanQRCode);
}

// Start scanning
scanQRCode();

// Send QR code data to server
function sendQRDataToServer(data) {
    const token = localStorage.getItem('authToken');
    const requestData = { token, qr_code: data, event_id : "1" };

    fetch('/api/qr_scanner/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(result => {
        console.log('Server response:', result);

        // Clear the current list of usernames
        const userList = document.getElementById('usernames');
        userList.innerHTML = '';

        // If there is a user list, display them
        if (result.success && result.user) {
            const users = result.user;
            // Iterate over the list of users and add them to the page
            users.forEach(username => {
                const li = document.createElement('li');
                li.textContent = username;
                userList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No users found.';
            userList.appendChild(li);
        }
    })
}

function goBack() {
    window.history.back();
}