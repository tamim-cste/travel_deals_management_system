from flask import Blueprint, jsonify

from services.stats_service import fetch_api_stats
from utils.validators import build_response

stats_bp = Blueprint("stats", __name__, url_prefix="/stats")


@stats_bp.route("", methods=["GET"])
def get_stats():
    stats = fetch_api_stats()
    response, status = build_response(True, "API usage statistics retrieved successfully.", data=stats)
    return jsonify(response), status