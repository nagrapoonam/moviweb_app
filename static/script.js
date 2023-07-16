document.addEventListener("DOMContentLoaded", function() {
  // Fetch random movies from the OMDB API
  fetchRandomMovies()
    .then(function(movies) {
      // Generate carousel slides
      generateCarouselSlides(movies);

      // Generate random movies
      generateRandomMovies(movies);
    })
    .catch(function(error) {
      console.error("Error:", error);
    });
});

function fetchRandomMovies() {
  const api_url = "http://www.omdbapi.com/?apikey=4bf81bd7&t";
  const movieTitles = ["Silo", "The Witcher", "Sound Of Freedom", "Black Mirror", "Titanic", "The Flash", "Extraction II", "Yellowstone", "The Boys", "The Covenant", "Barbie"];

  // Fetch movie details from the OMDB API for each title
  const fetchMoviePromises = movieTitles.map((title) => {
    const url = `${api_url}=${encodeURIComponent(title)}`;
    return fetch(url)
      .then((response) => response.json())
      .then((data) => ({
        title: data.Title,
        poster: data.Poster,
        director: data.Director,
        year: data.Year,
        rating: data.imdbRating
      }))
      .catch((error) => {
        console.error(`Error fetching movie "${title}":`, error);
        return null;
      });
  });

  // Return a promise that resolves to an array of movies
  return Promise.all(fetchMoviePromises).then((movies) => movies.filter(Boolean));
}

function generateCarouselSlides(movies) {
  const carousel = document.querySelector(".carousel");

  // Generate carousel slides dynamically
  movies.forEach(function(movie) {
    const slide = document.createElement("div");
    slide.classList.add("carousel-slide");

    const img = document.createElement("img");
    img.src = movie.poster;
    img.alt = movie.title;

    slide.appendChild(img);
    carousel.appendChild(slide);
  });

  // Initialize the carousel using Bootstrap Carousel
  $(".carousel").carousel();
}

function generateRandomMovies(movies) {
  const movieGrid = document.querySelector(".movie-grid");

  // Generate random movies dynamically
  movies.slice(0, 10).forEach(function(movie) {
    const movieElement = document.createElement("div");
    movieElement.classList.add("movie");

    const img = document.createElement("img");
    img.src = movie.poster;
    img.alt = movie.title;

    const title = document.createElement("h3");
    title.classList.add("movie-title");
    title.textContent = movie.title;

    movieElement.appendChild(img);
    movieElement.appendChild(title);
    movieGrid.appendChild(movieElement);
  });
}
