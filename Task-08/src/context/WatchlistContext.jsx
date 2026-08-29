import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

const WatchlistContext = createContext(null);

function getStoredMovies(key) {
  try {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error(`Unable to load ${key}:`, error);
    return [];
  }
}

export function WatchlistProvider({ children }) {
  const [watchlist, setWatchlist] = useState(() =>
    getStoredMovies("ohara-watchlist")
  );

  const [collection, setCollection] = useState(() =>
    getStoredMovies("ohara-collection")
  );

  /* ---------------- WATCHLIST ---------------- */

  const isInWatchlist = (movieId) => {
    return watchlist.some((movie) => movie.id === movieId);
  };

  const addToWatchlist = (movie) => {
    setWatchlist((current) => {
      if (current.some((item) => item.id === movie.id)) {
        return current;
      }

      return [...current, movie];
    });
  };

  const removeFromWatchlist = (movieId) => {
    setWatchlist((current) =>
      current.filter((movie) => movie.id !== movieId)
    );
  };

  const toggleWatchlist = (movie) => {
    if (isInWatchlist(movie.id)) {
      removeFromWatchlist(movie.id);
    } else {
      addToWatchlist(movie);
    }
  };

  /* ---------------- COLLECTION ---------------- */

  const isInCollection = (movieId) => {
    return collection.some((movie) => movie.id === movieId);
  };

  const addToCollection = (movie) => {
    setCollection((current) => {
      if (current.some((item) => item.id === movie.id)) {
        return current;
      }

      return [...current, movie];
    });
  };

  const removeFromCollection = (movieId) => {
    setCollection((current) =>
      current.filter((movie) => movie.id !== movieId)
    );
  };

  const toggleCollection = (movie) => {
    if (isInCollection(movie.id)) {
      removeFromCollection(movie.id);
    } else {
      addToCollection(movie);
    }
  };

  /* ---------------- PERSISTENCE ---------------- */

  useEffect(() => {
    localStorage.setItem(
      "ohara-watchlist",
      JSON.stringify(watchlist)
    );
  }, [watchlist]);

  useEffect(() => {
    localStorage.setItem(
      "ohara-collection",
      JSON.stringify(collection)
    );
  }, [collection]);

  return (
    <WatchlistContext.Provider
      value={{
        watchlist,
        collection,

        addToWatchlist,
        removeFromWatchlist,
        toggleWatchlist,
        isInWatchlist,

        addToCollection,
        removeFromCollection,
        toggleCollection,
        isInCollection,
      }}
    >
      {children}
    </WatchlistContext.Provider>
  );
}

export function useWatchlist() {
  const context = useContext(WatchlistContext);

  if (!context) {
    throw new Error(
      "useWatchlist must be used inside WatchlistProvider"
    );
  }

  return context;
}