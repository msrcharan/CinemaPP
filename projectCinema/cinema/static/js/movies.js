class MoviePageFacade {
    constructor(containerSelector) {
        this.mainContainer = document.querySelector(containerSelector);
        this.moviesPerPage = 30;
        this.moviesFetched = false; // Track if movies have been fetched
    }

    async init() {
        try {
            if (!this.moviesFetched) { // Fetch movies only if not already fetched
                const movies = await this.fetchMovies(); // Fetch movies
                this.totalPages = Math.ceil(movies.length / this.moviesPerPage);
                this.setupPages(movies);
                this.moviesFetched = true; // Set flag to true after fetching movies
            }
        } catch (error) {
            console.error('Failed to initialize movie pages:', error);
        }
    }

    async fetchMovies() {
        // Check if there's a genre filter in the URL
        const params = new URLSearchParams(window.location.search);
        const genre = params.get('genre');
        const release_date = params.get('release_date');

        // If a genre filter is present, fetch filtered movies
        if (genre) {
            const response = await fetch(`/filter/?release_date=${release_date}&genre=${genre}`);
            console.log(genre)
            if (!response.ok) {
                throw new Error('Failed to fetch filtered movies');
            }
            return response.json();
        } else {
            // Otherwise, fetch all movies
            const response = await fetch('/api/movies/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }
    }

    setupPages(movies) {
        for (let i = 0; i < this.totalPages; i++) {
            const page = this.createPage(i);
            this.populatePage(page, movies, i);
            this.mainContainer.appendChild(page);
        }
    }

    createPage(pageIndex) {
        const page = document.createElement('div');
        page.className = 'page';
        page.id = `page-${pageIndex + 1}`;
        page.style.padding = '30px';
        page.style.display = pageIndex === 0 ? 'block' : 'none'; // first page
        return page;
    }

    populatePage(page, movies, pageIndex) {
        const flexColumn = document.createElement('div');
        flexColumn.className = 'flex-column';
        page.appendChild(flexColumn);

        const startIndex = pageIndex * this.moviesPerPage;
        const endIndex = Math.min((pageIndex + 1) * this.moviesPerPage, movies.length);

        for (let j = startIndex; j < endIndex; j++) {
            if (j % 6 === 0) {
                var flexRow = document.createElement('div');
                flexRow.className = 'flex-row';
                flexColumn.appendChild(flexRow);
            }

            const movieButton = this.createMovieButton(movies[j]);
            flexRow.appendChild(movieButton);
        }

        this.addNavigationButtons(pageIndex, flexColumn);
    }

    createMovieButton(movie) {
        const movieButton = document.createElement('button');
        movieButton.className = 'movie-button';
        movieButton.style.background = "transparent";
        movieButton.style.border = "none";
        movieButton.style.display = "block"; 

        const movieTile = document.createElement('img');
        movieTile.src = movie.image;
        movieTile.alt = movie.title;  
        movieTile.className = 'movie-tile';

        const contentContainer = document.createElement('div');
        contentContainer.className = 'content-container';
        contentContainer.style.display = "inline-block";  

        contentContainer.appendChild(movieTile);

        const movieTitle = document.createElement('div');
        movieTitle.innerText = movie.title;
        movieTitle.className = 'movie-title';
        movieTitle.style.textAlign = "center"; 

        contentContainer.appendChild(movieTitle);

        movieButton.appendChild(contentContainer);

        movieButton.addEventListener('click', () => this.showPopup(movie));

        return movieButton;
    }

    addNavigationButtons(pageIndex, flexColumn) {
        if (pageIndex > 0) {
            const prevBtn = document.createElement('a');
            prevBtn.href = '#';
            prevBtn.textContent = 'Previous Page';
            prevBtn.onclick = () => this.showPage(pageIndex, pageIndex - 1);
            flexColumn.appendChild(prevBtn);
        }
        if (pageIndex < this.totalPages - 1) {
            const nextBtn = document.createElement('a');
            nextBtn.href = '#';
            nextBtn.textContent = 'Next Page';
            nextBtn.onclick = () => this.showPage(pageIndex, pageIndex + 1);
            flexColumn.appendChild(nextBtn);
        }
    }

    showPage(currentPageIndex, nextPageIndex) {
        document.getElementById(`page-${currentPageIndex + 1}`).style.display = 'none';
        document.getElementById(`page-${nextPageIndex + 1}`).style.display = 'block';
        window.scrollTo(0, 0);
        return false;
    }

    showPopup(movie) {
        const myPopup = document.getElementById("myPopup");
        myPopup.querySelector("h2").innerText = movie.title;
        document.getElementById("moviePoster").src = movie.image;
        document.getElementById("movieDescription").innerText = movie.rating + ' - ' + movie.description;
        document.getElementById("movieTrailer").src = movie.trailer_url;

        document.getElementById("book-now").addEventListener('click', function() {
            window.location.href = '/individual_movie/' + movie.title + '/';
        });

        myPopup.style.display = "block";

        document.querySelector(".closePopup").addEventListener("click", function () {
            myPopup.style.display = "none";
        });

        window.addEventListener("click", function (event) {
            if (event.target == myPopup) {
                myPopup.style.display = "none";
            }
        });
    }
}

// function applyFilter() {
//     const genre = document.getElementById('genre').value;
//     const url = genre ? `/filter/?genre=${genre}` : '/movies/';
//     window.location.href = url;
    
// }

document.addEventListener('DOMContentLoaded', function() {
    const facade = new MoviePageFacade('.main-container');
    facade.init();
});
