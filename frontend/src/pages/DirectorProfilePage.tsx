import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getDirector } from "../api/client";
import type { Director, Movie } from "../types";
import MovieCard from "../components/MovieCard";
import LoadingState from "../components/LoadingState";

/** Shows director profile with bio and filmography. */
export default function DirectorProfilePage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [director, setDirector] = useState<Director | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getDirector(Number(id))
      .then(setDirector)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="container"><LoadingState /></div>;
  if (error || !director) {
    return (
      <div className="container" style={{ paddingTop: 40 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
        <div className="error-state">⚠️ {error ?? "Director not found."}</div>
      </div>
    );
  }

  const movies = (director.movies ?? []) as Movie[];
  const avgRating = movies.length > 0
    ? (movies.reduce((sum, m) => sum + m.rating, 0) / movies.length).toFixed(1)
    : "—";

  return (
    <div className="container" style={{ paddingBottom: 60 }}>
      <div style={{ paddingTop: 32 }}>
        <button className="back-link" onClick={() => navigate(-1)}>← Back</button>
      </div>

      <div className="profile-layout">
        <div className="profile-avatar">
          {director.photo_url ? (
            <img src={director.photo_url} alt={director.name} />
          ) : (
            <span>🎬</span>
          )}
        </div>

        <div>
          <h1 className="profile-name">{director.name}</h1>

          {director.bio && <p className="profile-bio">{director.bio}</p>}

          <div>
            {director.birth_year && (
              <div className="profile-stat">
                <span className="profile-stat-value">{director.birth_year}</span>
                <span className="profile-stat-label">Born</span>
              </div>
            )}
            <div className="profile-stat">
              <span className="profile-stat-value">{movies.length}</span>
              <span className="profile-stat-label">Films</span>
            </div>
            <div className="profile-stat">
              <span className="profile-stat-value">★ {avgRating}</span>
              <span className="profile-stat-label">Avg Rating</span>
            </div>
          </div>
        </div>
      </div>

      {movies.length > 0 && (
        <>
          <div className="section-divider" />
          <div className="section-header">
            <h2 className="section-title">FILMOGRAPHY</h2>
            <span className="section-count">{movies.length} films</span>
          </div>
          <div className="movie-grid">
            {movies.map((m) => <MovieCard key={m.id} movie={m} />)}
          </div>
        </>
      )}
    </div>
  );
}
