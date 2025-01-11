function date_time_now() {
    const now = new Date();
    const options = {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false 
    };
    return now.toLocaleString('en-GB', options);

}

function generateTimeOptions() {
    const timeOptions = [];
    for (let i = 0; i < 24; i++) {
        const time = `${i.toString().padStart(2, '0')}:00`; // Format as "00:00"
        timeOptions.push(`<option value="${time}">${time}</option>`);
    }
    return timeOptions.join('');

}

document.addEventListener('DOMContentLoaded', async function () {

    const current_user = sessionStorage['username'];
    const userRole = sessionStorage['role'];

    const startTimeSelect = document.getElementById('startTime');
    const endTimeSelect = document.getElementById('endTime');

    const optionsHTML = generateTimeOptions();
    startTimeSelect.innerHTML = optionsHTML;
    endTimeSelect.innerHTML = optionsHTML;

    room_filters = document.getElementById('timeSelectionForm');

    room_filters.addEventListener('submit', async function () {

        event.preventDefault();

        const date = document.getElementById('datePicker').value;
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;
        const criteria1 = document.getElementById('criteria1').value; //computer, normal
        const criteria2 = document.getElementById('criteria2').value; //white, black, interactive
        const criteria3 = document.getElementById('criteria3').value; // 1 has media, 0 - has no media

        if (startTime >= endTime) {
            alert('Началният час трябва да бъде преди крайния час!');
            return;
        }

        const data = JSON.stringify({
            username: current_user, role: userRole, date: date, startTime: startTime, endTime: endTime,
            criteria1: criteria1, criteria2: criteria2, criteria3: criteria3
        });

        const response = await fetch('../py/get_rooms.py', { //May need to redart the PATH 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        const response_data = await response.json();

        const container = document.getElementById('roomSelectionForm');

        const radioGroupName = 'roomSelection';

        let roomSeqNumber = 1;

        response_data.rooms.forEach(room => {
            const roomElement = document.createElement('section');

            roomElement.innerHTML = `
            <label>
                <input type="radio" name="${radioGroupName}" value="${room.number}">
                <strong>Стая/Зала ${roomSeqNumber}: ${room.number}</strong>
            </label>
            <p>Вид стая - ${room.criteria1}</p>
            <p>Вид дъска - ${room.criteria2}</p>
            <p>Налична мултимедия - ${room.criteria3}</p>
            <p>Капацитет - ${room.seatsCount}</p>
            `;

            container.appendChild(roomElement);
            roomSeqNumber++;
        });

        const containerSubmit = document.createElement('p');
        containerSubmit.innerHTML = `
        <button type="submit" class= "fixed-footer">Запази стая</button>
        `;
        container.appendChild(containerSubmit);
        
        reserved_room = document.getElementById('roomSelectionForm');

        reserved_room.addEventListener('submit', async function () {

                event.preventDefault();

                const selectedRoom = document.querySelector('input[name="roomSelection"]:checked');
                if (!selectedRoom) {
                    alert('Моля, изберете стая преди да запазите!');
                    return;
                }

                const roomNumber = selectedRoom.value;                

                dateSaved = date_time_now();

                roomDataJSON = JSON.stringify({
                    username: current_user, role: userRole, roomNumber: roomNumber, date: date,
                    startTime: startTime, endTime: endTime, dateReservation: dateSaved,
                });
                    
                const roomDataJSON = JSON.stringify(reviewData);

                const response = await fetch('../py/reserve_room.py', { //May need to redart the PATH 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: roomDataJSON
                });

                final_response = await response.json();

                if (final_response.success) {
                    alert('Стаята/Залата беше успешно запазена!');

                    window.location.href = '../html/room_search.html';

                } else {
                    alert('Възникна грешка! Заявката не беше запазена!');
                }

        });
    });
});
    
