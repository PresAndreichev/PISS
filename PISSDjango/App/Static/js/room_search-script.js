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

function generateTimeOptions(offset = 0) {
    const timeOptions = [];
    for (let i = 6 + offset; i < 24 + offset; i++) {
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

    startTimeSelect.innerHTML = generateTimeOptions();
    endTimeSelect.innerHTML = generateTimeOptions(1);

    room_filters = document.getElementById('timeSelectionForm');

    room_filters.addEventListener('submit', async function () {

        event.preventDefault();

        const date = new Date(document.getElementById('datePicker').value);
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;
        const isComputer = document.getElementById('isComputer').value; //1 - isComp, 0 - is normal
        const hasWhiteBoard = document.getElementById('white').checked;
        const hasBlackBoard = document.getElementById('white').checked;
        const hasInteractiveBoard = document.getElementById('white').checked;
        const hasMedia = document.getElementById('media').checked; // 1 has media, 0 - has no media

        if (startTime >= endTime) {
            alert('Началният час трябва да бъде преди крайния час!');
            return;
        }

        const data = JSON.stringify({
            username: current_user, role: userRole, date: date, startTime: startTime, endTime: endTime,
            isComputer: isComputer, hasWhiteBoard: hasWhiteBoard, hasBlackBoard: hasBlackBoard, hasInteractiveBoard: hasInteractiveBoard, hasMedia: hasMedia
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

            let isComp, black, white, inter, media;

            if (room.isComputer) {
                isComp = "Компютърна";
            } else {
                isComp = "Обикновена";
            }

            if (room.hasWhiteBoard) {
                white = "Да";
            } else {
                white = "Не";
            }

            if (room.hasBlackBoard) {
                black = "Да";
            } else {
                black = "Не";
            }

            if (room.hasInteractiveBoard) {
                inter = "Да";
            } else {
                inter = "Не";
            }

            if (room.hasMedia) {
                media = "Да";
            } else {
                media = "Не";
            }

            roomElement.innerHTML = `
            <label>
                <input type="radio" name="${radioGroupName}" value="${room.roomNumber}">
                <strong>${roomSeqNumber}. Стая/Зала: ${room.roomNumber}</strong>
            </label>
            <p>Вид стая - ${isComp}</p>
            <p>Вид дъска - </p>
            <p>    Черна - ${black}</p>
            <p>    Бяла - ${white}</p>
            <p>    Интерактивна - ${inter}</p>
            <p>Налична мултимедия - ${media}</p>
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
    
