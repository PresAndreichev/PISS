
document.addEventListener('DOMContentLoaded', async function () {

    const current_user = sessionStorage['username'];
    const userRole = sessionStorage['role'];
    const password = sessionStorage['password'];
    
    const data = JSON.stringify({
        username: current_user, role: userRole, password: password
    });

    const response = await fetch('../py/get_saved_rooms.py', { //May need to redart the PATH 
         method: 'POST',
         headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
         },
         body: data
    });

    const response_data = await response.json();

    const container = document.getElementById('savedRoomsField');

    let roomSeqNumber = 1;

    response_data.rooms.forEach(room => {
        const roomElement = document.createElement('section');

        lessonType = room.lectureType;
        type;
        if (lessonType == "lecture") {
            type = "Лекция";
        } else if (lessonType == "practical") {
            type = "Практикум";
        } else if (lessonType == "theoretical") {
            type = "Семинар";
        }

         roomElement.innerHTML = `
            <h3>${roomSeqNumber}. Дисциплина: ${room.subject}</h3>
            <p>Тема: ${room.lessonName}</p>
            <p>Тип занятие: ${type}</p>
            <p>Преподавател по дисциплина: ${room.lessonName}</p>
            <p>Стая/Зала: ${room.number}</p>
            <p>Ден: ${room.date}</p>
            <p>Начален час: ${room.start}</p>
            <p>Краен час: ${room.end}</p>
            
         `;

        container.appendChild(roomElement);
        roomSeqNumber++;
    });
       
});
    
