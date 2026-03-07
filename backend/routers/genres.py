"""
Genre routes for the Movie Explorer API.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Genre
from schemas import GenresResponse, GenreSchema

router = APIRouter(prefix="/api/genres", tags=["Genres"])


@router.get("/", response_model=GenresResponse, summary="List all genres")
def get_genres(db: Session = Depends(get_db)):
    """
    Retrieve a list of all available genres.
    Use the returned genre IDs to filter movies via the `/api/movies/` endpoint.
    """
    genres = db.query(Genre).order_by(Genre.name).all()
    return GenresResponse(
        genres=[GenreSchema.model_validate(g) for g in genres],
        count=len(genres),
    )


@router.get("/{genre_id}", response_model=GenreSchema, summary="Get genre by ID")
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single genre by its ID.

    Raises **404** if the genre does not exist.
    """
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail=f"Genre with id {genre_id} not found")
    return GenreSchema.model_validate(genre)
