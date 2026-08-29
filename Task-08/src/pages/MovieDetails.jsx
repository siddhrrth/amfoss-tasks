import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getMovieDetails } from "../services/tmdb";
import { useWatchlist } from "../context/WatchlistContext";

const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";
const BACKDROP_BASE_URL = "https://image.tmdb.org/t/p/original";

function MovieDetails() {
  const { id } = useParams();

  const {
    addToWatchlist,
    removeFromWatchlist,
    isInWatchlist,
    addToCollection,
    removeFromCollection,
    isInCollection,
  } = useWatchlist();

  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMovie() {
      try {
        setLoading(true);
        setError("");

        const data = await getMovieDetails(id);

        setMovie(data);
      } catch (error) {
        console.error(error);
        setError("Unable to load movie details.");
      } finally {
        setLoading(false);
      }
    }

    loadMovie();
  }, [id]);

  /* ---------------- LOADING ---------------- */

  if (loading) {
    return (
      <section className="details-page">
        <div className="details-loading">
          Loading archive record...
        </div>
      </section>
    );
  }

  /* ---------------- ERROR ---------------- */

  if (error || !movie) {
    return (
      <section className="page">
        <p className="section-label">
          ARCHIVE ERROR
        </p>

        <h1>Record unavailable</h1>

        <p className="page-description">
          {error || "This movie could not be found."}
        </p>

        <Link to="/" className="back-link">
          ← Return to archive
        </Link>
      </section>
    );
  }

  /* ---------------- MOVIE DATA ---------------- */

  const posterUrl = movie.poster_path
    ? `${IMAGE_BASE_URL}${movie.poster_path}`
    : null;

  const backdropUrl = movie.backdrop_path
    ? `${BACKDROP_BASE_URL}${movie.backdrop_path}`
    : null;

  const year = movie.release_date
    ? movie.release_date.slice(0, 4)
    : "Unknown";

  const runtime = movie.runtime
    ? `${Math.floor(movie.runtime / 60)}h ${
        movie.runtime % 60
      }m`
    : "Runtime unavailable";

  const saved = isInWatchlist(movie.id);
  const collected = isInCollection(movie.id);

  /* ---------------- PAGE ---------------- */

  return (
    <section className="details-page">
      {backdropUrl && (
        <div
          className="details-backdrop"
          style={{
            backgroundImage: `url(${backdropUrl})`,
          }}
        />
      )}

      <div className="details-overlay" />

      <div className="details-content">
        <Link to="/" className="back-link">
          ← Back to archive
        </Link>

        <div className="details-main">

          {/* POSTER */}

          <div className="details-poster">
            {posterUrl ? (
              <img
                src={posterUrl}
                alt={movie.title}
              />
            ) : (
              <div className="no-poster">
                No Poster
              </div>
            )}
          </div>

          {/* INFORMATION */}

          <div className="details-info">
            <p className="section-label">
              ARCHIVE RECORD
            </p>

            <h1>{movie.title}</h1>

            {movie.tagline && (
              <p className="tagline">
                "{movie.tagline}"
              </p>
            )}

            <div className="movie-meta">
              <span>{year}</span>

              <span>•</span>

              <span>{runtime}</span>

              <span>•</span>

              <span>
                ★ {movie.vote_average?.toFixed(1)}
              </span>
            </div>

            <div className="genres">
              {movie.genres?.map((genre) => (
                <span key={genre.id}>
                  {genre.name}
                </span>
              ))}
            </div>

            <p className="overview">
              {movie.overview ||
                "No overview available for this record."}
            </p>

            {/* ACTIONS */}

            <div className="details-actions">

              <button
                type="button"
                className={`watchlist-button ${
                  saved ? "saved" : ""
                }`}
                onClick={() => {
                  if (saved) {
                    removeFromWatchlist(movie.id);
                  } else {
                    addToWatchlist(movie);
                  }
                }}
              >
                {saved
                  ? "✓ Saved to Watchlist"
                  : "+ Add to Watchlist"}
              </button>

              <button
                type="button"
                className={`collection-button ${
                  collected ? "saved" : ""
                }`}
                onClick={() => {
                  if (collected) {
                    removeFromCollection(movie.id);
                  } else {
                    addToCollection(movie);
                  }
                }}
              >
                {collected
                  ? "✓ In Collection"
                  : "+ Add to Collection"}
              </button>

            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default MovieDetails;