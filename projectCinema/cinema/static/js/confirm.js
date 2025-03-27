function getSeniorTicketCount() {
    const seniorTicketElement = document.querySelector('.SrTicket .TicNum');
    return parseInt(seniorTicketElement.textContent, 10);
}

function getRegularTicketCount() {
    const regularTicketElement = document.querySelector('.RTicket .TicNum');
    return parseInt(regularTicketElement.textContent, 10);
}

function getKidTicketCount() {
    const kidTicketElement = document.querySelector('.KTicket .TicNum');
    return parseInt(kidTicketElement.textContent, 10);
}
//prices
function calculateTotal(srCount, rCount, kdCount) {
    const srPrice = 15; // senior ticket
    const rPrice = 20; //  regular ticket
    const kdPrice = 10; // kid ticket
    return (srCount * srPrice) + (rCount * rPrice) + (kdCount * kdPrice);
}

document.getElementById('bookButton').addEventListener('click', function() {
    const orderContainer = document.createElement('div');
    orderContainer.classList.add('order-container');

    orderContainer.style.cssText = `
        width: 80vw;
        height: 80vh;
        top: 15vh;
        display: flex;
        justify-content: center;
        align-items: flex-end;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        padding: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
        z-index: 1000;
    `;

    orderContainer.innerHTML = `
        <button type="button" id="confirmOrder">Confirm Order</button>
        <button type="button" id="updateOrder">Update Order</button>
    `;
    const buttons = orderContainer.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.padding = '5px 10px';
        button.style.margin = '0 5px';
        button.style.fontSize = '3vw';
    });
    
    document.body.appendChild(orderContainer);

    const seniorTickets = getSeniorTicketCount();
    const regularTickets = getRegularTicketCount();
    const kidTickets = getKidTicketCount();
    const total = calculateTotal(seniorTickets, regularTickets, kidTickets);

    const messageDisplay = document.createElement('div');
    messageDisplay.setAttribute('id', 'ticketSummary');
    messageDisplay.innerHTML = `
        <p>Regular Tickets: ${regularTickets}</p>
        <p>Kid Tickets: ${kidTickets}</p>
        <p>Senior Tickets: ${seniorTickets}</p>
        <p>Total: $${total}</p>
    `;

    messageDisplay.style.position = 'relative';
    messageDisplay.style.top = '-46vh';
    messageDisplay.style.left = '-50vw';
    messageDisplay.style.fontSize = '2vw';
    
    orderContainer.appendChild(messageDisplay);

    document.getElementById('confirmOrder').addEventListener('click', function() {
        console.log('Confirm Order button clicked');
        window.location.href = "../OrderPlaced/index.html";
    });

    document.getElementById('updateOrder').addEventListener('click', function() {
        console.log('Update Order button clicked');
        orderContainer.remove(); 
    });
});
