"""
Unit tests for the Movie Explorer FastAPI backend.
Uses FastAPI's TestClient (backed by httpx) with an in-memory SQLite database.
Tests cover all endpoints, filters, and edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use in-memory SQLite for tests — isolated from the real database
TEST_DATABASE_URL = "sqlite:///./test_movie_explorer.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override: use the test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import app AFTER defining the override so we can patch the dependency
from main import app
from database import get_db
from models import Base, Movie, Actor, Director, Genre

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables and seed minimal test data before each test; drop after."""
    Base.metadata.create_all(bind=test_engine)
    _seed_test_data()
    yield
    Base.metadata.drop_all(bind=test_engine)


def _seed_test_data():
    """Insert minimal test data for isolated, predictable tests."""
    db = TestingSessionLocal()
    try:
        if db.query(Movie).count() > 0:
            return

        action = Genre(name="Action")
        drama = Genre(name="Drama")
        db.add_all([action, drama])

        director = Director(name="Test Director", bio="A test director.", birth_year=1970)
        db.add(director)

        actor1 = Actor(name="Actor One", bio="First test actor.", birth_year=1980)
        actor2 = Actor(name="Actor Two", bio="Second test actor.", birth_year=1985)
        db.add_all([actor1, actor2])

        db.flush()

        movie1 = Movie(
            title="Test Action Movie",
            release_year=2020,
            synopsis="An action movie for testing.",
            rating=7.5,
            runtime_minutes=120,
            director=director,
            genres=[action],
            actors=[actor1],
        )
        movie2 = Movie(
            title="Test Drama Movie",
            release_year=2021,
            synopsis="A drama movie for testing.",
            rating=8.0,
            runtime_minutes=90,
            director=director,
            genres=[drama],
            actors=[actor2],
        )
        db.add_all([movie1, movie2])
        db.commit()
    finally:
        db.close()


client = TestClient(app)


# ─────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────

def test_health_check():
    """API should return 200 with status ok."""
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


# ─────────────────────────────────────────────────────────────
# Movies — List & Filters
# ─────────────────────────────────────────────────────────────

def test_get_all_movies():
    """Should return all movies with no filters applied."""
    res = client.get("/api/movies/")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 2
    assert len(data["movies"]) == 2


def test_movies_response_shape():
    """Each movie should include required fields."""
    res = client.get("/api/movies/")
    movie = res.json()["movies"][0]
    assert "id" in movie
    assert "title" in movie
    assert "release_year" in movie
    assert "genres" in movie
    assert "director" in movie
    assert "actors" in movie
    assert "rating" in movie


