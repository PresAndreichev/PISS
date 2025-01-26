document.addEventListener('DOMContentLoaded', async function () {

    const current_user = sessionStorage['username'];
    const userRole = sessionStorage['role'];

    lesson_filters = document.getElementById('LessonSearchForm');

    lesson_filters.addEventListener('submit', async function () {

        event.preventDefault();

        const lessonName = document.getElementById('lesson-name').value;
        const startDate = new Date(document.getElementById('startDate').value);
        const endDate = new Date(document.getElementById('endDate').value);
        const type = document.getElementById('lecture-type').value; //lecture, practical, theoretical, all

        if (startDate >= endDate) {
            alert('Началната дата трябва да бъде преди крайната!');
            return;
        }

        const data = JSON.stringify({
            username: current_user, role: userRole, startDate: startDate, endDate: endDate,
            lessonName: lessonName, lessonType: type
        });

        const response = await fetch('../py/get_lesson.py', { //May need to redart the PATH 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        const response_data = await response.json();

        const container = document.getElementById('LessonDetailsForm');

        const radioGroupName = 'lessonSelection';

        let lessonSeqNumber = 1;

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
                role: userRole,
                lessonName: selectedLessonDetails.name,
                date: selectedLessonDetails.date,
                startTime: selectedLessonDetails.startTime,
                endTime: selectedLessonDetails.endTime,
                lectureType: selectedLessonDetails.lectureType,
                dateAttendanceChecked: dateSaved,
            });

            const response = await fetch('../py/take_attendance.py', { //May need to redart the PATH 
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

                window.location.href = '../html/lesson_search.html';

            } else {
                alert('Възникна грешка! Присъствието не беше отчетено!');
            }

        });
    });
});

