"""
Movie routes for the Movie Explorer API.
All filtering is handled server-side via query parameters.
FastAPI auto-generates OpenAPI/Swagger docs from type annotations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Movie, Genre, Director, Actor
from schemas import MoviesResponse, MovieDetailSchema, MovieSchema

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.get("/", response_model=MoviesResponse, summary="List movies with optional filters")
def get_movies(
    genre_id: int | None = Query(None, description="Filter by genre ID"),
    director_id: int | None = Query(None, description="Filter by director ID"),
    actor_id: int | None = Query(None, description="Filter by actor ID"),
    release_year: int | None = Query(None, ge=1888, le=2100, description="Filter by release year"),
    search: str | None = Query(None, description="Search by title (case-insensitive)"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of movies.

    Supports filtering by:
    - **genre_id**: Filter movies belonging to a specific genre
    - **director_id**: Filter movies by a specific director
    - **actor_id**: Filter movies featuring a specific actor
    - **release_year**: Filter movies by exact release year (1888–2100)
    - **search**: Partial, case-insensitive title search

    Returns an empty list with a message when no results are found.
    """
    query = db.query(Movie)

    if genre_id is not None:
        genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if not genre:
            raise HTTPException(status_code=404, detail=f"Genre with id {genre_id} not found")
        query = query.filter(Movie.genres.any(Genre.id == genre_id))

    if director_id is not None:
        director = db.query(Director).filter(Director.id == director_id).first()
        if not director:
            raise HTTPException(status_code=404, detail=f"Director with id {director_id} not found")
        query = query.filter(Movie.director_id == director_id)

    if actor_id is not None:
        actor = db.query(Actor).filter(Actor.id == actor_id).first()
        if not actor:
            raise HTTPException(status_code=404, detail=f"Actor with id {actor_id} not found")
        query = query.filter(Movie.actors.any(Actor.id == actor_id))

    if release_year is not None:
        query = query.filter(Movie.release_year == release_year)

    if search:
        query = query.filter(func.lower(Movie.title).contains(func.lower(search)))

    movies = query.order_by(Movie.release_year.desc()).all()

    message = None
    if not movies:
        message = "No movies found matching the filters"

    return MoviesResponse(
        movies=[MovieSchema.model_validate(m) for m in movies],
        count=len(movies),
        message=message,
    )


@router.get("/{movie_id}", response_model=MovieDetailSchema, summary="Get movie by ID")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve full details for a single movie by its ID.

    Includes complete cast (actors), director info, genres, and synopsis.

    Raises **404** if the movie does not exist.
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")
    return MovieDetailSchema.model_validate(movie)
