import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getMovies } from "../api/client";
import type { Movie } from "../types";
import MovieCard from "../components/MovieCard";
import LoadingState from "../components/LoadingState";

/** Landing page with featured movies and navigation links. */
export default function HomePage() {
  const navigate = useNavigate();
  const [featured, setFeatured] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMovies()
      .then((res) => {
        // Show top 8 by rating for the featured section
        const sorted = [...res.movies].sort((a, b) => b.rating - a.rating);
        setFeatured(sorted.slice(0, 8));
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <div
        style={{
          background: "linear-gradient(135deg, #0a0a0f 0%, #16161f 50%, #1a1226 100%)",
          borderBottom: "1px solid var(--border)",
          padding: "80px 0",
          textAlign: "center",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "radial-gradient(ellipse at 20% 50%, rgba(232,184,75,0.06) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(100,80,200,0.06) 0%, transparent 50%)",
            pointerEvents: "none",
          }}
        />
        <div className="container" style={{ position: "relative" }}>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "clamp(3rem, 8vw, 6rem)",
              letterSpacing: "0.06em",
              color: "var(--text-primary)",
              lineHeight: 1,
              marginBottom: 16,
            }}
          >
            CINESCOPE
          </h1>
          <p
            style={{
              fontSize: "1.1rem",
              color: "var(--text-secondary)",
              maxWidth: 500,
              margin: "0 auto 36px",
              lineHeight: 1.6,
            }}
          >
            Explore films, discover directors, and browse actors all in one place.
          </p>
          <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
            <button
              onClick={() => navigate("/movies")}
              style={{
                background: "var(--accent)",
                color: "#0a0a0f",
                border: "none",
                borderRadius: "var(--radius)",
                padding: "12px 28px",
                fontWeight: 700,
                fontSize: "0.9rem",
                letterSpacing: "0.05em",
                cursor: "pointer",
                transition: "opacity 0.2s",
              }}
              onMouseOver={(e) => (e.currentTarget.style.opacity = "0.88")}
              onMouseOut={(e) => (e.currentTarget.style.opacity = "1")}
            >
              Browse Movies
            </button>
            <button
              onClick={() => navigate("/actors")}
              style={{
                background: "transparent",
                color: "var(--text-primary)",
                border: "1px solid var(--border-accent)",
                borderRadius: "var(--radius)",
                padding: "12px 28px",
                fontWeight: 500,
                fontSize: "0.9rem",
                cursor: "pointer",
              }}
            >
              Explore Actors
            </button>
          </div>
        </div>
      </div>

      {/* Top Rated */}
      <div className="container" style={{ paddingTop: 48, paddingBottom: 60 }}>
        <div className="section-header">
          <h2 className="section-title">TOP RATED</h2>
          <button
            onClick={() => navigate("/movies")}
            style={{
              background: "none",
              border: "none",
              color: "var(--accent)",
              fontSize: "0.85rem",
              cursor: "pointer",
              marginLeft: "auto",
            }}
          >
            View all →
          </button>
        </div>

        {loading ? (
          <LoadingState message="Loading movies..." />
        ) : (
          <div className="movie-grid">
            {featured.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
