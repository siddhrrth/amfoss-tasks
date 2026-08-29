import { Link, NavLink } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <Link to="/" className="logo">
        <span className="logo-mark">◈</span>

        <span>
          OHARA
          <small>ARCHIVE</small>
        </span>
      </Link>

      <nav>
        <NavLink to="/" end>
          Discover
        </NavLink>

        <NavLink to="/watchlist">
          Watchlist
        </NavLink>

        <NavLink to="/collection">
          Collection
        </NavLink>
      </nav>
    </header>
  );
}

export default Navbar;