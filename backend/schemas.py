"""
Pydantic schemas used for FastAPI request validation and response serialization.
FastAPI uses these to auto-generate OpenAPI (Swagger) documentation.
"""

from pydantic import BaseModel
from typing import Optional


# --- Genre ---

class GenreSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# --- Director (compact, used inside Movie responses) ---

class DirectorBriefSchema(BaseModel):
    id: int
    name: str
    bio: str
    birth_year: Optional[int]
    photo_url: str

    model_config = {"from_attributes": True}


# --- Actor (compact, used inside Movie list responses) ---

class ActorBriefSchema(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# --- Actor (full, used in actor detail responses) ---

class ActorSchema(BaseModel):
    id: int
    name: str
    bio: str
    birth_year: Optional[int]
    photo_url: str

    model_config = {"from_attributes": True}


# --- Movie (used in list views) ---

class MovieSchema(BaseModel):
    id: int
    title: str
    release_year: int
    synopsis: str
    rating: float
    poster_url: str
    runtime_minutes: Optional[int]
    director: Optional[DirectorBriefSchema]
    genres: list[GenreSchema]
    actors: list[ActorBriefSchema]

    model_config = {"from_attributes": True}


# --- Movie (full detail, includes complete actor info) ---

class MovieDetailSchema(BaseModel):
    id: int
    title: str
    release_year: int
    synopsis: str
    rating: float
    poster_url: str
    runtime_minutes: Optional[int]
    director: Optional[DirectorBriefSchema]
    genres: list[GenreSchema]
    actors: list[ActorSchema]

    model_config = {"from_attributes": True}


# --- Director (full, includes filmography) ---

class DirectorDetailSchema(BaseModel):
    id: int
    name: str
    bio: str
    birth_year: Optional[int]
    photo_url: str
    movies: list[MovieSchema]

    model_config = {"from_attributes": True}


# --- Actor (full, includes filmography) ---

class ActorDetailSchema(BaseModel):
    id: int
    name: str
    bio: str
    birth_year: Optional[int]
    photo_url: str
    movies: list[MovieSchema]

    model_config = {"from_attributes": True}


# --- API response wrappers ---

class MoviesResponse(BaseModel):
    movies: list[MovieSchema]
    count: int
    message: Optional[str] = None


class ActorsResponse(BaseModel):
    actors: list[ActorSchema]
    count: int
    message: Optional[str] = None


class DirectorsResponse(BaseModel):
    directors: list[DirectorBriefSchema]
    count: int
    message: Optional[str] = None


class GenresResponse(BaseModel):
    genres: list[GenreSchema]
    count: int
