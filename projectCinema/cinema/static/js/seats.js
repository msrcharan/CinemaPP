//tickets
let totalTickets = 0; 
const bookButton = document.getElementById('bookButton');



function removeAllSelectedSeats() {
    const seats = document.querySelectorAll('.SeatSelect div div');
    seats.forEach(seat => {
        seat.classList.remove('selected');
        hideButton();
    });
}
function hideButton() {
        bookButton.style.display = 'none';
    }
function showButton() {
        bookButton.style.display = 'block';
    }
function updateTotalTickets() {
    const ticketCounts = document.querySelectorAll('.TicNum');
    totalTickets = Array.from(ticketCounts).reduce((acc, el) => acc + parseInt(el.textContent, 10), 0);
    document.querySelector('.count').textContent = totalTickets;
    removeAllSelectedSeats()
    updateSeatSelectionAvailability(); 
}

function updateTicketCount(element, increment) {
    let countElement = element.parentNode.querySelector('.TicNum');
    let currentCount = parseInt(countElement.textContent);
    currentCount = increment ? currentCount + 1 : Math.max(currentCount - 1, 0);
    countElement.textContent = currentCount;
    updateTotalTickets(); 
}











document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.addTic, .removeTic').forEach(button => {
        button.addEventListener('click', function() {
            const isIncrement = this.classList.contains('addTic');
            updateTicketCount(this, isIncrement);
        });
    });
});

//Seats
document.addEventListener('DOMContentLoaded', function() {
    const seats = document.querySelectorAll('.SeatSelect div div');
    seats.forEach(seat => {
        seat.addEventListener('click', function() {
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
            } else {
                const currentlySelectedSeats = document.querySelectorAll('.SeatSelect .selected').length;
                if (currentlySelectedSeats < totalTickets) {
                    this.classList.add('selected');
                }
            }
            
            const updatedSelectedSeats = document.querySelectorAll('.SeatSelect .selected').length;
            
            if (totalTickets == updatedSelectedSeats) {
                showButton();
            } else {
                hideButton();
            }
        });
    });
});
