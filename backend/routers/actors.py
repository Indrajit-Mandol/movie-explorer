"""
Actor routes for the Movie Explorer API.
Supports filtering actors by movies or genres they acted in.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Actor, Genre, Movie
from schemas import ActorsResponse, ActorDetailSchema, ActorSchema

router = APIRouter(prefix="/api/actors", tags=["Actors"])


@router.get("/", response_model=ActorsResponse, summary="List actors with optional filters")
def get_actors(
    genre_id: int | None = Query(None, description="Filter actors by genre they appeared in"),
    movie_id: int | None = Query(None, description="Filter actors by a specific movie"),
    search: str | None = Query(None, description="Search actors by name"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of actors.

    Supports filtering by:
    - **genre_id**: Actors who appeared in movies of this genre
    - **movie_id**: Actors who appeared in a specific movie
    - **search**: Partial, case-insensitive name search
    """
    query = db.query(Actor)

    if genre_id is not None:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(status_code=404, detail=f"Genre with id {genre_id} not found")
        query = query.filter(
            Actor.movies.any(Movie.genres.any(Genre.id == genre_id))
        )

    if movie_id is not None:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")
        query = query.filter(Actor.movies.any(Movie.id == movie_id))

    if search:
        query = query.filter(Actor.name.ilike(f"%{search}%"))

    actors = query.order_by(Actor.name).all()

    message = None
    if not actors:
        message = "No actors found"

    return ActorsResponse(
        actors=[ActorSchema.model_validate(a) for a in actors],
        count=len(actors),
        message=message,
    )


@router.get("/{actor_id}", response_model=ActorDetailSchema, summary="Get actor profile by ID")
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve an actor's full profile including their filmography.

    Raises **404** if the actor does not exist.
    """
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail=f"Actor with id {actor_id} not found")
    return ActorDetailSchema.model_validate(actor)
