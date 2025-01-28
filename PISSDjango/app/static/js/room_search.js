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
    for (let i = 6 + offset; i < 23 + offset; i++) {
        const time = `${i.toString().padStart(2, '0')}:00`; // Format as "00:00"
        timeOptions.push(`<option value="${time}">${time}</option>`);
    }
    return timeOptions.join('');

}




document.addEventListener('DOMContentLoaded', async function () {

    const token = localStorage.getItem('authToken');
    let current_user = undefined;
    if (token!=null){
        try {
            const decoded = jwt_decode(token);
            const username = decoded.username || decoded.user_id; 
            current_user = username;
        } catch (e) {
            console.error("Error decoding token:", e);
        }
    }


    // We could change it to just not sending anything in JSON depending on how you made the tokens work
    const referedPage = current_user === undefined ? 'начално' : 'главно';
    const referedPageSite = current_user === undefined ? "/static/html/main.html" : "/static/html/index.html";
    const headerText = "Обратно към " + referedPage + " меню";
    const headerButton = document.querySelector('header > a');
    headerButton.textContent = headerText
    headerButton.setAttribute("href", referedPageSite);

    const startTimeSelect = document.getElementById('startTime');
    const endTimeSelect = document.getElementById('endTime');

    startTimeSelect.innerHTML = generateTimeOptions();
    endTimeSelect.innerHTML = generateTimeOptions(1);

    room_filters = document.getElementById('timeSelectionForm');

    room_filters.addEventListener('submit', async function () {
        const container = document.getElementById('roomSelectionForm');
        
        event.preventDefault();

        const date = new Date(document.getElementById('datePicker').value).toISOString().split('T')[0];
        const startTime = document.getElementById('startTime').value;
        const endTime = document.getElementById('endTime').value;
        const isComputer = document.getElementById('isComputer').value; //1 - isComp, 0 - is normal
        const hasWhiteBoard = document.getElementById('white').checked;
        const hasBlackBoard = document.getElementById('black').checked;
        const hasInteractiveBoard = document.getElementById('interactive').checked;
        const hasMedia = document.getElementById('media').checked; // 1 has media, 0 - has no media
        const minCapacity = document.getElementById('capacity').value;
        console.log(date, startTime, endTime, isComputer, hasWhiteBoard, hasBlackBoard, hasInteractiveBoard, hasMedia, minCapacity);
        if (startTime >= endTime) {
            alert('Началният час трябва да бъде преди крайния час!');
            return;
        }
        let data;
        if(token == null){    
            data = JSON.stringify({ "date": date, "startTime": startTime, "endTime": endTime, "isComputer": isComputer, "hasWhiteBoard": hasWhiteBoard,
                "hasBlackBoard": hasBlackBoard, "hasInteractiveBoard": hasInteractiveBoard, "hasMedia": hasMedia,"minCapacity": minCapacity
            });
        }
        else{
            data = JSON.stringify({date: date, startTime: startTime, endTime: endTime, isComputer: isComputer,
                hasWhiteBoard: hasWhiteBoard, hasBlackBoard: hasBlackBoard, hasInteractiveBoard: hasInteractiveBoard,
                hasMedia: hasMedia,minCapacity: minCapacity
            });
        }

        const response = await fetch('/api/get_rooms/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        const response_data = await response.json();

        const topicContainer = document.getElementById('sessionTopic');
        topicContainer.display.style = 'none';
        const header = document.querySelector('#roomSelectionForm>h2');
        topicContainer.removeAttribute('required');

        let roomSeqNumber = 1;
        response_data.rooms.forEach(room => {
            container.style.display = 'flex';
            topicContainer.setAttribute('required', "true"); // reset in order when we have no rooms to reserve
            header.style.display = 'block';
            topicContainer.display.style = 'block';

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

            const roomElement = document.createElement('section');
            roomElement.setAttribute('data', room.id);
            roomElement.style.display = 'flex';
            roomElement.style.justifyContent = "center";
            roomElement.style.alignItems = "center";

            const roomDescription = document.createElement('div');
            roomDescription.style.flexGrow = 1
            roomDescription.innerHTML = `
            <strong> ${roomSeqNumber}. Стая/Зала: ${room.roomNumber}</strong>
            <p>Вид стая - ${isComp}</p>
            <p>Вид дъска:</p>
            <ul type='none'>
            <li>    Черна - ${black}</li>
            <li>    Бяла - ${white}</li>
            </ul>
            <p>    Интерактивна - ${inter}</p>
            <p>Налична мултимедия - ${media}</p>
            <p>Капацитет - ${room.seatsCount}</p>
            `;
            roomElement.appendChild(roomDescription);

            if (token != null) {
                //topicContainer.removeAttribute('hidden');
                topicContainer.style.display = 'flex';
                topicContainer.setAttribute('required', "true");
                const topic = topicContainer.value;
                const reserveButton = document.createElement('button');
                reserveButton.textContent = 'Резервирай';
                reserveButton.style.flexGrow = 1


                reserveButton.addEventListener('click', async function () {
                    const room_id = room.id;
                    const data = JSON.stringify({ room_id: room_id, date: date, startTime: startTime, endTime: endTime, token: token, topic: topic });
                    const response = await fetch('/api/reserve_room/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: data
                    });

                    if (response.status === 200) {
                        alert('Успешно резервирахте стаята!');
                        window.location.href = '/static/html/index.html';
                    } else {
                        alert('Неуспешно резервиране на стаята!');
                        window.location.href = '/static/html/get_rooms.html';
                    }
                });
                
                roomElement.appendChild(reserveButton);
            }

            
            container.appendChild(roomElement);
            roomSeqNumber++;
        });

        
    });
});
    
