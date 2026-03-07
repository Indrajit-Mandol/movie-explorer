import { useState, useCallback } from "react";

const STORAGE_KEY = "movie_explorer_favorites";

/** Reads favorites from localStorage. Returns empty array if missing or invalid. */
function readFavorites(): number[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as number[];
  } catch {
    return [];
  }
}

/**
 * Hook to manage a list of favorite movie IDs stored in localStorage.
 * No user account required — persisted per browser.
 */
export function useFavorites() {
  const [favorites, setFavorites] = useState<number[]>(readFavorites);

  const toggleFavorite = useCallback((movieId: number) => {
    setFavorites((prev) => {
      const next = prev.includes(movieId)
        ? prev.filter((id) => id !== movieId)
        : [...prev, movieId];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const isFavorite = useCallback(
    (movieId: number) => favorites.includes(movieId),
    [favorites]
  );

  return { favorites, toggleFavorite, isFavorite };
}
