from flask import Blueprint, jsonify
from utils.logger import setup_logger

health_bp = Blueprint("health", __name__)
logger = setup_logger(__name__)

@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint used for monitoring and load balancers.
    """
    logger.debug("Health check requested")
    return jsonify({
        "status": "ok",
        "service": "doc-agent-backend"
    })
