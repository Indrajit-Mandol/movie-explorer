"""
Actor routes for the Movie Explorer API.
Supports filtering actors by movies or genres they acted in.
"""

from flask import Blueprint, jsonify, request
from models import db, Actor, Genre

actors_bp = Blueprint("actors", __name__, url_prefix="/api/actors")


@actors_bp.route("/", methods=["GET"])
def get_actors():
    """
    Get a list of actors with optional filters.
    ---
    tags:
      - Actors
    parameters:
      - name: genre_id
        in: query
        type: integer
        description: Filter actors by genre they acted in
      - name: movie_id
        in: query
        type: integer
        description: Filter actors by movie they appeared in
      - name: search
        in: query
        type: string
        description: Search actors by name
    responses:
      200:
        description: List of actors
      404:
        description: Genre or movie not found
    """
    from models import Movie

    query = Actor.query

    # Filter by genre (actors who acted in movies of this genre)
    genre_id = request.args.get("genre_id", type=int)
    if genre_id is not None:
        genre = Genre.query.get(genre_id)
        if not genre:
            return jsonify({"error": f"Genre with id {genre_id} not found"}), 404
        query = query.filter(
            Actor.movies.any(Movie.genres.any(Genre.id == genre_id))
        )

    # Filter by movie
    movie_id = request.args.get("movie_id", type=int)
    if movie_id is not None:
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify({"error": f"Movie with id {movie_id} not found"}), 404
        query = query.filter(Actor.movies.any(Movie.id == movie_id))

    # Search by name
    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Actor.name.ilike(f"%{search}%"))

    actors = query.order_by(Actor.name).all()

    if not actors:
        return jsonify({"actors": [], "count": 0, "message": "No actors found"}), 200

    return jsonify({"actors": [a.to_dict() for a in actors], "count": len(actors)}), 200


@actors_bp.route("/<int:actor_id>", methods=["GET"])
def get_actor(actor_id):
    """
    Get a single actor by ID with their filmography.
    ---
    tags:
      - Actors
    parameters:
      - name: actor_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Actor profile with movies
      404:
        description: Actor not found
    """
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({"error": f"Actor with id {actor_id} not found"}), 404

    return jsonify(actor.to_dict(include_movies=True)), 200
