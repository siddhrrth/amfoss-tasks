import MovieGrid from "../components/MovieGrid";
import { useWatchlist } from "../context/WatchlistContext";

function Watchlist() {
  const { watchlist } = useWatchlist();

  return (
    <main className="page">
      <p className="section-label">YOUR WATCHLIST</p>

      <h1>Watchlist</h1>

      <p className="page-description">
        Movies you've saved to watch later.
      </p>

      {watchlist.length > 0 ? (
        <>
          <div className="collection-stats">
            <span>{watchlist.length}</span>
            {watchlist.length === 1 ? " film saved" : " films saved"}
          </div>

          <MovieGrid movies={watchlist} />
        </>
      ) : (
        <div className="empty-state">
          <div className="empty-icon">◇</div>

          <h2>Your watchlist is empty</h2>

          <p>
            Discover a movie and save it here when you want to watch it later.
          </p>
        </div>
      )}
    </main>
  );
}

export default Watchlist;