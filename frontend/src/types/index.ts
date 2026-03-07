// Core entity types matching backend models

export interface Genre {
  id: number;
  name: string;
}

export interface Director {
  id: number;
  name: string;
  bio: string;
  birth_year: number | null;
  photo_url: string;
  movies?: Movie[];
}

export interface Actor {
  id: number;
  name: string;
  bio: string;
  birth_year: number | null;
  photo_url: string;
  movies?: Movie[];
}

export interface Movie {
  id: number;
  title: string;
  release_year: number;
  synopsis: string;
  rating: number;
  poster_url: string;
  runtime_minutes: number | null;
  director: Director | null;
  genres: Genre[];
  actors: { id: number; name: string }[] | Actor[];
}

// API response wrappers
export interface MoviesResponse {
  movies: Movie[];
  count: number;
  message?: string;
}

export interface ActorsResponse {
  actors: Actor[];
  count: number;
  message?: string;
}

export interface DirectorsResponse {
  directors: Director[];
  count: number;
  message?: string;
}

export interface GenresResponse {
  genres: Genre[];
  count: number;
}

// Filter state for movie browsing
export interface MovieFilters {
  genre_id?: number;
  director_id?: number;
  actor_id?: number;
  release_year?: number;
  search?: string;
}
