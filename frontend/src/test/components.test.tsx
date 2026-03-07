/**
 * Frontend unit tests for components and hooks.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import MovieCard from "../components/MovieCard";
import PersonCard from "../components/PersonCard";
import EmptyState from "../components/EmptyState";
import LoadingState from "../components/LoadingState";
import { useFavorites } from "../hooks/useFavorites";
import { renderHook, act } from "@testing-library/react";
import type { Movie } from "../types";

// ---------- Mock Data ----------

const mockMovie: Movie = {
  id: 1,
  title: "Inception",
  release_year: 2010,
  synopsis: "A mind-bending thriller.",
  rating: 8.8,
  poster_url: "",
  runtime_minutes: 148,
  director: { id: 1, name: "Christopher Nolan", bio: "", birth_year: 1970, photo_url: "" },
  genres: [{ id: 1, name: "Sci-Fi" }, { id: 2, name: "Action" }],
  actors: [{ id: 1, name: "Leonardo DiCaprio" }],
};

const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// ---------- MovieCard ----------

describe("MovieCard", () => {
  beforeEach(() => mockNavigate.mockClear());

  it("renders movie title and year", () => {
    render(<MemoryRouter><MovieCard movie={mockMovie} /></MemoryRouter>);
    expect(screen.getByText("Inception")).toBeInTheDocument();
    expect(screen.getByText(/2010/)).toBeInTheDocument();
  });

  it("renders genre badges", () => {
    render(<MemoryRouter><MovieCard movie={mockMovie} /></MemoryRouter>);
    expect(screen.getByText("Sci-Fi")).toBeInTheDocument();
    expect(screen.getByText("Action")).toBeInTheDocument();
  });

  it("renders rating", () => {
    render(<MemoryRouter><MovieCard movie={mockMovie} /></MemoryRouter>);
    expect(screen.getByText(/8.8/)).toBeInTheDocument();
  });

  it("navigates to movie detail on click", () => {
    render(<MemoryRouter><MovieCard movie={mockMovie} /></MemoryRouter>);
    fireEvent.click(screen.getByRole("button"));
    expect(mockNavigate).toHaveBeenCalledWith("/movies/1");
  });

  it("shows placeholder when no poster_url", () => {
    render(<MemoryRouter><MovieCard movie={{ ...mockMovie, poster_url: "" }} /></MemoryRouter>);
    expect(screen.getByText("Inception")).toBeInTheDocument();
  });

  it("shows director name in meta", () => {
    render(<MemoryRouter><MovieCard movie={mockMovie} /></MemoryRouter>);
    expect(screen.getByText(/Christopher Nolan/)).toBeInTheDocument();
  });

  it("shows +N badge for more than 2 genres", () => {
    const movie = {
      ...mockMovie,
      genres: [
        { id: 1, name: "Sci-Fi" },
        { id: 2, name: "Action" },
        { id: 3, name: "Drama" },
      ],
    };
    render(<MemoryRouter><MovieCard movie={movie} /></MemoryRouter>);
    expect(screen.getByText("+1")).toBeInTheDocument();
  });
});

// ---------- PersonCard ----------

describe("PersonCard", () => {
  beforeEach(() => mockNavigate.mockClear());

  it("renders actor name", () => {
    render(
      <MemoryRouter>
        <PersonCard id={1} name="Tom Hanks" type="actor" birth_year={1956} movieCount={5} />
      </MemoryRouter>
    );
    expect(screen.getByText("Tom Hanks")).toBeInTheDocument();
  });

  it("renders birth year and film count", () => {
    render(
      <MemoryRouter>
        <PersonCard id={1} name="Tom Hanks" type="actor" birth_year={1956} movieCount={5} />
      </MemoryRouter>
    );
    expect(screen.getByText(/1956/)).toBeInTheDocument();
    expect(screen.getByText(/5 films/)).toBeInTheDocument();
  });

  it("navigates to actor profile on click", () => {
    render(
      <MemoryRouter>
        <PersonCard id={2} name="Meryl Streep" type="actor" />
      </MemoryRouter>
    );
    fireEvent.click(screen.getByRole("button"));
    expect(mockNavigate).toHaveBeenCalledWith("/actors/2");
  });

  it("navigates to director profile for director type", () => {
    render(
      <MemoryRouter>
        <PersonCard id={3} name="Nolan" type="director" />
      </MemoryRouter>
    );
    fireEvent.click(screen.getByRole("button"));
    expect(mockNavigate).toHaveBeenCalledWith("/directors/3");
  });
});

// ---------- EmptyState ----------

describe("EmptyState", () => {
  it("renders default empty state", () => {
    render(<EmptyState />);
    expect(screen.getByText("Nothing found")).toBeInTheDocument();
  });

  it("renders custom title and message", () => {
    render(<EmptyState title="No movies" message="Add some movies." />);
    expect(screen.getByText("No movies")).toBeInTheDocument();
    expect(screen.getByText("Add some movies.")).toBeInTheDocument();
  });
});

// ---------- LoadingState ----------

describe("LoadingState", () => {
  it("renders spinner with default message", () => {
    render(<LoadingState />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("renders custom message", () => {
    render(<LoadingState message="Fetching data..." />);
    expect(screen.getByText("Fetching data...")).toBeInTheDocument();
  });
});

// ---------- useFavorites hook ----------

describe("useFavorites", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("starts with empty favorites", () => {
    const { result } = renderHook(() => useFavorites());
    expect(result.current.favorites).toEqual([]);
  });

  it("adds a movie to favorites", () => {
    const { result } = renderHook(() => useFavorites());
    act(() => result.current.toggleFavorite(42));
    expect(result.current.favorites).toContain(42);
    expect(result.current.isFavorite(42)).toBe(true);
  });

  it("removes a movie when toggled again", () => {
    const { result } = renderHook(() => useFavorites());
    act(() => result.current.toggleFavorite(42));
    act(() => result.current.toggleFavorite(42));
    expect(result.current.favorites).not.toContain(42);
    expect(result.current.isFavorite(42)).toBe(false);
  });

  it("persists to localStorage", () => {
    const { result } = renderHook(() => useFavorites());
    act(() => result.current.toggleFavorite(7));
    const stored = JSON.parse(localStorage.getItem("movie_explorer_favorites") ?? "[]");
    expect(stored).toContain(7);
  });

  it("can manage multiple favorites", () => {
    const { result } = renderHook(() => useFavorites());
    act(() => {
      result.current.toggleFavorite(1);
      result.current.toggleFavorite(2);
      result.current.toggleFavorite(3);
    });
    expect(result.current.favorites).toHaveLength(3);
  });
});
