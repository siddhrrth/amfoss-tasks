import { Link } from "react-router-dom";

const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

function MovieCard({ movie }) {
  const posterUrl = movie.poster_path
    ? `${IMAGE_BASE_URL}${movie.poster_path}`
    : null;

  return (
    <Link to={`/movie/${movie.id}`} className="movie-card">
      <div className="poster-container">
        {posterUrl ? (
          <img
            src={posterUrl}
            alt={movie.title}
            loading="lazy"
          />
        ) : (
          <div className="no-poster">
            No Poster
          </div>
        )}

        <div className="movie-rating">
          ★ {movie.vote_average?.toFixed(1)}
        </div>
      </div>

      <div className="movie-info">
        <h3>{movie.title}</h3>

        <p>
          {movie.release_date
            ? movie.release_date.slice(0, 4)
            : "Unknown"}
        </p>
      </div>
    </Link>
  );
}

export default MovieCard;