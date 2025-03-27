document.addEventListener('DOMContentLoaded', function () {

    const myPopup = document.getElementById('myPopup'); // Adjust the ID if necessary
    const closePopup = document.querySelector('.closePopup'); // This assumes there's only one close button

    console.log("js loaded");

    // Function to update and show the popup with user info
    function showPopup() {
        myPopup.style.display = "block";
    }

    const button = document.getElementById('manage-users');
    button.addEventListener("click", function () {
        console.log("Opening popup...");
        showPopup();
    });

    // Close the popup when the user clicks on <span> (x)
    closePopup.addEventListener("click", function () {
        myPopup.style.display = "none";
    });

    // Close the popup when the user clicks anywhere outside of it
    window.addEventListener("click", function (event) {
        if (event.target == myPopup) {
            myPopup.style.display = "none";
        }
    });

    // Assuming this is your initial array of user objects
    // Example array of user objects
    let users = [
        { id: 1, name: 'admin@admin.com', type: 'Admin' },
        { id: 2, name: 'user@user.com', type: 'User' },
        { id: 3, name: 'admin2@admin.com', type:'Admin'},
        { id: 4, name: 'user2@user.com', type: 'User' }
    ];
    
    
    function addUsersToPopup(users) {
        const popupContent = document.querySelector('.popup-content');
        popupContent.innerHTML = ''; // Clear previous content
        const userList = document.createElement('ul');

        users.forEach((user, index) => {
            const li = document.createElement('li');
            li.textContent = `${user.name} - ${user.type}`;

            // Remove button
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.onclick = () => removeUser(index);

            const adminBtn = document.createElement('button');
            adminBtn.setAttribute('data-index', index);
            if (user.type == 'Admin') {
                adminBtn.textContent = 'Admin';
            } else {
                adminBtn.textContent = 'User';
            }
            adminBtn.onclick = () => changeUserType(index);

            li.appendChild(removeBtn);
            li.appendChild(adminBtn);
            userList.appendChild(li);
        });

        popupContent.appendChild(userList);
    }

    function removeUser(index) {
        users.splice(index, 1);
        addUsersToPopup(users);
    }

    function changeUserType(index) {
        const isAdmin = users[index].type == 'Admin';
        users[index].type = isAdmin ? 'User' : 'Admin';
        document.querySelector(`button[data-index='${index}']`).textContent = isAdmin ? 'User' : 'Admin';
    }

    // Initially populate the popup with users
    addUsersToPopup(users);

});
