from flask import Flask
from flask_cors import CORS

from config import Config
from routes.health import health_bp
from routes.analyze import analyze_bp
from utils.logger import setup_logger

HOST = "0.0.0.0"
PORT = 8000

logger = setup_logger(__name__)


def create_app() -> Flask:
    logger.info("Initializing Flask application")

    try:
        app = Flask(__name__)
        app.config.from_object(Config)

        logger.info(
            "Application configuration loaded | DEBUG=%s",
            app.config.get("DEBUG")
        )

        # Enable CORS
        CORS(app)
        logger.info("CORS successfully enabled")

        # Register blueprints
        app.register_blueprint(health_bp)
        logger.info("Health routes registered")

        app.register_blueprint(analyze_bp)
        logger.info("Analyze routes registered")

        logger.info("Flask application initialized successfully")
        return app

    except Exception as exc:
        logger.error(
            "Application initialization failed",
            exc_info=True
        )
        raise exc


if __name__ == "__main__":
    try:
        logger.info("Starting Doc Agent Backend Server")
        app = create_app()

        logger.info(
            "Server running on host=%s port=%s",
            HOST,
            PORT
        )

        app.run(host=HOST, port=PORT)

    except Exception as exc:
        logger.critical(
            "Server startup failed",
            exc_info=True
        )
        raise exc