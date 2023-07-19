// Fetch movie data from movies.json
fetch('movies.json')
  .then(response => response.json())
  .then(data => {
    const movies = data;
    const header = document.querySelector('header');

    // Iterate over each movie
    for (const userId in movies) {
      const user = movies[userId];
      const userMovies = user.movies;

      // Iterate over each movie poster
      for (const movieId in userMovies) {
        const movie = userMovies[movieId];
        const posterUrl = movie.poster;

        // Create an image element for the movie poster
        const posterImage = document.createElement('img');
        posterImage.src = posterUrl;

        // Append the poster image to the header
        header.appendChild(posterImage);
      }
    }
  })
  .catch(error => {
    console.error('Error fetching movie data:', error);
  });
