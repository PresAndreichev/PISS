﻿async function generateSubjectsList() {
    const subjectsList = await (await fetch('/api/list_subjects/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    })).json();

    const shadowDOMNode = document.createDocumentFragment();
    const firstEmptyChild =  document.createElement("option");
    shadowDOMNode.appendChild(firstEmptyChild);

    subjectsList.subjects.forEach(subject => {
        shadowDOMNode.appendChild(generateSubjectOption(subject));
    })
    document.getElementById("lesson-name").appendChild(shadowDOMNode);
}

function generateSubjectOption(subject) {
    const optionNode = document.createElement("option");
    optionNode.textContent = subject.subjectName;
    optionNode.value = subject.subjectId;
    return optionNode;
}

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
    const DEFAULT_MAX_INTERVAL_MONTHS = 1;
    defaultEndDate.setMonth(defaultEndDate.getMonth() + DEFAULT_MAX_INTERVAL_MONTHS) // JS automatically does the % length

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

    const type = document.getElementById('lecture-type').value; //lecture, practical, theoretical, all, guest-lecture

    let data = { 
        "startDate": startDate,
        "endDate": endDate,
        "lessonType": type,
    };

    const lessonId = document.getElementById('lesson-name').value;
    if (lessonId !== "") { // If a concrete subject has been selected, add it to the query (if not we will return all subjects)
        data.lessonId = Number(lessonId);
    }

    const token = localStorage.getItem('authToken');
    if (token !== null) { // Add the token to the query if the person has a valid one
        data.token = token;
    }
    
    return data;
}

async function sendLessonsQuery() {
    const data = generateRoomRequestBody();
    const response = await fetch('/api/get_lessons/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
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

function generateLessonDescription(lesson, lessonSeqNumber) {
    const type = getLessonTypeBasedOnReturnedJSON(lesson.lectureType)
    const lessonDescription = document.createElement("article");
    lessonDescription.innerHTML = `
    <header>
        <h3>№${lessonSeqNumber}. ${lesson.lessonName}</h3>
        <h4>Стая/Зала: ${lesson.roomNumber}</h4>
    </header>
    <p>Ден - ${lesson.date}</p>
    <p>Начален час - ${lesson.startTime}</p>
    <p>Краен час - ${lesson.endTime}</p>
    <p>Вид занятие - ${type}</p>
    `;
    return lessonDescription;
}

function generateLessonAttendButton(lesson, token) {
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

function generateLessonElement(lesson, lessonSeqNumber, token) {
    const lessonElement = document.createElement('section');
    lessonElement.setAttribute("data-id", lesson.id);
    lessonElement.classList.add("lesson-container");

    const lessonDescription = generateLessonDescription(lesson, lessonSeqNumber);
    lessonElement.appendChild(lessonDescription);
    
    const attendButton = generateLessonAttendButton(lesson, token);
    if (attendButton !== null) { // if we have token, a button would be created
        lessonElement.appendChild(attendButton);
    }
    return lessonElement;
}

document.addEventListener('DOMContentLoaded', async function () {
    await generateSubjectsList();
    generateBackMenuButton();
    disallowPastDates();

    document.getElementById('lessonSelectionForm').addEventListener('submit', async function (event) {
        event.preventDefault();
        const responseData = await sendLessonsQuery();
        const lessonsContainer = document.getElementById('LessonDetailsForm');
        lessonsContainer.innerHTML = ''; // reset the container after previous query
        lessonsContainer.setAttribute("hidden", true);
        
        if (responseData.lessons.length === 0) {
            alert("Няма уроци спрямо зададените критерии!");
            return;
        }
        lessonsContainer.removeAttribute("hidden");

        let lessonSeqNumber = 1;
        const token = localStorage.getItem('authToken');
        responseData.lessons.forEach(lesson => {
            const lessonElement = generateLessonElement(lesson, lessonSeqNumber, token);
            lessonsContainer.appendChild(lessonElement);
            lessonSeqNumber++;
        });
    });
});