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

    const lessonName = document.getElementById('lesson-name').value;
    if (lessonName !== "") { // If a concrete subject has been selected, add it to the query (if not we will return all subjects)
        data.lessonName = lessonName;
    }
    return data;
}

document.addEventListener('DOMContentLoaded', async function () {
    generateBackMenuButton();
    disallowPastDates();

    document.getElementById('LessonSearchForm').addEventListener('submit', async function (event) {
        event.preventDefault();
        const data = generateRoomRequestBody();

        const response = await fetch('/api/get_lessons/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const response_data = await response.json();

        const container = document.getElementById('LessonDetailsForm');

        const radioGroupName = 'lessonSelection';
        
        let lessonSeqNumber = 1;

        response_data.lessons.forEach(lesson => {
            let lessonElement = document.createElement('section');

            lessonType = lesson.lectureType;
            console.log(lessonType);
            let type;
            if (lessonType == "Lecture") {
                type = "Лекция";
            }  else if (lessonType == "Practicum"){
                type = "Практикум";
            } else if (lessonType == "Seminar"){
                type = "Семинар";
            } else if (lessonType == "GuestLecture"){
                type = "Гост лекция";
            }

            lessonElement.innerHTML = `
            <label>
                <input type="radio" name="${radioGroupName}" value="${lessonSeqNumber}">
                <strong>${lessonSeqNumber}. ${lesson.lessonName}</strong>
                <strong>Стая/Зала: ${lesson.roomNumber}</strong>
            </label>
            <p>Ден - ${lesson.date}</p>
            <p>Начален час - ${lesson.startTime}</p>
            <p>Краен час - ${lesson.endTime}</p>
            <p>Вид занятие - ${type}</p>
            `;
            lessonElement.setAttribute("data-id", lesson.id);
            container.appendChild(lessonElement);
            lessonSeqNumber++;
        });

        const containerSubmit = document.createElement('p');
        containerSubmit.innerHTML = `
        <button type="submit" class= "fixed-footer">Отбележи присъствие</button>
        `;
        container.appendChild(containerSubmit);

        attended_lesson = document.getElementById('lessonSelectionForm');

        attended_lesson.addEventListener('submit', async function () {

            const selectedLesson = document.querySelector('input[name="lessonSelection"]:checked');

            if (!selectedLesson) {
                alert('Моля, изберете урок преди да запазите!');
                return;
            }

            const lessonSeqNumber = selectedLesson.value;

            const selectedLessonDetails = response_data.lessons[lessonSeqNumber - 1];  

            if (!selectedLessonDetails) {
                alert('Грешка при извличане на информация за избраната стая!');
                return;
            }

            const dateSaved = date_time_now();

            const lessonDataJSON = JSON.stringify({
                username: current_user,
                lessonName: selectedLessonDetails.name,
                date: selectedLessonDetails.date,
                startTime: selectedLessonDetails.startTime,
                endTime: selectedLessonDetails.endTime,
                lectureType: selectedLessonDetails.lectureType,
                dateAttendanceChecked: dateSaved,
            });

            const response = await fetch('/api/take_attendance/', { //May need to redart the PATH 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: lessonDataJSON
            });

            final_response = await response.json();

            if (final_response.success) {
                alert('Успешно отчетено присъствие!');

                window.location.href = '/static/html/lesson_search.html';

            } else {
                alert('Възникна грешка! Присъствието не беше отчетено!');
            }

        });
    });
});

