﻿function getUserNameFromToken() {
    const token = localStorage.getItem("authToken");
    if (token) {
        try {
            const decoded = jwt_decode(token);
            const username = decoded.username || decoded.user_id;
            return username;
        } catch (e) {
            console.error("Error decoding token:", e);
        }
    } else {
        console.error("No token found");
    }
    return undefined;
}

async function greet() {
    const greeting = document.getElementById("greeting");
    greeting.textContent = "Добре дошли, " + getUserNameFromToken() + "!";
}

function parseReturnedTimeFromServer(time) {
    return time.split(':').slice(0,2).join(':');
}

function generateMeetingDescription(event, eventNumber, userUserName) {
    const startTime = parseReturnedTimeFromServer(event.startTime);
    const endTime = parseReturnedTimeFromServer(event.endTime);
    const hostName = event.hostUserName === userUserName ? "Вие" : event.hostUserName;

    const description = document.createElement("article");
    description.innerHTML = `
    <header>
        <h3>№${eventNumber}.    ${event.topic}</h3>
        <h4>Стая/Зала: ${event.roomNumber}</h4>
        <h4>Домакин: ${hostName}</h4>
    </header>
    <p>Ден - ${event.date}</p>
    <p>Начален час - ${startTime}</p>
    <p>Краен час - ${endTime}</p>
    <p>Заети ${event.attendeesCount} места от общо ${event.totalSeats}</p>
    `;
    return description;
}

function getLessonTypeBasedOnReturnedJSON(lessonTypeFromJSON) {
    const lessonParser = {
        "Lecture": "Лекция",
        "Practicum": "Практикум",
        "Seminar": "Семинар",
        "GuestLecture": "Гост-лекция"
    };

    return lessonParser[lessonTypeFromJSON];
}

function extendContainerNodeWithLessonAttributes(event, eventElement) {
    if (!'lectureType' in event) {
        return eventElement;
    }

    const headerOfEventElement = eventElement.getElementsByTagName("header")[0];
    const lectureType = document.createElement("h4");
    lectureType.textContent = getLessonTypeBasedOnReturnedJSON(eventElement.lectureType)
    headerOfEventElement.appendChild(lectureType);

    const subjectNode = document.createElement("h4");
    subjectNode.textContent = getLessonTypeBasedOnReturnedJSON(eventElement.subjectName)
    headerOfEventElement.appendChild(subjectNode);
}

function generateEventCard(event, eventNumber, userUserName) {
    const eventCard = document.createElement("section");
    eventCard.setAttribute("data-id", event.id);
    eventCard.classList.add("event");
    if (event.hostUserName === userUserName) {
        eventCard.classList.add("host");
    }

    const descriptionNode = generateMeetingDescription(event, eventNumber, userUserName);
    extendContainerNodeWithLessonAttributes(event, descriptionNode);
    eventCard.appendChild(descriptionNode);

    // ADD BUTTONS HERE
    return eventCard;
}

document.addEventListener('DOMContentLoaded', async function () {
    greet();

    const token = localStorage.getItem('authToken');
    const data = JSON.stringify({token: token});
    const response = await (await fetch('/api/index_visualization/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: data
    })).json();
    console.log(response);

    const shadowDOMNode = document.createDocumentFragment();

    let eventNumber = 1;
    const userUserName = getUserNameFromToken();
    response.events.forEach(event => {
        console.log(event);
        const eventElement = generateEventCard(event, eventNumber, userUserName);
        console.log(eventElement);
        shadowDOMNode.appendChild(eventElement);
        eventNumber++;
    });
    console.log("for-a mina")
    document.querySelectorAll("body > section")[1].appendChild(shadowDOMNode);
});
