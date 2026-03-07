import { useNavigate } from "react-router-dom";
import type { Movie } from "../types";

interface Props {
  movie: Movie;
}

/** Displays a movie as a card with poster, title, year, rating, and genres. */
export default function MovieCard({ movie }: Props) {
  const navigate = useNavigate();

  const getRatingColor = (rating: number) => {
    if (rating >= 8) return "#4caf7d";
    if (rating >= 6.5) return "#e8b84b";
    return "#e85b4b";
  };

  return (
    <div
      className="movie-card"
      onClick={() => navigate(`/movies/${movie.id}`)}
      role="button"
      tabIndex={0}
      aria-label={`View details for ${movie.title}`}
      onKeyDown={(e) => e.key === "Enter" && navigate(`/movies/${movie.id}`)}
    >
      <div className="movie-card-poster">
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={`${movie.title} poster`} loading="lazy" />
        ) : (
          <div className="movie-card-poster-placeholder">
            <span className="poster-icon">🎞️</span>
            <span>{movie.title}</span>
          </div>
        )}
        {movie.rating > 0 && (
          <div
            className="movie-card-rating"
            style={{ color: getRatingColor(movie.rating) }}
            title="Rating out of 10"
          >
            ★ {movie.rating.toFixed(1)}
          </div>
        )}
      </div>
      <div className="movie-card-body">
        <div className="movie-card-title">{movie.title}</div>
        <div className="movie-card-meta">
          {movie.release_year}
          {movie.director && ` · ${movie.director.name}`}
        </div>
        <div className="movie-card-genres">
          {movie.genres.slice(0, 2).map((g) => (
            <span key={g.id} className="genre-badge">
              {g.name}
            </span>
          ))}
          {movie.genres.length > 2 && (
            <span className="genre-badge">+{movie.genres.length - 2}</span>
          )}
        </div>
      </div>
    </div>
  );
}
