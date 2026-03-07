/** Centered loading spinner shown while data is being fetched. */
export default function LoadingState({ message = "Loading..." }: { message?: string }) {
  return (
    <div className="loading-state">
      <div className="loading-spinner" role="status" aria-label={message} />
      <p style={{ color: "var(--text-muted)", fontSize: "0.875rem" }}>{message}</p>
    </div>
  );
}
