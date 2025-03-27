

var div = document.createElement("div");
var userName = document.body.getAttribute('data-user-name');
var innerHTML =
  '<div class="top">\n' +
  '<div class="cinema-container">\n' +
  '<a href="/"><div class="empty"></div></a>\n' +
  '<a href="/" class="cinema-plus">Cinema++</a>\n' +
  '</div>\n' +
  '<a href="/movies/" class="movies">Movies</a>\n' +
  '<div class="sign-in-container">\n';

var userLoggedIn = document.body.getAttribute('data-user-logged-in') == 'true';

if (userLoggedIn) {
  innerHTML += `
  <div class="user-logged-in">
      <a href="#" class="user-name-dropdown">${ userName } ▼</a>
      <div class="dropdown-content">
          <a href="/edit-profile">Edit Profile</a>
          <a href="/mybookings">My Bookings</a>
          <a href="/logout">Logout</a>
      </div>
  </div>`;
} else {
  innerHTML += 
  '<a href="/registration/" class="sign-in-join" id="sign-logo"><div class="user-not-logged-in"></div></a>\n' +
  '<a href="/registration/" class="sign-in-join" id="sign-text">Sign In / Join</a>\n';
}
innerHTML +=   '</div>\n' +
'</div>\n';
div.innerHTML += innerHTML;

document.body.prepend(div);

const dropdown = document.querySelector('.user-name-dropdown');
if (dropdown) {
    dropdown.addEventListener('click', function(event) {
        event.preventDefault();
        var dropdownContent = document.querySelector('.dropdown-content');
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });
}