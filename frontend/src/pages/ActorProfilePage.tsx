import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getActor } from "../api/client";
import type { Actor, Movie } from "../types";
import MovieCard from "../components/MovieCard";
import LoadingState from "../components/LoadingState";

/** Shows actor profile with bio and all movies they appeared in. */
export default function ActorProfilePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [actor, setActor] = useState<Actor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getActor(Number(id))
      .then(setActor)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="container"><LoadingState /></div>;
  if (error || !actor) {
    return (
      <div className="container" style={{ paddingTop: 40 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
        <div className="error-state">⚠️ {error ?? "Actor not found."}</div>
      </div>
    );
  }

  const movies = (actor.movies ?? []) as Movie[];

  // Collect all genres from their movies
  const allGenres = Array.from(
    new Map(
      movies.flatMap((m) => m.genres).map((g) => [g.id, g])
    ).values()
  );

  return (
    <div className="container" style={{ paddingBottom: 60 }}>
      <div style={{ paddingTop: 32 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
      </div>

      <div className="profile-layout">
        {/* Avatar */}
        <div>
          <div className="profile-avatar">
            {actor.photo_url ? (
              <img src={actor.photo_url} alt={actor.name} />
            ) : (
              <span>🎭</span>
            )}
          </div>
        </div>

        {/* Info */}
        <div>
          <h1 className="profile-name">{actor.name}</h1>

          {actor.bio && <p className="profile-bio">{actor.bio}</p>}

          <div>
            {actor.birth_year && (
              <div className="profile-stat">
                <span className="profile-stat-value">{actor.birth_year}</span>
                <span className="profile-stat-label">Born</span>
              </div>
            )}
            <div className="profile-stat">
              <span className="profile-stat-value">{movies.length}</span>
              <span className="profile-stat-label">Films</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">{allGenres.length}</span>
              <span className="profile-stat-label">Genres</span>
            </div>
          </div>

          {allGenres.length > 0 && (
            <div style={{ marginTop: 20 }}>
              <div className="detail-section-title">Genres</div>
              <div className="detail-genres" style={{ marginTop: 8 }}>
                {allGenres.map((g) => (
                  <span key={g.id} className="genre-badge">{g.name}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Filmography */}
      {movies.length > 0 && (
        <>
          <div className="section-divider" />
          <div className="section-header">
            <h2 className="section-title">FILMOGRAPHY</h2>
            <span className="section-count">{movies.length} films</span>
          </div>
          <div className="movie-grid">
            {movies.map((m) => (
              <MovieCard key={m.id} movie={m} />
            ))}
          </div>
        </>
      )}

      {movies.length === 0 && (
        <p style={{ color: "var(--text-muted)", marginTop: 24 }}>No films listed yet.</p>
      )}
    </div>
  );
}
