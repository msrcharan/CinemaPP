document.addEventListener('DOMContentLoaded', function() {
    const times = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];

    function updateDates() {
        const dayNames = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
        const monthNames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

        const today = new Date();
        for (let i = 0; i < 5; i++) { 
            const date = new Date(today.getFullYear(), today.getMonth(), today.getDate() + i);
            const daySpan = document.querySelector(`.D${i + 1} .Day`);
            const monthSpan = document.querySelector(`.D${i + 1} .Month`);
            daySpan.textContent = i === 0 ? 'Today' : dayNames[date.getDay()];
            monthSpan.textContent = `${monthNames[date.getMonth()]} ${date.getDate()}`;
        }
    }

    function showTimeSelector(callback) {
        const container = document.getElementById('timeSelector');
        container.innerHTML = ''; // Clear previous times
        times.forEach(time => {
            const timeElement = document.createElement('div');
            timeElement.textContent = time;
            timeElement.style.cursor = 'pointer';
            timeElement.addEventListener('click', () => {
                callback(time); // Execute callback with the selected time
                container.style.display = 'none'; // Hide the selector after selection
            });
            container.appendChild(timeElement);
        });
        container.style.display = 'block'; // Show the container for time selection
    }
    

    function addClickListeners() {
        document.querySelectorAll('.DateContainer').forEach((container, index) => {
            container.addEventListener('click', function() {
                const daySpan = document.querySelector(`.D${index + 1} .Day`).textContent;
                const monthSpan = document.querySelector(`.D${index + 1} .Month`).textContent;
                showTimeSelector(selectedTime => {
                    console.log(`You selected: ${selectedTime} on ${daySpan} ${monthSpan}`);
                    // Navigate after the time has been selected within the callback
                    window.location.href = "{{html/seats.html";
                });
            });
        });
    }

    updateDates();
    addClickListeners();
});
