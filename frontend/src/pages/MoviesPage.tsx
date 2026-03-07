import { useState, useCallback, useEffect } from "react";
import { getMovies, getGenres, getDirectors, getActors } from "../api/client";
import type { Movie, Genre, Director, Actor, MovieFilters } from "../types";
import MovieCard from "../components/MovieCard";
import LoadingState from "../components/LoadingState";
import EmptyState from "../components/EmptyState";

/**
 * Main movies browsing page.
 * All filtering is sent to the backend — no client-side filtering.
 */
export default function MoviesPage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);
  const [directors, setDirectors] = useState<Director[]>([]);
  const [actors, setActors] = useState<Actor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [count, setCount] = useState(0);

  const [filters, setFilters] = useState<MovieFilters>({});

  // Load filter options on mount
  useEffect(() => {
    Promise.all([getGenres(), getDirectors(), getActors()]).then(
      ([g, d, a]) => {
        setGenres(g.genres);
        setDirectors(d.directors);
        setActors(a.actors);
      }
    );
  }, []);

  // Fetch movies whenever filters change
  const fetchMovies = useCallback(() => {
    setLoading(true);
    setError(null);
    getMovies(filters)
      .then((res) => {
        setMovies(res.movies);
        setCount(res.count);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [filters]);

  useEffect(() => {
    fetchMovies();
  }, [fetchMovies]);

  const updateFilter = (key: keyof MovieFilters, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value === "" ? undefined : key === "search" ? value : Number(value),
    }));
  };

  const clearFilters = () => setFilters({});
  const hasFilters = Object.values(filters).some((v) => v !== undefined && v !== "");

  return (
    <div className="container" style={{ paddingTop: 40, paddingBottom: 60 }}>
      <div className="page-header">
        <h1 className="page-title">MOVIES</h1>
        <p className="page-subtitle">Browse and filter the full catalogue</p>
      </div>

      {/* Filters */}
      <div className="filters-bar">
        {/* Search */}
        <div className="filter-group search-wrapper" style={{ flex: 2 }}>
          <label className="filter-label">Search</label>
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="filter-input"
            placeholder="Search by title..."
            value={filters.search ?? ""}
            onChange={(e) => updateFilter("search", e.target.value)}
            aria-label="Search movies"
          />
        </div>

        {/* Genre */}
        <div className="filter-group">
          <label className="filter-label">Genre</label>
          <select
            className="filter-select"
            value={filters.genre_id ?? ""}
            onChange={(e) => updateFilter("genre_id", e.target.value)}
            aria-label="Filter by genre"
          >
            <option value="">All Genres</option>
            {genres.map((g) => (
              <option key={g.id} value={g.id}>{g.name}</option>
            ))}
          </select>
        </div>

        {/* Director */}
        <div className="filter-group">
          <label className="filter-label">Director</label>
          <select
            className="filter-select"
            value={filters.director_id ?? ""}
            onChange={(e) => updateFilter("director_id", e.target.value)}
            aria-label="Filter by director"
          >
            <option value="">All Directors</option>
            {directors.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
        </div>

        {/* Actor */}
        <div className="filter-group">
          <label className="filter-label">Actor</label>
          <select
            className="filter-select"
            value={filters.actor_id ?? ""}
            onChange={(e) => updateFilter("actor_id", e.target.value)}
            aria-label="Filter by actor"
          >
            <option value="">All Actors</option>
            {actors.map((a) => (
              <option key={a.id} value={a.id}>{a.name}</option>
            ))}
          </select>
        </div>

        {/* Year */}
        <div className="filter-group" style={{ minWidth: 120 }}>
          <label className="filter-label">Year</label>
          <input
            type="number"
            className="filter-input"
            placeholder="e.g. 2010"
            min={1888}
            max={2100}
            value={filters.release_year ?? ""}
            onChange={(e) => updateFilter("release_year", e.target.value)}
            aria-label="Filter by release year"
          />
        </div>

        {hasFilters && (
          <button className="filter-clear-btn" onClick={clearFilters}>
            ✕ Clear
          </button>
        )}
      </div>

      {/* Results */}
      {!loading && !error && (
        <p className="results-count">
          {count} movie{count !== 1 ? "s" : ""} found
        </p>
      )}

      {loading ? (
        <LoadingState message="Loading movies..." />
      ) : error ? (
        <div className="error-state">
          <p>⚠️ {error}</p>
          <button onClick={fetchMovies} style={{ marginTop: 12, padding: "8px 16px", background: "transparent", border: "1px solid currentColor", borderRadius: 6, color: "inherit", cursor: "pointer" }}>
            Retry
          </button>
        </div>
      ) : movies.length === 0 ? (
        <EmptyState
          icon="🎞️"
          title="No movies found"
          message={hasFilters ? "Try adjusting or clearing your filters." : "No movies are available."}
        />
      ) : (
        <div className="movie-grid">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  );
}
