import { NavLink } from "react-router-dom";

/** Top navigation bar with links to all main sections. */
export default function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar-brand">
        🎬 CINESCOPE
      </NavLink>
      <ul className="navbar-links">
        <li>
          <NavLink
            to="/movies"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Movies
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/actors"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Actors
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/directors"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Directors
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/favorites"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            ★ Favorites
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}