def test_filter_movies_by_genre():
    """Should return only movies that belong to the specified genre."""
    db = TestingSessionLocal()
    genre = db.query(Genre).filter_by(name="Action").first()
    db.close()

    res = client.get(f"/api/movies/?genre_id={genre.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 1
    assert "Action" in data["movies"][0]["title"]


def test_filter_movies_by_director():
    """Should return only movies by the specified director."""
    db = TestingSessionLocal()
    director = db.query(Director).first()
    db.close()

    res = client.get(f"/api/movies/?director_id={director.id}")
    assert res.status_code == 200
    assert res.json()["count"] == 2  # Both test movies have the same director


def test_filter_movies_by_actor():
    """Should return only movies featuring the specified actor."""
    db = TestingSessionLocal()
    actor = db.query(Actor).filter_by(name="Actor One").first()
    db.close()

    res = client.get(f"/api/movies/?actor_id={actor.id}")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_filter_movies_by_release_year():
    """Should return only movies from the specified year."""
    res = client.get("/api/movies/?release_year=2020")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 1
    assert data["movies"][0]["release_year"] == 2020


def test_filter_movies_search_by_title():
    """Should perform a case-insensitive partial title match."""
    res = client.get("/api/movies/?search=drama")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_filter_movies_combined():
    """Combining filters should apply all constraints (AND logic)."""
    db = TestingSessionLocal()
    genre = db.query(Genre).filter_by(name="Action").first()
    db.close()

    res = client.get(f"/api/movies/?genre_id={genre.id}&release_year=2020")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_filter_movies_no_results():
    """Should return empty list with a message when no movies match."""
    res = client.get("/api/movies/?search=zzznomatch")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 0
    assert data["message"] is not None


def test_filter_movies_invalid_genre():
    """Should return 404 when genre_id does not exist."""
    res = client.get("/api/movies/?genre_id=99999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


def test_filter_movies_invalid_director():
    """Should return 404 when director_id does not exist."""
    res = client.get("/api/movies/?director_id=99999")
    assert res.status_code == 404


def test_filter_movies_invalid_actor():
    """Should return 404 when actor_id does not exist."""
    res = client.get("/api/movies/?actor_id=99999")
    assert res.status_code == 404


def test_filter_movies_invalid_year_too_low():
    """Should return 422 for a year below the minimum (1888)."""
    res = client.get("/api/movies/?release_year=1800")
    assert res.status_code == 422  # FastAPI validation error


def test_filter_movies_invalid_year_too_high():
    """Should return 422 for a year above the maximum (2100)."""
    res = client.get("/api/movies/?release_year=9999")
    assert res.status_code == 422


# ─────────────────────────────────────────────────────────────
# Movies — Detail
# ─────────────────────────────────────────────────────────────

def test_get_movie_by_id():
    """Should return full movie detail including cast."""
    db = TestingSessionLocal()
    movie = db.query(Movie).first()
    db.close()

    res = client.get(f"/api/movies/{movie.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == movie.id
    assert "actors" in data
    assert "director" in data
    assert "genres" in data
    assert "synopsis" in data


def test_get_movie_not_found():
    """Should return 404 for a non-existent movie ID."""
    res = client.get("/api/movies/99999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


# ─────────────────────────────────────────────────────────────
# Actors
# ─────────────────────────────────────────────────────────────

def test_get_all_actors():
    """Should return all actors."""
    res = client.get("/api/actors/")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 2


def test_filter_actors_by_genre():
    """Should return only actors who appeared in movies of the given genre."""
    db = TestingSessionLocal()
    genre = db.query(Genre).filter_by(name="Action").first()
    db.close()

    res = client.get(f"/api/actors/?genre_id={genre.id}")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_filter_actors_by_movie():
    """Should return only actors who appeared in the given movie."""
    db = TestingSessionLocal()
    movie = db.query(Movie).first()
    db.close()

    res = client.get(f"/api/actors/?movie_id={movie.id}")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_search_actors_by_name():
    """Should filter actors by partial name match."""
    res = client.get("/api/actors/?search=One")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_get_actor_by_id():
    """Should return actor profile with filmography."""
    db = TestingSessionLocal()
    actor = db.query(Actor).first()
    db.close()

    res = client.get(f"/api/actors/{actor.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == actor.id
    assert "movies" in data


def test_get_actor_not_found():
    """Should return 404 for a non-existent actor ID."""
    res = client.get("/api/actors/99999")
    assert res.status_code == 404


# ─────────────────────────────────────────────────────────────
# Directors
# ─────────────────────────────────────────────────────────────

def test_get_all_directors():
    """Should return all directors."""
    res = client.get("/api/directors/")
    assert res.status_code == 200
    assert res.json()["count"] == 1


def test_get_director_by_id():
    """Should return director profile with their filmography."""
    db = TestingSessionLocal()
    director = db.query(Director).first()
    db.close()

    res = client.get(f"/api/directors/{director.id}")
    assert res.status_code == 200
    data = res.json()
    assert "movies" in data
    assert len(data["movies"]) == 2  # Both test movies belong to this director


def test_get_director_not_found():
    """Should return 404 for a non-existent director ID."""
    res = client.get("/api/directors/99999")
    assert res.status_code == 404


def test_search_directors_by_name():
    """Should filter directors by partial name match."""
    res = client.get("/api/directors/?search=Test")
    assert res.status_code == 200
    assert res.json()["count"] == 1


# ─────────────────────────────────────────────────────────────
# Genres
# ─────────────────────────────────────────────────────────────

def test_get_all_genres():
    """Should return all genres."""
    res = client.get("/api/genres/")
    assert res.status_code == 200
    assert res.json()["count"] == 2


def test_get_genre_by_id():
    """Should return a single genre by ID."""
    db = TestingSessionLocal()
    genre = db.query(Genre).first()
    db.close()

    res = client.get(f"/api/genres/{genre.id}")
    assert res.status_code == 200
    assert res.json()["id"] == genre.id


def test_get_genre_not_found():
    """Should return 404 for a non-existent genre ID."""
    res = client.get("/api/genres/99999")
    assert res.status_code == 404
