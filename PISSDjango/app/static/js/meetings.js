function disallowPastDates() {
    const currDate = new Date().toISOString().split('T')[0];
    document.getElementById("startDate").setAttribute('min', currDate);
    document.getElementById("endDate").setAttribute('min', currDate);
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

function generateBackMenuButton() {
    const token = localStorage.getItem('authToken');
    const current_user = getCurrentUser(token);

    const referedPage = current_user === undefined ? 'начално' : 'главно';
    const referedPageSite = current_user === undefined ? "/static/html/main.html" : "/static/html/index.html";
    const headerText = "Обратно към " + referedPage + " меню";
    const headerButton = document.querySelector('header > a');
    headerButton.textContent = headerText
    headerButton.setAttribute("href", referedPageSite);
}

function getTodayUNIXTime() {
    let todayUnixTime = new Date();
    todayUnixTime.setUTCHours(0, 0, 0, 0);
    return todayUnixTime.getTime();
}

function getParsedStartDate(todayUnixTime) {
    const enteredStartDate = document.getElementById('startDate').value;
    let startDate = enteredStartDate === "" ? new Date(todayUnixTime) : new Date(enteredStartDate);
    
    if (startDate.getTime() < todayUnixTime) {
        startDate = new Date(todayUnixTime);
    }
    return startDate;
}

function getParsedEndDate(todayUnixTime, startDate) {
    const defaultEndDate = new Date(todayUnixTime);
    const DEFAULT_MAX_INTERVAL_DAYS = 3;
    defaultEndDate.setDate(defaultEndDate.getDate() + DEFAULT_MAX_INTERVAL_DAYS) // JS automatically does the % length

    const enteredEndDate = document.getElementById('endDate').value;
    let endDate = enteredEndDate === "" ? new Date(defaultEndDate.getTime()) : new Date(enteredEndDate);
    if (endDate.getTime() < startDate.getTime()) {
        endDate = new Date(defaultEndDate.getTime());
    }
    return endDate;
}

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function generateRoomRequestBody() {
    const todayUnixTime = getTodayUNIXTime();
    const startDateObj = getParsedStartDate(todayUnixTime); // startDate.toISOString().split('T')[0];
    const startDate = formatDate(startDateObj);
    const endDate = formatDate(getParsedEndDate(todayUnixTime, startDateObj));

    let data = { 
        "startDate": startDate,
        "endDate": endDate,
    };

    const roomNumber = document.getElementById('room-number').value;
    if (roomNumber !== "") { // If a concrete room has been selected, add it to the query
        data.roomNumber = Number(roomNumber);
    }

    const token = localStorage.getItem('authToken');
    if (token !== null) { // Add the token to the query if the person has a valid one
        data.token = token;
    }
    
    return data;
}

async function sendMeetingsQuery() {
    const data = generateRoomRequestBody();
    const response = await fetch('/api/get_meetings/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

// event (nelesson), sys startTime, endTIme (ako ne sa podadeni, start e dnes) endDate sled 3 dni, hostID - ako ne vseki (vajno - da ne izlizat eventi, za koito sum zapisan ili sum host), roomId - ako ne za vsqka
//start_time, end_time, date, host_ID/or not, room_id/not

function parseReturnedTimeFromServer(time) {
    return time.split(':').slice(0,2).join(':');
}

function generateMeetingDescription(meeting, meetingSeqNumber) {
    const startTime = parseReturnedTimeFromServer(meeting.startTime)
    const endTime = parseReturnedTimeFromServer(meeting.endTime)

    const description = document.createElement("article");
    description.innerHTML = `
    <header>
        <h3>№${meetingSeqNumber}.    ${meeting.topic}</h3>
        <h4>Стая/Зала: ${meeting.roomNumber}</h4>
        <h4>Домакин: ${meeting.hostUsername}</h4>
    </header>
    <p>Ден - ${meeting.date}</p>
    <p>Начален час - ${startTime}</p>
    <p>Краен час - ${endTime}</p>
    <p>Заети ${meeting.attendeesCount} места от общо ${meeting.roomCapacity}</p>
    `;
    return description;
}

function generateMeetingAttendButton(meeting, token) {
    // create a button, only if we have valid token
    if (token === null) 
        return null;

    const reserveButton = document.createElement('button');
    reserveButton.textContent = 'Присъствай!';
    reserveButton.style.flexGrow = 1

    // Listen for the event and show the button only if the user is registered, otherwise don't show it
    reserveButton.addEventListener('click', async function (event) {
        const roomEventId = event.target.parentElement.getAttribute("data-id");
        // we MUST extract the values FROM INSIDE this lambda function, otherwise context is lost when invoking event!
        const realToken = localStorage.getItem('authToken');

        const data = JSON.stringify({roomEventId: roomEventId, token: realToken});

        const response = await fetch('/api/take_attendance/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });
        
        if (response.status === 200) {
            alert('Успешно се записахте за събитието');
        } else {
            // He has already registered or the capacity of the room has been fulfilled!
            alert('Не успяхте да се запишете за урока - вече сте записан или местата са свършили ;(');
        }

        // Nevermind how the operation went, we should get the latest result (either we have reached a capacity or need to know which rooms are still available
        document.getElementById('lessonSelectionForm').submit();
    })

    return reserveButton;
}

function generateLessonElement(meeting, meetingSeqNumber, token) {
    const meetingElement = document.createElement('section');
    meetingElement.setAttribute("data-id", meeting.id);
    meetingElement.classList.add("lesson-container");

    const description = generateMeetingDescription(meeting, meetingSeqNumber);
    meetingElement.appendChild(description);
    
    const attendButton = generateMeetingAttendButton(meeting, token);
    if (attendButton !== null) { // if we have token, a button would be created
        meetingElement.appendChild(attendButton);
    }
    return meetingElement;
}

document.addEventListener('DOMContentLoaded', async function () {
    generateBackMenuButton();
    disallowPastDates();

    document.getElementById('lessonSelectionForm').addEventListener('submit', async function (event) {
        event.preventDefault();
        const meetingsContainer = document.getElementById('LessonDetailsForm');
        meetingsContainer.innerHTML = ''; // reset the container after previous query
        meetingsContainer.setAttribute("hidden", true);
        
        const responseData = await sendMeetingsQuery();
        if (responseData.events.length === 0) {
            alert("Няма събития в посочения интервал!");
            return;
        }
        meetingsContainer.removeAttribute("hidden");

        let meetingSeqNumber = 1;
        const token = localStorage.getItem('authToken');
        responseData.events.forEach(meeting => {
            const meetingElement = generateLessonElement(meeting, meetingSeqNumber, token);
            meetingsContainer.appendChild(meetingElement);
            meetingSeqNumber++;
        });
    });
});