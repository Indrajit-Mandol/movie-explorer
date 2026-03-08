

import type {
  MoviesResponse,
  ActorsResponse,
  DirectorsResponse,
  GenresResponse,
  Movie,
  Actor,
  Director,
  MovieFilters,
} from "../types";

const BASE_URL = "/api";

/** Generic fetch wrapper with error handling */
async function apiFetch<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Unknown error" }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

/** Build query string from filter object, skipping undefined/empty values */
function buildQuery(filters: Record<string, string | number | undefined>): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value !== undefined && value !== "" && value !== 0) {
      params.set(key, String(value));
    }
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

// --- Movies ---

export const getMovies = (filters: MovieFilters = {}): Promise<MoviesResponse> => {
  const query = buildQuery(filters as Record<string, string | number | undefined>);
  return apiFetch<MoviesResponse>(`/movies/${query}`);
};

export const getMovie = (id: number): Promise<Movie> => {
  return apiFetch<Movie>(`/movies/${id}`);
};

// --- Actors ---

export const getActors = (filters: { genre_id?: number; movie_id?: number; search?: string } = {}): Promise<ActorsResponse> => {
  const query = buildQuery(filters as Record<string, string | number | undefined>);
  return apiFetch<ActorsResponse>(`/actors/${query}`);
};

export const getActor = (id: number): Promise<Actor> => {
  return apiFetch<Actor>(`/actors/${id}`);
};

// --- Directors ---

export const getDirectors = (filters: { search?: string } = {}): Promise<DirectorsResponse> => {
  const query = buildQuery(filters as Record<string, string | number | undefined>);
  return apiFetch<DirectorsResponse>(`/directors/${query}`);
};

export const getDirector = (id: number): Promise<Director> => {
  return apiFetch<Director>(`/directors/${id}`);
};

// --- Genres ---

export const getGenres = (): Promise<GenresResponse> => {
  return apiFetch<GenresResponse>(`/genres/`);
};
