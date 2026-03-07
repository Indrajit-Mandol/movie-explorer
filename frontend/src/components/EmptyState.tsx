interface Props {
  icon?: string;
  title?: string;
  message?: string;
}

/** Shown when a list has no results (empty search or filters). */
export default function EmptyState({
  icon = "🎞️",
  title = "Nothing found",
  message = "Try adjusting your filters.",
}: Props) {
  return (
    <div className="empty-state" role="status">
      <div className="empty-state-icon">{icon}</div>
      <div className="empty-state-title">{title}</div>
      <div className="empty-state-message">{message}</div>
    </div>
  );
}
