document.addEventListener("DOMContentLoaded", function() {
    // Get movie details from the URL query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const movieTitle = urlParams.get('title');
    const movieDescription = urlParams.get('description');
    // Remove movieRating and movieStars variables

    const moviePosterUrl = urlParams.get('posterUrl');
    const movieTrailerUrl = urlParams.get('trailerUrl');

    // Set movie details in the HTML elements
    document.getElementById('movieTitle').innerText = movieTitle;
    document.getElementById('movieDescription').innerText = movieDescription;
    // Remove setting for movieRating and movieStars
    document.getElementById('moviePoster').src = moviePosterUrl;
    document.getElementById('movieTrailer').src = movieTrailerUrl;
});
