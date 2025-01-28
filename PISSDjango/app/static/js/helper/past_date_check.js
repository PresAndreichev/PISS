const currDate = new Date().toISOString().split('T')[0];
document.getElementById("datePicker").setAttribute('min', currDate);