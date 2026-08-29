# Task 08 — The Ohara Archive 

An interactive movie discovery, archival, and personal curation web application built with **React** and **Vite**, powered by the **TMDB (The Movie Database) API**. 

Inspired by the concept of the *Library of Ohara*, this project serves as a cinematic archive where users can discover trending titles, execute real-time searches, inspect rich metadata, and curate persistent personal **Watchlists** and **Collections**.


## Tech Stack & Core Libraries

- **Frontend Framework:** React (Vite-powered SPA)
- **Routing:** React Router v6 (`BrowserRouter`, `Routes`, `Route`, `useParams`, `useNavigate`)
- **State Management:** React Context API (`useContext`, `useReducer` / `useState`)
- **Persistence Layer:** Browser `localStorage` API
- **API Integration:** TMDB API (v3 REST endpoints) via native `fetch` / asynchronous services
- **Styling:** Custom Vanilla CSS with a responsive dark-mode library aesthetic

---

## Key Features & Technical Implementation

### 1. Centralized API Service (`src/services/tmdb.js`)
- Abstracted TMDB API communication into modular service functions (`getTrendingMovies`, `searchMovies`, `getMovieDetails`).
- Handled authentication securely via Vite environment variables (`VITE_TMDB_ACCESS_TOKEN`) using authorization Bearer headers.
- Implemented robust error handling and response parsing for movie posters, backdrop paths, genre IDs, and ratings.

### 2. Global State & Persistence (`src/context/WatchlistContext.jsx`)
- Built a custom **React Context** (`WatchlistContext` & `useWatchlist` hook) to avoid prop drilling and provide global access to both **Watchlist** and **Collection** records.
- Implemented bidirectional synchronisation with `window.localStorage`:
  - Automatically loads existing bookmarks on initial mount.
  - Persists state updates (`addMovie`, `removeMovie`, `toggleCollection`) instantaneously as serialized JSON.

### 3. Dynamic Routing & Deep Linking (`React Router`)
- Configured clean, client-side SPA navigation:
  - `/` → Trending feed (`Home.jsx`)
  - `/search` → Search queries and live dynamic results (`Search.jsx`)
  - `/movie/:id` → Detailed metadata view with dynamic route params (`MovieDetails.jsx`)
  - `/watchlist` → Saved prospective watch items (`Watchlist.jsx`)
  - `/collection` → Personally curated archive of favorite films (`Collection.jsx`)

### 4. Modular UI Components
- **`MovieCard.jsx`:** Encapsulated individual movie preview card with hover states, release year formatting, vote score badges, and direct action triggers (Add to Watchlist / Collection).
- **`MovieGrid.jsx`:** Reusable responsive CSS grid component adaptable across Trending, Search, Watchlist, and Collection views with graceful empty states.
- **`Navbar.jsx`:** Responsive navigational header with active route styling and quick search access.

---

## Project Structure

```text
Task-08/
├── src/
│   ├── components/
│   │   ├── MovieCard.jsx        # Reusable movie display card with action controls
│   │   ├── MovieGrid.jsx        # Responsive grid layout wrapper
│   │   └── Navbar.jsx           # Global navigation bar with route links
│   │
│   ├── context/
│   │   └── WatchlistContext.jsx # Global state management & localStorage sync
│   │
│   ├── pages/
│   │   ├── Home.jsx             # Trending movies showcase
│   │   ├── Search.jsx           # Search input and results grid
│   │   ├── MovieDetails.jsx     # Full metadata, cast, runtime, backdrop & overview
│   │   ├── Watchlist.jsx        # Saved to-watch list
│   │   └── Collection.jsx       # Personal curated library
│   │
│   ├── services/
│   │   └── tmdb.js              # TMDB API requests & authentication headers
│   │
│   ├── App.jsx                  # Main routing configuration & Context Provider
│   ├── main.jsx                 # Application root entry point
│   └── index.css                # Global theme variables, typography & layout styles
│
├── .env.example                 # Template for required environment variables
├── package.json                 # Dependencies and build scripts
└── README.md
```

---

## Local Setup and Installation

### Prerequisites
- Node.js (v18.0.0 or higher recommended)
- npm or yarn package manager
- A free TMDB API Account & Read Access Token ([TMDB API Settings](https://www.themoviedb.org/settings/api))

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Task-08.git
cd Task-08
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the root of the project:
```bash
cp .env.example .env
```
Add your TMDB API Read Access Token:
```env
VITE_TMDB_ACCESS_TOKEN=your_tmdb_read_access_token_here
```

### 4. Run the development server
```bash
npm run dev
```
Open your browser at `http://localhost:5173` to view the application.

### 5. Build for Production
```bash
npm run build
```

---

## Key Learnings & Engineering Takeaways

- **State Architecture with React Context:** Architected a single-source-of-truth context provider (`WatchlistContext`) to manage independent lists (`watchlist` vs `collection`) without unnecessary re-renders.
- **Persistent Client Storage:** Handled edge cases in `localStorage` synchronization, including JSON parsing validation, default state fallback, and quota management.
- **REST API Consumption:** Structured asynchronous requests with `fetch`/`axios` inside custom service layers (`tmdb.js`), abstracting endpoint URLs, parameter serialization, and image asset path prefixing (`https://image.tmdb.org/t/p/w500`).
- **Client-Side Routing:** Implemented dynamic route matching (`/movie/:id`) and programmatic navigation with React Router hooks (`useParams`, `useNavigate`).
- **Responsive Layout Design:** Designed fluid card grid systems utilizing modern CSS Grid (`grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))`) and Flexbox layouts.

---
