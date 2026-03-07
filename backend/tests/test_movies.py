"""
Unit tests for the Movie Explorer API.
Tests cover movie listing, filtering, actor profiles, and edge cases.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Movie, Actor, Director, Genre


@pytest.fixture
def app():
    """Create a test Flask application with an in-memory SQLite database."""
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with test_app.app_context():
        db.create_all()
        _seed_test_data()

    yield test_app

    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


def _seed_test_data():
    """Insert minimal test data into the in-memory database."""
    action = Genre(name="Action")
    drama = Genre(name="Drama")
    db.session.add_all([action, drama])

    director = Director(name="Test Director", birth_year=1970)
    db.session.add(director)

    actor1 = Actor(name="Actor One", birth_year=1980)
    actor2 = Actor(name="Actor Two", birth_year=1985)
    db.session.add_all([actor1, actor2])

    db.session.flush()

    movie1 = Movie(
        title="Test Movie Action",
        release_year=2020,
        synopsis="An action movie.",
        rating=7.5,
        runtime_minutes=120,
        director=director,
        genres=[action],
        actors=[actor1],
    )
    movie2 = Movie(
        title="Test Movie Drama",
        release_year=2021,
        synopsis="A drama movie.",
        rating=8.0,
        runtime_minutes=90,
        director=director,
        genres=[drama],
        actors=[actor2],
    )
    db.session.add_all([movie1, movie2])
    db.session.commit()


# --- Health Check ---

def test_health_check(client):
    """API should return a 200 health status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


# --- Movies ---

def test_get_all_movies(client):
    """Should return all movies when no filters applied."""
    response = client.get("/api/movies/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2
    assert len(data["movies"]) == 2


def test_filter_movies_by_genre(client):
    """Should return only movies matching the genre filter."""
    with client.application.app_context():
        genre = Genre.query.filter_by(name="Action").first()

    response = client.get(f"/api/movies/?genre_id={genre.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1
    assert "Action" in data["movies"][0]["title"]


def test_filter_movies_by_release_year(client):
    """Should return only movies from the specified year."""
    response = client.get("/api/movies/?release_year=2020")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1
    assert data["movies"][0]["release_year"] == 2020


def test_filter_movies_by_invalid_genre(client):
    """Should return 404 when genre_id does not exist."""
    response = client.get("/api/movies/?genre_id=9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_filter_movies_invalid_year(client):
    """Should return 400 for an invalid release year."""
    response = client.get("/api/movies/?release_year=1800")
    assert response.status_code == 400


def test_search_movies_by_title(client):
    """Should find movies by partial title match."""
    response = client.get("/api/movies/?search=drama")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1


def test_no_movies_found(client):
    """Should return empty list with message when no movies match."""
    response = client.get("/api/movies/?search=nonexistentxyz")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 0
    assert "message" in data


def test_get_movie_by_id(client):
    """Should return full movie details including cast."""
    with client.application.app_context():
        movie = Movie.query.first()

    response = client.get(f"/api/movies/{movie.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == movie.id
    assert "actors" in data
    assert "director" in data
    assert "genres" in data


def test_get_movie_not_found(client):
    """Should return 404 for a non-existent movie ID."""
    response = client.get("/api/movies/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


# --- Actors ---

def test_get_all_actors(client):
    """Should return all actors."""
    response = client.get("/api/actors/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2


def test_get_actor_by_id(client):
    """Should return actor profile with movies."""
    with client.application.app_context():
        actor = Actor.query.first()

    response = client.get(f"/api/actors/{actor.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == actor.id
    assert "movies" in data


def test_get_actor_not_found(client):
    """Should return 404 for non-existent actor."""
    response = client.get("/api/actors/9999")
    assert response.status_code == 404


def test_filter_actors_by_genre(client):
    """Should return actors who appeared in movies of a specific genre."""
    with client.application.app_context():
        genre = Genre.query.filter_by(name="Action").first()

    response = client.get(f"/api/actors/?genre_id={genre.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1


# --- Directors ---

def test_get_all_directors(client):
    """Should return all directors."""
    response = client.get("/api/directors/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1


def test_get_director_by_id(client):
    """Should return director profile with filmography."""
    with client.application.app_context():
        director = Director.query.first()

    response = client.get(f"/api/directors/{director.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "movies" in data
    assert len(data["movies"]) == 2


def test_get_director_not_found(client):
    """Should return 404 for non-existent director."""
    response = client.get("/api/directors/9999")
    assert response.status_code == 404


# --- Genres ---

def test_get_all_genres(client):
    """Should return all genres."""
    response = client.get("/api/genres/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 2


def test_get_genre_not_found(client):
    """Should return 404 for non-existent genre."""
    response = client.get("/api/genres/9999")
    assert response.status_code == 404
