import { useEffect, useState } from "react";
import { useFavorites } from "../hooks/useFavorites";
import { getMovie } from "../api/client";
import type { Movie } from "../types";
import MovieCard from "../components/MovieCard";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";

/**
 * Favorites page - shows movies the user has saved.
 * Uses localStorage for persistence (no account required).
 */
export default function FavoritesPage() {
  const { favorites, toggleFavorite } = useFavorites();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (favorites.length === 0) {
      setMovies([]);
      return;
    }
    setLoading(true);
    Promise.all(favorites.map((id) => getMovie(id)))
      .then(setMovies)
      .catch(() => setMovies([]))
      .finally(() => setLoading(false));
  }, [favorites]);

  return (
    <div className="container" style={{ paddingTop: 40, paddingBottom: 60 }}>
      <div className="page-header">
        <h1 className="page-title">★ FAVORITES</h1>
        <p className="page-subtitle">Your saved movies — stored locally in this browser</p>
      </div>

      {loading ? (
        <LoadingState message="Loading favorites..." />
      ) : movies.length === 0 ? (
        <EmptyState
          icon="☆"
          title="No favorites yet"
          message='Browse movies and click "Add to Favorites" to save them here.'
        />
      ) : (
        <>
          <p className="results-count">{movies.length} saved movie{movies.length !== 1 ? "s" : ""}</p>
          <div className="movie-grid">
            {movies.map((movie) => (
              <div key={movie.id} style={{ position: "relative" }}>
                <MovieCard movie={movie} />
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleFavorite(movie.id);
                  }}
                  title="Remove from favorites"
                  style={{
                    position: "absolute",
                    top: 8,
                    left: 8,
                    background: "rgba(0,0,0,0.7)",
                    border: "none",
                    borderRadius: 6,
                    color: "#e8b84b",
                    cursor: "pointer",
                    padding: "3px 8px",
                    fontSize: "0.78rem",
                  }}
                >
                  ★ Remove
                </button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
