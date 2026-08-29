import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import MovieGrid from "../components/MovieGrid";
import { searchMovies } from "../services/tmdb";

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();

  const query = searchParams.get("query") || "";

  const [input, setInput] = useState(query);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!query.trim()) {
      setMovies([]);
      return;
    }

    async function performSearch() {
      try {
        setLoading(true);
        setError("");

        const data = await searchMovies(query);

        setMovies(data.results || []);
      } catch (error) {
        console.error(error);
        setError("Unable to search the archive.");
      } finally {
        setLoading(false);
      }
    }

    performSearch();
  }, [query]);

  function handleSubmit(event) {
    event.preventDefault();

    const trimmedInput = input.trim();

    if (!trimmedInput) {
      return;
    }

    setSearchParams({
      query: trimmedInput,
    });
  }

  return (
    <section className="page search-page">
      <p className="section-label">ARCHIVE SEARCH</p>

      <h1>Search the Archive</h1>

      <p className="page-description">
        Search thousands of movies preserved in the
        cinematic archive.
      </p>

      <form
        className="archive-search"
        onSubmit={handleSubmit}
      >
        <span>⌕</span>

        <input
          type="text"
          value={input}
          onChange={(event) =>
            setInput(event.target.value)
          }
          placeholder="Search for a movie..."
          aria-label="Search for a movie"
        />

        <button type="submit">
          Search
        </button>
      </form>

      {query && (
        <div className="search-results-heading">
          <div>
            <p className="section-label">
              SEARCH RESULTS
            </p>

            <h2>
              Results for "{query}"
            </h2>
          </div>

          {!loading && (
            <span>
              {movies.length} movies
            </span>
          )}
        </div>
      )}

      {loading && (
        <div className="empty-state">
          <h2>Searching the archive...</h2>
          <p>
            Retrieving cinematic records.
          </p>
        </div>
      )}

      {error && (
        <div className="empty-state">
          <h2>Search failed</h2>
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && query && (
        <MovieGrid movies={movies} />
      )}

      {!loading && !error && query && movies.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">◇</div>

          <h2>No records found</h2>

          <p>
            Try searching for another movie.
          </p>
        </div>
      )}
    </section>
  );
}

export default Search;