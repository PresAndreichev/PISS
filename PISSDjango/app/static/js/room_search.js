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

function getCurrentUser(token) {
    if (token !== null) {
        try {
            const decoded = jwt_decode(token);
            const username = decoded.username || decoded.user_id; 
            return username;
        } catch (e) {
            return undefined;
        }
    }
    return undefined;
}

function generateBackMenuButton(current_user) {
    const referedPage = current_user === undefined ? 'начално' : 'главно';
    const referedPageSite = current_user === undefined ? "/static/html/main.html" : "/static/html/index.html";
    const headerText = "Обратно към " + referedPage + " меню";
    const headerButton = document.querySelector('header > a');
    headerButton.textContent = headerText
    headerButton.setAttribute("href", referedPageSite);
}

function generateInputTimeOptions() {
    const startTimeSelect = document.getElementById('startTime');
    const endTimeSelect = document.getElementById('endTime');
    startTimeSelect.innerHTML = generateTimeOptions();
    endTimeSelect.innerHTML = generateTimeOptions(1);
}

function generateRoomRequestBody(token) {
    const date = new Date(document.getElementById('datePicker').value).toISOString().split('T')[0];
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const isComputer = Number(document.getElementById('isComputer').value); //1 - isComp, 0 - is normal
    const hasWhiteBoard = document.getElementById('white').checked;
    const hasBlackBoard = document.getElementById('black').checked;
    const hasInteractiveBoard = document.getElementById('interactive').checked;
    const hasMedia = document.getElementById('media').checked; // 1 has media, 0 - has no media
    const minCapacity = Number(document.getElementById('capacity').value);

    if (startTime >= endTime) {
        alert('Началният час трябва да бъде преди крайния час!');
        return;
    }

    let data = { 
        "date": date, 
        "startTime": startTime, 
        "endTime": endTime, 
        "isComputer": isComputer, 
        "hasWhiteBoard": hasWhiteBoard,
        "hasBlackBoard": hasBlackBoard, 
        "hasInteractiveBoard": hasInteractiveBoard, 
        "hasMedia": hasMedia,
        "minCapacity": minCapacity
    };

    if (token !== null) { // Add the token to the query if the person has a valid one
        data.token = token;
    }
    return data;
}

function toggleResultsVisibility(hideThem, resultNode, headerNode, topicNode, roomListNode, token) {
    if (hideThem) {
        resultNode.style.display = "none";
        roomListNode.style.display = "none";
        roomListNode.innerHTML = ''; // remove all children

        headerNode.style.display = "none";

        topicNode.style.display = "none";
        topicNode.removeAttribute('required');
    } else {
        resultNode.style.display = "flex";
        headerNode.style.display = "block";

        // In order to show the topicNode from which we add text to the topic, we have to be logged in!
        if (token !== null) {
            topicNode.style.display = "block";
            topicNode.setAttribute('required', true);
        }
        roomListNode.style.display = "block";
    }
}

function extractRoomValues(returnedRoom) {
    const isComputerRoom = returnedRoom.isComputer ? "Компютърна" : "Обикновена";
    const hasBlackBoard = returnedRoom.hasBlackBoard ? "Да" : "Не";
    const hasWhiteBoard = returnedRoom.hasWhiteBoard ? "Да" : "Не";
    const hasInteractiveBoard = returnedRoom.hasInteractiveBoard ? "Да" : "Не";
    const hasMedia = returnedRoom.hasMedia ? "Да" : "Не";

    return {
        isComputerRoom: isComputerRoom,
        hasBlackBoard: hasBlackBoard,
        hasWhiteBoard: hasWhiteBoard,
        hasInteractiveBoard: hasInteractiveBoard,
        hasMedia: hasMedia
    };
}

