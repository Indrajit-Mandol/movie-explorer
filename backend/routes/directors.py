"""
Director routes for the Movie Explorer API.
"""

from flask import Blueprint, jsonify, request
from models import db, Director

directors_bp = Blueprint("directors", __name__, url_prefix="/api/directors")


@directors_bp.route("/", methods=["GET"])
def get_directors():
    """
    Get a list of all directors.
    ---
    tags:
      - Directors
    parameters:
      - name: search
        in: query
        type: string
        description: Search directors by name
    responses:
      200:
        description: List of directors
    """
    query = Director.query

    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Director.name.ilike(f"%{search}%"))

    directors = query.order_by(Director.name).all()

    if not directors:
        return jsonify({"directors": [], "count": 0, "message": "No directors found"}), 200

    return jsonify({"directors": [d.to_dict() for d in directors], "count": len(directors)}), 200


@directors_bp.route("/<int:director_id>", methods=["GET"])
def get_director(director_id):
    """
    Get a single director by ID with their filmography.
    ---
    tags:
      - Directors
    parameters:
      - name: director_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Director profile with movies
      404:
        description: Director not found
    """
    director = Director.query.get(director_id)
    if not director:
        return jsonify({"error": f"Director with id {director_id} not found"}), 404

    return jsonify(director.to_dict(include_movies=True)), 200
