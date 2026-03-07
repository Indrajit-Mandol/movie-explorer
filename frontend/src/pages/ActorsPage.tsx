import { useState, useEffect, useCallback } from "react";
import { getActors, getGenres } from "../api/client";
import type { Actor, Genre } from "../types";
import PersonCard from "../components/PersonCard";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";

/** Browse all actors, filterable by genre. */
export default function ActorsPage() {
  const [actors, setActors] = useState<Actor[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [genreFilter, setGenreFilter] = useState<number | undefined>();
  const [search, setSearch] = useState("");

  useEffect(() => {
    getGenres().then((g) => setGenres(g.genres));
  }, []);

  const fetch = useCallback(() => {
    setLoading(true);
    setError(null);
    getActors({ genre_id: genreFilter, search: search || undefined })
      .then((res) => setActors(res.actors))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [genreFilter, search]);

  useEffect(() => { fetch(); }, [fetch]);

  return (
    <div className="container" style={{ paddingTop: 40, paddingBottom: 60 }}>
      <div className="page-header">
        <h1 className="page-title">ACTORS</h1>
        <p className="page-subtitle">Discover the talent behind the films</p>
      </div>

      <div className="filters-bar">
        <div className="filter-group search-wrapper" style={{ flex: 2 }}>
          <label className="filter-label">Search</label>
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="filter-input"
            placeholder="Search actors..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search actors by name"
          />
        </div>
        <div className="filter-group">
          <label className="filter-label">Genre</label>
          <select
            className="filter-select"
            value={genreFilter ?? ""}
            onChange={(e) => setGenreFilter(e.target.value ? Number(e.target.value) : undefined)}
            aria-label="Filter actors by genre"
          >
            <option value="">All Genres</option>
            {genres.map((g) => (
              <option key={g.id} value={g.id}>{g.name}</option>
            ))}
          </select>
        </div>
        {(genreFilter || search) && (
          <button className="filter-clear-btn" onClick={() => { setGenreFilter(undefined); setSearch(""); }}>
            ✕ Clear
          </button>
        )}
      </div>

      <p className="results-count">{actors.length} actor{actors.length !== 1 ? "s" : ""}</p>

      {loading ? (
        <LoadingState message="Loading actors..." />
      ) : error ? (
        <div className="error-state">⚠️ {error}</div>
      ) : actors.length === 0 ? (
        <EmptyState icon="🎭" title="No actors found" message="Try adjusting your filters." />
      ) : (
        <div className="person-grid">
          {actors.map((a) => (
            <PersonCard
              key={a.id}
              id={a.id}
              name={a.name}
              photo_url={a.photo_url}
              birth_year={a.birth_year}
              movieCount={a.movies?.length}
              type="actor"
            />
          ))}
        </div>
      )}
    </div>
  );
}