function buildRoomDescription(room, numberInResultSet) {
    const roomCharacteristics = extractRoomValues(room);
    const roomDescriptionNode = document.createElement('div');
    roomDescriptionNode.style.flexGrow = 1
    roomDescriptionNode.innerHTML = `
        <strong>№${numberInResultSet}. Стая/Зала: ${room.roomNumber}</strong>
        <p>Вид стая - ${roomCharacteristics.isComputerRoom}</p>
        <p>Вид дъска:</p>
        <ul type='none'>
            <li>Черна - ${roomCharacteristics.hasBlackBoard}</li>
            <li>Бяла - ${roomCharacteristics.hasWhiteBoard}</li>
        </ul>
            <p>    Интерактивна - ${roomCharacteristics.hasInteractiveBoard}</p>
            <p>Налична мултимедия - ${roomCharacteristics.hasMedia}</p>
            <p>Капацитет - ${room.seatsCount}</p>        
        `;
    roomDescriptionNode.setAttribute("data-id", room.id);
    return roomDescriptionNode
}

function buildReserveRoomButton() {
    const reserveButton = document.createElement('button');
    reserveButton.textContent = 'Резервирай';
    reserveButton.style.flexGrow = 1

    reserveButton.addEventListener('click', async function (event) {
        const room_id = event.target.parentElement.children[0].getAttribute("data-id");
        // we MUST extract the values FROM INSIDE this lambda function, otherwise context is lost when invoking event!
        const token = localStorage.getItem('authToken');
        const unessentialData = generateRoomRequestBody(token);
        const topic = document.getElementById('sessionTopic').value;
        if (topic === "") {
            alert("No text added into the topic!");
            return;
        }

        const data = JSON.stringify({ room_id: room_id, date: unessentialData.date, startTime: unessentialData.startTime, 
            endTime: unessentialData.endTime, token: token, topic: topic });

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
            // REFACTOR THE HTMLs here! - maybe sent another request for rooms available then
            window.location.href = '/static/html/get_rooms.html';
        }
    });

    return reserveButton;
}

function buildSingleRoomNode(room, roomNumberForPrinting, token) {
    const roomElement = document.createElement('section');
    roomElement.setAttribute('data-id', room.id);
    roomElement.style.display = 'flex';
    roomElement.style.justifyContent = "center";
    roomElement.style.alignItems = "center";

    const roomDescription = buildRoomDescription(room, roomNumberForPrinting);
    roomElement.appendChild(roomDescription);

    if (token != null) {
        const reserveButton = buildReserveRoomButton();
        roomElement.appendChild(reserveButton);
    }
    return roomElement;
}

async function executeSearch(event) {
    event.preventDefault();

    const resultNode = document.getElementById('roomSelectionForm');
    const headerNode = document.querySelector('#roomSelectionForm > h2');
    const topicNode = document.getElementById('sessionTopic');
    const roomsListNode = document.getElementById('roomList');
    const token = localStorage.getItem('authToken');
    toggleResultsVisibility(true, resultNode, headerNode, topicNode, roomsListNode, token);

    const stringifiedData = JSON.stringify(generateRoomRequestBody(token));
    const response = await fetch('/api/get_rooms/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: stringifiedData
    });
    const responseData = await response.json();

    const rooms = responseData.rooms;
    if (rooms.length > 0) {
        toggleResultsVisibility(false, resultNode, headerNode, topicNode, roomsListNode, token);

        // NB! - using ShadowDOM (a.k.a DocFragments) is MUCH faster than appending to the direct parent when done multiple times
        const shadowDomContainer = document.createDocumentFragment();
        let roomNumberForPrinting = 1;
        rooms.forEach(room => {
            const roomNode = buildSingleRoomNode(room, roomNumberForPrinting, token);
            shadowDomContainer.appendChild(roomNode);
            roomNumberForPrinting++;
        });
        roomsListNode.appendChild(shadowDomContainer);
    } else {
        alert("No free rooms are available in the desired time slot :(");
    }   
}

document.addEventListener('DOMContentLoaded', async function () {
    const token = localStorage.getItem('authToken');
    let current_user = getCurrentUser(token);
    generateBackMenuButton(current_user);
    generateInputTimeOptions();
    document.getElementById('timeSelectionForm')
      .addEventListener('submit', executeSearch);
});