document.addEventListener('DOMContentLoaded', async function () {

    // We could change it to just not sending anything in JSON depending on how you made the tokens work
    const current_user = null;
    const userRole = 0;

    lesson_filters = document.getElementById('LessonSearchForm');

    lesson_filters.addEventListener('submit', async function () {

        event.preventDefault();

        const lessonName = document.getElementById('lesson-name').value;
        const startDate = new Date(document.getElementById('startDate').value);
        const endDate = new Date(document.getElementById('endDate').value);
        const type = document.getElementById('lecture-type').value; //lecture, practical, theoretical, all

        if (startDate > endDate) {
            alert('Началната дата трябва да бъде преди крайната!');
            return;
        }
                
        const data = JSON.stringify({
            username: current_user, role: userRole, startDate: startDate, endDate: endDate,
            lessonName: lessonName, lessonType: type
        });

        const response = await fetch('/api/get_lesson', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        const response_data = await response.json();

        const container = document.getElementById('LessonList');

        let lessonSeqNumber = 1;

        note = container.createElement('section');

        note.innerHTML = `<p>!Трябва да сте регистриран потребител, ако искате да запазите зала!</p>
                <p>Ако вече имате регистрация, влезте от тук: <a href="/static/html/login.html" class="back_buttons">Вход</a></p>
                <p>Ако още нямате регистрация, влезте от тук: <a href="/static/html/register.html" class="back_buttons">Регистрация</a></p>
         `;

        container.appendChild(note);

        response_data.lessons.forEach(lesson => {
            const lessonElement = document.createElement('section');

            lessonType = lesson.lectureType;
            type;
            if (lessonType == "lecture") {
                type = "Лекция";
            }  else if (lessonType == "practical"){
                type = "Практикум";
            } else if (lessonType == "theoretical"){
                type = "Семинар";
            } else if (lessonType == "guest-lecture"){
                type = "Гост лекция";
            }

            lessonElement.innerHTML = `           
            <strong>${lessonSeqNumber}. ${lesson.lessonName}</strong>
            <p>Стая/Зала: ${lesson.roomNumber}</p>
            <p>Ден - ${lesson.date}</p>
            <p>Начален час - ${lesson.startTime}</p>
            <p>Краен час - ${lesson.endTime}</p>
            <p>Вид занятие - ${type}</p>
            `;

            container.appendChild(lessonElement);
            lessonSeqNumber++;
        });

        
    });
});

