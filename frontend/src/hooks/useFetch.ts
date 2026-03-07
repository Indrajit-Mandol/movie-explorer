import { useState, useEffect, useCallback } from "react";

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

/**
 * Generic data-fetching hook.
 * Re-fetches whenever the fetch function reference changes.
 */
export function useFetch<T>(fetchFn: () => Promise<T>): FetchState<T> & { refetch: () => void } {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const execute = useCallback(() => {
    setState({ data: null, loading: true, error: null });
    fetchFn()
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((err: Error) =>
        setState({ data: null, loading: false, error: err.message })
      );
  }, [fetchFn]);

  useEffect(() => {
    execute();
  }, [execute]);

  return { ...state, refetch: execute };
}
