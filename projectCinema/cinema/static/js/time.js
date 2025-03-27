document.addEventListener('DOMContentLoaded', function() {
    const times = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];
    const container = document.getElementById('timeSlots');

    times.forEach(time => {
        const timeElement = document.createElement('button');
        timeElement.textContent = time;
        timeElement.classList.add('time-slot');
        timeElement.onclick = function() { saveTime(time); };
        container.appendChild(timeElement);
    });
});

function saveTime(time) {
    // Save the time in a variable
    console.log(`Time selected: ${time}`); // For demonstration, we're just logging it
    // You can save this time variable in a way that suits your application needs
}
