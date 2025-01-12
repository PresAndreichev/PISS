
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

         roomElement.innerHTML = `
            <strong>Стая/Зала ${roomSeqNumber}: ${room.number}</strong>
            <p>Вид стая - ${room.lessonName}</p>
            <p>Вид стая - ${room.lessonType}</p>
            <p>Вид стая - ${room.date}</p>
            <p>Вид стая - ${room.startTime}</p>
            <p>Вид стая - ${room.endType}</p>
            <p>Вид стая - ${room.criteria1}</p>
            <p>Вид дъска - ${room.criteria2}</p>
            <p>Налична мултимедия - ${room.criteria3}</p>
            <p>Капацитет - ${room.seatsCount}</p>
         `;

         container.appendChild(roomElement);
         roomSeqNumber++;
    });        
       
});
    
