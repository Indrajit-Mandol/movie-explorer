

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import db
from routes.movies import movies_bp
from routes.actors import actors_bp
from routes.directors import directors_bp
from routes.genres import genres_bp


def create_app(config=None):
    """
    Application factory pattern for creating the Flask app.
    Accepts an optional config dict to override defaults (used in testing).
    """
    app = Flask(__name__)

    # Default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///movie_explorer.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Override with test config if provided
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Swagger/OpenAPI configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/",
    }

    swagger_template = {
        "info": {
            "title": "Movie Explorer API",
            "description": "API for browsing movies, actors, directors, and genres.",
            "version": "1.0.0",
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http", "https"],
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints
    app.register_blueprint(movies_bp)
    app.register_blueprint(actors_bp)
    app.register_blueprint(directors_bp)
    app.register_blueprint(genres_bp)

    # Health check endpoint
    @app.route("/api/health")
    def health():
        """Health check endpoint."""
        return jsonify({"status": "ok", "message": "Movie Explorer API is running"}), 200

    # Handle 404 errors
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    # Handle 405 Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    # Handle 500 Internal Server Errors
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        # Seed the database with initial data
        from seed_data import seed_database
        seed_database(app)

    app.run(host="0.0.0.0", port=5000, debug=True)
