from flask import Flask
from flask_cors import CORS
from config import Config
from routes.health import health_bp
from routes.analyze import analyze_bp
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app():
    logger.info("Starting application initialization")
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        logger.info(f"Application configured with DEBUG={app.config.get('DEBUG')}")
        
        CORS(app)
        logger.info("CORS enabled for the application")

        app.register_blueprint(health_bp)
        logger.info("Health blueprint registered")
        
        app.register_blueprint(analyze_bp)
        logger.info("Analyze blueprint registered")

        logger.info("Application initialization completed successfully")
        return app
    except Exception as e:
        logger.error(f"Failed to create application: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting Doc Agent Backend Server")
        app = create_app()
        logger.info("Server starting on host=0.0.0.0, port=8000")
        app.run(host="0.0.0.0", port=8000)
    except Exception as e:
        logger.critical(f"Failed to start server: {str(e)}", exc_info=True)
        raise
