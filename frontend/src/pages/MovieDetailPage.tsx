import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getMovie } from "../api/client";
import type { Movie } from "../types";
import { useFavorites } from "../hooks/useFavorites";
import LoadingState from "../components/LoadingState";

/** Displays full details for a single movie: poster, cast, director, genres, synopsis. */
export default function MovieDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isFavorite, toggleFavorite } = useFavorites();

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getMovie(Number(id))
      .then(setMovie)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="container"><LoadingState message="Loading movie..." /></div>;

  if (error || !movie) {
    return (
      <div className="container" style={{ paddingTop: 40 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
        <div className="error-state">
          <p>⚠️ {error ?? "Movie not found."}</p>
        </div>
      </div>
    );
  }

  const getRatingColor = (r: number) =>
    r >= 8 ? "#4caf7d" : r >= 6.5 ? "#e8b84b" : "#e85b4b";

  const favorited = isFavorite(movie.id);

  return (
    <div className="container" style={{ paddingBottom: 60 }}>
      <div style={{ paddingTop: 32 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
      </div>

      <div className="detail-layout">
        {/* Poster */}
        <div>
          <div className="detail-poster">
            {movie.poster_url ? (
              <img src={movie.poster_url} alt={`${movie.title} poster`} />
            ) : (
              <div className="detail-poster-placeholder">
                <span style={{ fontSize: "4rem" }}>🎞️</span>
                <span style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>No poster</span>
              </div>
            )}
          </div>

          {/* Favorites button */}
          <button
            className={`fav-btn ${favorited ? "active" : ""}`}
            onClick={() => toggleFavorite(movie.id)}
            style={{ marginTop: 12, width: "100%", justifyContent: "center" }}
            aria-pressed={favorited}
          >
            {favorited ? "★ In Favorites" : "☆ Add to Favorites"}
          </button>
        </div>

        {/* Info */}
        <div className="detail-info">
          <h1 className="detail-title">{movie.title}</h1>

          <div className="detail-meta-row">
            <span className="detail-year">{movie.release_year}</span>
            {movie.runtime_minutes && (
              <span className="detail-runtime">{movie.runtime_minutes} min</span>
            )}
            {movie.rating > 0 && (
              <span
                className="detail-rating"
                style={{ color: getRatingColor(movie.rating) }}
              >
                <span className="rating-star">★</span>
                {movie.rating.toFixed(1)} / 10
              </span>
            )}
          </div>

          <div className="detail-genres">
            {movie.genres.map((g) => (
              <span key={g.id} className="genre-badge">{g.name}</span>
            ))}
          </div>

          {/* Synopsis */}
          {movie.synopsis && (
            <div className="detail-section">
              <div className="detail-section-title">Synopsis</div>
              <p className="detail-synopsis">{movie.synopsis}</p>
            </div>
          )}

          {/* Director */}
          {movie.director && (
            <div className="detail-section">
              <div className="detail-section-title">Director</div>
              <Link to={`/directors/${movie.director.id}`} className="director-link">
                🎬 {movie.director.name}
              </Link>
            </div>
          )}

          {/* Cast */}
          {movie.actors && movie.actors.length > 0 && (
            <div className="detail-section">
              <div className="detail-section-title">Cast</div>
              <div className="cast-list">
                {movie.actors.map((actor) => (
                  <Link
                    key={actor.id}
                    to={`/actors/${actor.id}`}
                    className="cast-chip"
                  >
                    🎭 {actor.name}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
