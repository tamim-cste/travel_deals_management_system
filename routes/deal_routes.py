from flask import Blueprint, request, jsonify

from services.deal_service import create_deal, fetch_all_deals, fetch_deal
from utils.validators import build_response

deals_bp = Blueprint("deals", __name__, url_prefix="/deals")


@deals_bp.route("", methods=["POST"])
def add_deal():
    """POST /deals — Create a new travel deal."""
    data = request.get_json(silent=True)

    if not data:
        response, status = build_response(
            False, "Request body must be valid JSON.", status_code=400
        )
        return jsonify(response), status

    deal, errors = create_deal(data)

    if errors:
        response, status = build_response(
            False, "Validation failed.", data={"errors": errors}, status_code=422
        )
        return jsonify(response), status

    response, status = build_response(
        True, "Travel deal created successfully.", data=deal, status_code=201
    )
    return jsonify(response), status


@deals_bp.route("", methods=["GET"])
def get_deals():
    """GET /deals — Retrieve all travel deals."""
    deals = fetch_all_deals()
    response, status = build_response(
        True,
        "Deals retrieved successfully.",
        data={"deals": deals, "total": len(deals)},
    )
    return jsonify(response), status


@deals_bp.route("/<string:deal_id>", methods=["GET"])
def get_deal(deal_id):
    """GET /deals/<deal_id> — Retrieve a single travel deal."""
    deal = fetch_deal(deal_id)

    if not deal:
        response, status = build_response(
            False, f"Deal with id '{deal_id}' not found.", status_code=404
        )
        return jsonify(response), status

    response, status = build_response(True, "Deal retrieved successfully.", data=deal)
    return jsonify(response), status
