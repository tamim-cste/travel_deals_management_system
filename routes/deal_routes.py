from flask import Blueprint, request, jsonify

from services.deal_service import (
    create_deal, fetch_all_deals, fetch_deal,
    search_deals_service, filter_deals_service,
    sort_deals_service, fetch_recently_viewed
)
from utils.validators import build_response
from utils.logger import logger

deals_bp = Blueprint("deals", __name__, url_prefix="/deals")


# ---------------- Create Deal ----------------------

@deals_bp.route("", methods=["POST"])
def add_deal():
    """POST /deals — Create a new travel deal."""
    data = request.get_json(silent=True)

    if not data:
        logger.error("POST /deals — invalid or missing JSON body.")
        response, status = build_response(False, "Request body must be valid JSON.", status_code=400)
        return jsonify(response), status

    deal, errors = create_deal(data)

    if errors:
        response, status = build_response(False, "Validation failed.", data={"errors": errors}, status_code=422)
        return jsonify(response), status

    response, status = build_response(True, "Travel deal created successfully.", data=deal, status_code=201)
    return jsonify(response), status


# ---------------- Get All Deals ----------------------

@deals_bp.route("", methods=["GET"])
def get_deals():
    """GET /deals — Retrieve all travel deals."""
    deals = fetch_all_deals()
    response, status = build_response(True, "Deals retrieved successfully.", data={"deals": deals, "total": len(deals)})
    return jsonify(response), status


# ---------------- Search Deals ----------------------

@deals_bp.route("/search", methods=["GET"])
def search_deals():
    """GET /deals/search?destination=dubai&platform=booking&travel_type=Luxury"""
    destination = request.args.get("destination")
    platform = request.args.get("platform")
    travel_type = request.args.get("travel_type")

    results, error = search_deals_service(
        destination=destination,
        platform=platform,
        travel_type=travel_type
    )

    if error:
        response, status = build_response(False, error, status_code=400)
        return jsonify(response), status

    response, status = build_response(
        True,
        f"{len(results)} deal(s) found.",
        data={"deals": results, "total": len(results)}
    )
    return jsonify(response), status


# ---------------- Filter by Budget ----------------------

@deals_bp.route("/filter", methods=["GET"])
def filter_deals():
    """GET /deals/filter?min_price=1000&max_price=5000"""
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    results, errors = filter_deals_service(min_price=min_price, max_price=max_price)

    if errors:
        response, status = build_response(False, "Validation failed.", data={"errors": errors}, status_code=422)
        return jsonify(response), status

    response, status = build_response(
        True,
        f"{len(results)} deal(s) found in the given price range.",
        data={"deals": results, "total": len(results)}
    )
    return jsonify(response), status


# ---------------- Sort Deals ----------------------

@deals_bp.route("/sort", methods=["GET"])
def sort_deals():
    """GET /deals/sort?sort_by=price&order=asc"""
    sort_by = request.args.get("sort_by", "price")
    order = request.args.get("order", "asc")

    results, errors = sort_deals_service(sort_by=sort_by, order=order)

    if errors:
        response, status = build_response(False, "Validation failed.", data={"errors": errors}, status_code=422)
        return jsonify(response), status

    response, status = build_response(
        True,
        f"Deals sorted by '{sort_by}' in '{order}' order.",
        data={"deals": results, "total": len(results)}
    )
    return jsonify(response), status


# ---------------- Recently Viewed ----------------------

@deals_bp.route("/recent", methods=["GET"])
def recently_viewed():
    """GET /deals/recent — Get recently viewed deals."""
    deals = fetch_recently_viewed()

    if not deals:
        response, status = build_response(True, "No recently viewed deals yet.")
        return jsonify(response), status

    response, status = build_response(
        True,
        "Recently viewed deals retrieved successfully.",
        data={"deals": deals, "total": len(deals)}
    )
    return jsonify(response), status


# ---------------- Get Single Deal ----------------------

@deals_bp.route("/<string:deal_id>", methods=["GET"])
def get_deal(deal_id):
    """GET /deals/<deal_id> — Retrieve a single deal."""
    deal = fetch_deal(deal_id)

    if not deal:
        logger.error(f"GET /deals/{deal_id} — not found.")
        response, status = build_response(False, f"Deal with id '{deal_id}' not found.", status_code=404)
        return jsonify(response), status

    response, status = build_response(True, "Deal retrieved successfully.", data=deal)
    return jsonify(response), status