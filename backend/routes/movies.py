"""
Movie routes for the Movie Explorer API.
Supports filtering by genre, director, release year, and actor.
"""

from flask import Blueprint, jsonify, request
from models import db, Movie, Genre, Director, Actor

movies_bp = Blueprint("movies", __name__, url_prefix="/api/movies")


@movies_bp.route("/", methods=["GET"])
def get_movies():
    """
    Get a list of movies with optional filters.
    ---
    tags:
      - Movies
    parameters:
      - name: genre_id
        in: query
        type: integer
        description: Filter by genre ID
      - name: director_id
        in: query
        type: integer
        description: Filter by director ID
      - name: actor_id
        in: query
        type: integer
        description: Filter by actor ID
      - name: release_year
        in: query
        type: integer
        description: Filter by release year
      - name: search
        in: query
        type: string
        description: Search by title (case-insensitive)
    responses:
      200:
        description: List of movies
      400:
        description: Invalid filter parameters
    """
    query = Movie.query

    # Filter by genre
    genre_id = request.args.get("genre_id", type=int)
    if genre_id is not None:
        genre = Genre.query.get(genre_id)
        if not genre:
            return jsonify({"error": f"Genre with id {genre_id} not found"}), 404
        query = query.filter(Movie.genres.any(Genre.id == genre_id))

    # Filter by director
    director_id = request.args.get("director_id", type=int)
    if director_id is not None:
        director = Director.query.get(director_id)
        if not director:
            return jsonify({"error": f"Director with id {director_id} not found"}), 404
        query = query.filter(Movie.director_id == director_id)

    # Filter by actor
    actor_id = request.args.get("actor_id", type=int)
    if actor_id is not None:
        actor = Actor.query.get(actor_id)
        if not actor:
            return jsonify({"error": f"Actor with id {actor_id} not found"}), 404
        query = query.filter(Movie.actors.any(Actor.id == actor_id))

    # Filter by release year
    release_year = request.args.get("release_year", type=int)
    if release_year is not None:
        if release_year < 1888 or release_year > 2100:
            return jsonify({"error": "Invalid release year"}), 400
        query = query.filter(Movie.release_year == release_year)

    # Search by title
    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))

    movies = query.order_by(Movie.release_year.desc()).all()

    if not movies:
        return jsonify({"movies": [], "count": 0, "message": "No movies found matching the filters"}), 200

    return jsonify({"movies": [m.to_dict() for m in movies], "count": len(movies)}), 200


@movies_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    """
    Get a single movie by ID with full cast details.
    ---
    tags:
      - Movies
    parameters:
      - name: movie_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Movie details
      404:
        description: Movie not found
    """
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"error": f"Movie with id {movie_id} not found"}), 404

    return jsonify(movie.to_dict(include_cast=True)), 200
