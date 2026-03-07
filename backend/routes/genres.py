"""
Genre routes for the Movie Explorer API.
"""

from flask import Blueprint, jsonify
from models import db, Genre

genres_bp = Blueprint("genres", __name__, url_prefix="/api/genres")


@genres_bp.route("/", methods=["GET"])
def get_genres():
    """
    Get a list of all genres.
    ---
    tags:
      - Genres
    responses:
      200:
        description: List of all genres
    """
    genres = Genre.query.order_by(Genre.name).all()

    if not genres:
        return jsonify({"genres": [], "count": 0, "message": "No genres available"}), 200

    return jsonify({"genres": [g.to_dict() for g in genres], "count": len(genres)}), 200


@genres_bp.route("/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    """
    Get a single genre by ID.
    ---
    tags:
      - Genres
    parameters:
      - name: genre_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Genre details
      404:
        description: Genre not found
    """
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"error": f"Genre with id {genre_id} not found"}), 404

    return jsonify(genre.to_dict()), 200
