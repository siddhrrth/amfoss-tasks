import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTrendingMovies } from "../services/tmdb";
import MovieGrid from "../components/MovieGrid";

function Home() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchInput, setSearchInput] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    async function loadMovies() {
      try {
        setLoading(true);
        setError("");

        const data = await getTrendingMovies();

        setMovies(data.results || []);
      } catch (error) {
        console.error(error);
        setError("Unable to load movies.");
      } finally {
        setLoading(false);
      }
    }

    loadMovies();
  }, []);

  function handleSearch(event) {
    event.preventDefault();

    const query = searchInput.trim();

    if (!query) {
      return;
    }

    navigate(
      `/search?query=${encodeURIComponent(query)}`
    );
  }

  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">
            THE LIBRARY OF OHARA
          </p>

          <h1>
            Discover stories.
            <br />
            <span>Preserve legends.</span>
          </h1>

          <p className="hero-description">
            Explore the world's cinematic history and
            build your personal archive of
            unforgettable stories.
          </p>

          <form
            className="hero-search"
            onSubmit={handleSearch}
          >
            <span>⌕</span>

            <input
              type="text"
              value={searchInput}
              onChange={(event) =>
                setSearchInput(event.target.value)
              }
              placeholder="Search the archive..."
              aria-label="Search the archive"
            />

            <button type="submit">
              Search
            </button>
          </form>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <p className="section-label">
              EXPLORE
            </p>

            <h2>Trending Now</h2>
          </div>
        </div>

        {loading && (
          <div className="empty-card">
            Loading the archive...
          </div>
        )}

        {error && (
          <div className="empty-card">
            {error}
          </div>
        )}

        {!loading && !error && (
          <MovieGrid movies={movies} />
        )}
      </section>
    </div>
  );
}

export default Home;