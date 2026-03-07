import { useNavigate } from "react-router-dom";

interface Props {
  id: number;
  name: string;
  photo_url?: string;
  birth_year?: number | null;
  movieCount?: number;
  type: "actor" | "director";
}

/** Displays an actor or director as a card with avatar, name, and movie count. */
export default function PersonCard({ id, name, photo_url, birth_year, movieCount, type }: Props) {
  const navigate = useNavigate();
  const path = type === "actor" ? `/actors/${id}` : `/directors/${id}`;

  return (
    <div
      className="person-card"
      onClick={() => navigate(path)}
      role="button"
      tabIndex={0}
      aria-label={`View profile for ${name}`}
      onKeyDown={(e) => e.key === "Enter" && navigate(path)}
    >
      <div className="person-card-avatar">
        {photo_url ? (
          <img src={photo_url} alt={name} loading="lazy" />
        ) : (
          <span>{type === "actor" ? "🎭" : "🎬"}</span>
        )}
      </div>
      <div className="person-card-body">
        <div className="person-card-name">{name}</div>
        <div className="person-card-meta">
          {birth_year && <span>b. {birth_year}</span>}
          {movieCount !== undefined && (
            <span> · {movieCount} film{movieCount !== 1 ? "s" : ""}</span>
          )}
        </div>
      </div>
    </div>
  );
}
