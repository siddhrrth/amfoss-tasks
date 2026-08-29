import MovieGrid from "../components/MovieGrid";
import { useWatchlist } from "../context/WatchlistContext";

function Collection() {
  const { collection } = useWatchlist();

  return (
    <main className="page">
      <p className="section-label">PERSONAL ARCHIVE</p>

      <h1>My Collection</h1>

      <p className="page-description">
        Your personal collection of cinematic history.
      </p>

      {collection.length > 0 ? (
        <>
          <div className="collection-stats">
            <span>{collection.length}</span>
            {collection.length === 1 ? " film archived" : " films archived"}
          </div>

          <MovieGrid movies={collection} />
        </>
      ) : (
        <div className="empty-state">
          <div className="empty-icon">◇</div>

          <h2>No movies collected yet</h2>

          <p>
            Explore movies and add your favorites to build your personal
            archive.
          </p>
        </div>
      )}
    </main>
  );
}

export default Collection;