"""
Database models for Movie Explorer Platform.
Uses pure SQLAlchemy (no Flask) — compatible with FastAPI.
Defines Movies, Actors, Directors, and Genres with their relationships.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, ForeignKey, Table
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table: many-to-many between Movie and Genre
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

# Association table: many-to-many between Movie and Actor
movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id"), primary_key=True),
)


class Genre(Base):
    """Represents a film genre (e.g., Action, Drama)."""
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)


class Director(Base):
    """Represents a film director."""
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    bio = Column(Text, default="")
    birth_year = Column(Integer, nullable=True)
    photo_url = Column(String(500), default="")

    movies = relationship("Movie", back_populates="director", lazy="select")


class Actor(Base):
    """Represents a film actor."""
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    bio = Column(Text, default="")
    birth_year = Column(Integer, nullable=True)
    photo_url = Column(String(500), default="")

    movies = relationship("Movie", secondary=movie_actors, back_populates="actors", lazy="select")


class Movie(Base):
    """Represents a film with its metadata and relationships."""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False, index=True)
    release_year = Column(Integer, nullable=False, index=True)
    synopsis = Column(Text, default="")
    rating = Column(Float, default=0.0)
    poster_url = Column(String(500), default="")
    runtime_minutes = Column(Integer, nullable=True)

    director_id = Column(Integer, ForeignKey("directors.id"), nullable=True)
    director = relationship("Director", back_populates="movies")

    genres = relationship("Genre", secondary=movie_genres, lazy="select")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies", lazy="select")
