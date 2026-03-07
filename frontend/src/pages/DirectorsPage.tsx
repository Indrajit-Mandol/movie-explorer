import { useState, useEffect, useCallback } from "react";
import { getDirectors } from "../api/client";
import type { Director } from "../types";
import PersonCard from "../components/PersonCard";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";

/** Browse all directors. */
export default function DirectorsPage() {
  const [directors, setDirectors] = useState<Director[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const fetch = useCallback(() => {
    setLoading(true);
    setError(null);
    getDirectors({ search: search || undefined })
      .then((res) => setDirectors(res.directors))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [search]);

  useEffect(() => { fetch(); }, [fetch]);

  return (
    <div className="container" style={{ paddingTop: 40, paddingBottom: 60 }}>
      <div className="page-header">
        <h1 className="page-title">DIRECTORS</h1>
        <p className="page-subtitle">The visionaries behind the camera</p>
      </div>

      <div className="filters-bar">
        <div className="filter-group search-wrapper" style={{ flex: 1, maxWidth: 400 }}>
          <label className="filter-label">Search</label>
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="filter-input"
            placeholder="Search directors..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search directors by name"
          />
        </div>
        {search && (
          <button className="filter-clear-btn" onClick={() => setSearch("")}>
            ✕ Clear
          </button>
        )}
      </div>

      <p className="results-count">{directors.length} director{directors.length !== 1 ? "s" : ""}</p>

      {loading ? (
        <LoadingState message="Loading directors..." />
      ) : error ? (
        <div className="error-state">⚠️ {error}</div>
      ) : directors.length === 0 ? (
        <EmptyState icon="🎬" title="No directors found" message="Try a different search term." />
      ) : (
        <div className="person-grid">
          {directors.map((d) => (
            <PersonCard
              key={d.id}
              id={d.id}
              name={d.name}
              photo_url={d.photo_url}
              birth_year={d.birth_year}
              movieCount={d.movies?.length}
              type="director"
            />
          ))}
        </div>
      )}
    </div>
  );
}
