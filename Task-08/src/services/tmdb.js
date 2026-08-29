const BASE_URL = "https://api.themoviedb.org/3";

const headers = {
  accept: "application/json",
  Authorization: `Bearer ${import.meta.env.VITE_TMDB_ACCESS_TOKEN}`,
};

async function request(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers,
  });

  if (!response.ok) {
    throw new Error(`TMDB request failed: ${response.status}`);
  }

  return response.json();
}

export function getTrendingMovies() {
  return request("/trending/movie/week");
}

export function getPopularMovies() {
  return request("/movie/popular");
}

export function searchMovies(query) {
  return request(
    `/search/movie?query=${encodeURIComponent(query)}`
  );
}

export function getMovieDetails(id) {
  return request(`/movie/${id}`);
}