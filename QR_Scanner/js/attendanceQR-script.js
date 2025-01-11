document.addEventListener('DOMContentLoaded', async function () {
    const qrFeed = document.querySelector('#attendanceQR img');

    if (qrFeed) {
        console.log('QR code scanner feed loaded.');
    } else {
        console.error('QR code scanner feed not found.');
    }

    // Function to fetch and display scanned QR codes
    async function fetchScannedCodes() {
        console.log("Attempting to fetch scanned QR codes..."); // Log this for debugging
        try {
            const response = await fetch('/scanned_qr_codes');
            console.log('Fetched data:', response); // Log the raw response

            if (response.ok) {
                const data = await response.json();
                console.log('Scanned QR Codes:', data.scanned_codes); // Log the actual data

                // Example: Displaying the scanned codes in the console
                data.scanned_codes.forEach(item => {
                    console.log(`Code: ${item.code}, Timestamp: ${item.timestamp}`);
                });

                // Optionally update the UI here
                const list = document.getElementById('scannedCodesList');
                if (list) {
                    list.innerHTML = ''; // Clear the list first
                    data.scanned_codes.forEach(item => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<strong>Code:</strong> ${item.code} <strong>Timestamp:</strong> ${item.timestamp}`;
                        list.appendChild(listItem);
                    });
                }
            } else {
                console.error('Failed to fetch scanned codes.');
            }
        } catch (error) {
            console.error('Error fetching scanned codes:', error);
        }
    }

    // Fetch scanned codes every 5 seconds
    setInterval(fetchScannedCodes, 5000); // Adjust interval as needed
});
