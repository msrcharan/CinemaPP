function displayCard() {
    var cards = ["Card 1", "Card 2", "Card 3"];
    var selectedCard = document.getElementById('cardSelector').value;
    console.log(selectedCard)
    document.getElementById('cardDetails1').style.display = 'none';
    document.getElementById('cardDetails2').style.display = 'none';
    document.getElementById('cardDetails3').style.display = 'none';

    if (selectedCard[0] == 'C') {
        var number = selectedCard[5];
        var cardDetails = document.getElementById('cardDetails' + number);
        cardDetails.style.display = 'block';
    }
}