document.addEventListener('DOMContentLoaded', function () {
    console.log("dom loaded");
    const list = document.getElementById('shows-list');
    const children = list.children;
    const totalItems = children.length; // dynamically get the total items
    let currentIndex = 0;
    const itemsToShow = 7;

    const leftArrow = document.getElementById('left-arrow');
    const rightArrow = document.getElementById('right-arrow');
    const cont = document.getElementById('shows-container');

    function updateDisplay() {
        for (let i = 0; i < totalItems; i++) {
            children[i].style.display = 'none';
        }
        for (let i = currentIndex; i < currentIndex + itemsToShow && i < totalItems; i++) {
            children[i].style.display = 'inline-block';
        }
        leftArrow.style.visibility = currentIndex === 0 ? 'hidden' : 'visible';
        rightArrow.style.visibility = currentIndex + itemsToShow >= totalItems ? 'hidden' : 'visible';
    }

    function customScroll(direction) {
        currentIndex += direction * itemsToShow;
        if (currentIndex < 0) {
            currentIndex = 0;
        } else if (currentIndex + itemsToShow > totalItems) {
            currentIndex = Math.max(0, totalItems - itemsToShow); // adjust to show the last full set or remaining items
        }
        updateDisplay();
    }

    leftArrow.addEventListener('click', function () {
        customScroll(-1);
    });

    rightArrow.addEventListener('click', function () {
        customScroll(1);
    });

    updateDisplay(); // Initialize the display on load
    cont.style.visibility = 'visible';
});
