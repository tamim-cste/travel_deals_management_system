from database.store import get_all_deals, get_deal_by_id, insert_deal
from utils.validators import validate_deal


def create_deal(data):
    """
    Validates and creates a new travel deal.
    Returns (deal | None, errors | None)
    """
    is_valid, errors = validate_deal(data)
    if not is_valid:
        return None, errors

    # Sanitise / coerce types before storing
    sanitised = {
        "destination": data["destination"].strip(),
        "price": float(data["price"]),
        "platform": data["platform"].strip(),
        "rating": float(data["rating"]),
        "travel_type": data["travel_type"],
    }

    deal = insert_deal(sanitised)
    return deal, None


def fetch_all_deals():
    """Returns all stored travel deals."""
    return get_all_deals()


def fetch_deal(deal_id):
    """
    Returns a single deal by ID, or None if not found.
    """
    return get_deal_by_id(deal_id)
