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

let userRole;

function updateHrefBasedOnRole() {
    userRole = sessionStorage.getItem('role');

    const mainMenuLink = document.querySelector('a.button');

    if (userRole === 1) {
        mainMenuLink.href = 'student_index.html';
    } else if (userRole === 2) {
        mainMenuLink.href = 'teacher_index.html';
    }  else {
        
        mainMenuLink.href = '.';
    }
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

    current_user = sessionStorage['username'];

    updateHrefBasedOnRole();
    const startTimeSelect = document.getElementById('startTime');
    const endTimeSelect = document.getElementById('endTime');

    // Populate the dropdowns
    const optionsHTML = generateTimeOptions();
    startTimeSelect.innerHTML = optionsHTML;
    endTimeSelect.innerHTML = optionsHTML;

    const data = JSON.stringify({ username: current_user });

    const response = await fetch('../python/get_rooms.py', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: data
    });

    const response_data = await response.json();
  
    const select = document.getElementById('studentNumber');

    response_data.forEach(number => {
        const option = document.createElement('option');
        option.value = number;
        option.textContent = number;
        select.appendChild(option);
    });
    

});

option = document.getElementById('selectForm');

option.addEventListener('submit', async function () {

    event.preventDefault();

    const studentNumber = document.getElementById('studentNumber').value;
    if (studentNumber) {

        const data = JSON.stringify({ studentFN: studentNumber});

        const response = await fetch('../php/get_questions.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: data
        });

        response_data = await response.json();

        const container = document.getElementById('reviewForm');
        container.innerHTML = '';
        q_Number = 1;

        response_data.questions.forEach(question => {

            questionElement = document.createElement('section');
            questionElement.innerHTML = `
                        <h3>Въпрос ${q_Number}: ${question.question}</h3>
                        <p>Отговор 1 - ${question.opt1}</p>
                        <p>Отговор 2 - ${question.opt2}</p>
                        <p>Отговор 3 - ${question.opt3}</p>
                        <p>Отговор 4 - ${question.opt4}</p>
                        <p>Верен отговор - ${question.answer}</p>
                        <p>Ниво на трудност - ${question.difficulty}</p>
                        <p>Забележка от автора - ${question.note}</p>
                        <label for="review${q_Number}">Ревю:</label>
                        <p><textarea id="review${q_Number}" name="review${q_Number}"></textarea></p>
                        <p><label for="rating${q_Number}">Оценка:</label></p>
                        <select id="rating${q_Number}" name="rating${q_Number}">
                            <option value="1">1 - кой го е мислил този въпрос</option>
                            <option value="2">2 - има какво да се желае</option>
                            <option value="3">3 - бива</option>
                            <option value="4">4 - на една крачка от величието</option>
                            <option value="5">5 - велик</option>
                        </select>
                    `;
            container.appendChild(questionElement);
            q_Number++;

        });

        containerSubmit = document.createElement('p');
        containerSubmit.innerHTML = `
                        <button type="submit">Изпрати рецензия</button>`;
        container.appendChild(containerSubmit);

       
    }
    review = document.getElementById('reviewForm');

    review.addEventListener('submit', async function () {

        event.preventDefault();

        date_review = date_time_now();

        review_questions = response_data.questions;
        reviewer = sessionStorage['username'];

        var sections = document.getElementsByTagName('section');

        reviewData = [];

        for (var i = 0; i < sections.length; i++) {
            var reviewId = 'review' + (i + 1);
            var ratingId = 'rating' + (i + 1);

            var review_note = document.getElementById(reviewId).value;
            var rating = document.getElementById(ratingId).value;
            var question = response_data.questions[i]['question'];

            const review = {
                question: question,
                rating: rating,
                review_note: review_note,
                reviewer: reviewer,
                date: date_review
            };
            reviewData.push(review);
        }

        const reviewDataJSON = JSON.stringify(reviewData);


        const response = await fetch('../php/save_reviews.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: reviewDataJSON
        });


        final_response = await response.json();

        if (final_response.success) {
            alert('Ревюто беше успешно запазено!');

            window.location.href = '../html/review_questions.html';

        } else {
            alert('Възникна грешка! Ревюто не беше запазено!');
        }

    });
});


    
