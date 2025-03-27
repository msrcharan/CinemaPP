async function loadMovies(category) {
    const container = document.getElementById(category);
    try {
        const response = await fetch(`/movies?category=${category}`);
        if (!response.ok) throw new Error('Failed to fetch movies');
        const movies = await response.json();
        container.innerHTML = ''; // Clear existing movies
        movies.forEach(movie => {
            const movieElement = createMovieElement(movie);
            container.querySelector('.movies-container').appendChild(movieElement);
        });
    } catch (error) {
        console.error('Error loading movies:', error);
        container.innerHTML = '<p>Error loading movies.</p>';
    }
}

function createMovieElement(movie) {
    const div = document.createElement('div');
    div.className = 'movie';
    div.innerHTML = `
        <h3>${movie.title}</h3>
        <p>${movie.description}</p>
        <button onclick="playTrailer('${movie.trailer_url}')">Play Trailer</button> 
    `;
    return div;
}

function playTrailer(trailerLink) {
    const iframeHtml = `
        <div id="trailer-modal" onclick="this.remove()">
            <iframe src="${trailerLink}" frameborder="0" allowfullscreen></iframe>
        </div>
    `;
    document.body.innerHTML += iframeHtml;
}

async function searchMovie() {
    const query = document.getElementById('search-bar').value;
    if (!query) return;
    try {
        const response = await fetch(`/movies/search?title=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Search failed');
        const movies = await response.json();
        // Assuming we display search results in the 'currently-running' section for simplicity
        const container = document.getElementById('currently-running').querySelector('.movies-container');
        container.innerHTML = ''; // Clear previous results
        movies.forEach(movie => {
            const movieElement = createMovieElement(movie);
            container.appendChild(movieElement);
        });
        // Optionally, hide or clear the 'coming-soon' section during search results display
    } catch (error) {
        console.error('Error during search:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    populateCarousel();
});

let currentSlide = 0;

// function populateCarousel() {
//     const now_showing = [
//         {% for movie in now_showing %}
//             { title: '{{ movie.title }}', image: '{{ movie.image.url }}', trailer: '{{ movie.trailer }}', description: '{{ movie.description }}' },
//         {% endfor %}
//     ];
    
//     const coming_soon = [
//         {% for movie in coming_soon %}
//             { title: '{{ movie.title }}', image: '{{ movie.image.url }}', trailer: '{{ movie.trailer }}', description: '{{ movie.description }}' },
//         {% endfor %}
//     ];

//     populateCategory('now-playing', now_showing);
//     populateCategory('coming-soon', coming_soon);
// }

// function populateCategory(categoryId, movies) {
//     const container = document.getElementById(categoryId);
//     movies.forEach((movie, index) => {
//         const item = document.createElement('div');
//         item.className = 'carousel-item';
//         item.innerHTML = `<button class="movieButton" data-movie-index="${index}">
//             <img src="${movie.image}" alt="${movie.title}">
//             <label class="movietitle">${movie.title}</label>
//         </button>`;
//         container.appendChild(item);
//     });

//     // Select the popup and close button elements
    
//       const myPopup = document.getElementById("myPopup");
//       const movieTitle = myPopup.querySelector("h2");
//       const popupPoster = document.getElementById("moviePoster");
//       const popupDescription = document.getElementById("movieDescription");
//       const popupTrailer = document.getElementById("movieTrailer");
//       const closePopup = document.querySelector(".closePopup");
  
//       // Function to update and show the popup based on the clicked movie
//       function showPopup(movie) {
//           movieTitle.innerText = movie.title;
//           popupPoster.src = movie.image;
//           popupPoster.alt = movie.title;
//           popupDescription.innerText = movie.description;
//           popupTrailer.src = movie.trailer;
//           myPopup.style.display = "block";
//       }

//         container.querySelectorAll('.movieButton').forEach(button => {
//             button.addEventListener("click", function () {
//                 const movieIndex = this.getAttribute('data-movie-index');
//                 const movie = movies[movieIndex];
//                 showPopup(movie);
//             });
//         });

//     // Close the popup when the user clicks on <span> (x)
//     closePopup.addEventListener("click", function () {
//         myPopup.style.display = "none";
//     });

//     // Close the popup when the user clicks anywhere outside of it
//     window.addEventListener("click", function (event) {
//         if (event.target == myPopup) {
//             myPopup.style.display = "none";
//         }
//     });

// }


let currentSlides = {};

function moveSlide(carouselId, direction) {
    const carousel = document.getElementById(carouselId);
    const totalSlides = carousel.querySelectorAll('.carousel-item').length;
    currentSlides[carouselId] = currentSlides[carouselId] || 0;

    if (direction === 'next') {
        currentSlides[carouselId] = (currentSlides[carouselId] + 1) % totalSlides;
    } else {
        currentSlides[carouselId] = (currentSlides[carouselId] - 1 + totalSlides) % totalSlides;
    }

    const newTransformValue = `translateX(-${currentSlides[carouselId] * 100}%)`;
    carousel.querySelector('.carousel-container').style.transform = newTransformValue;
}
