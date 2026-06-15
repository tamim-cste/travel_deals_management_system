from database.store import (
    get_all_deals, get_deal_by_id, insert_deal,
    search_deals, filter_deals_by_price, sort_deals, get_recently_viewed
)
from utils.validators import (
    validate_deal, validate_filter_params, validate_sort_params
)
from utils.logger import logger


# ----------- Create -----------------------

def create_deal(data):
    is_valid, errors = validate_deal(data)
    if not is_valid:
        logger.warning(f"Deal creation failed — validation errors: {errors}")
        return None, errors

    sanitised = {
        "destination": data["destination"].strip(),
        "price": float(data["price"]),
        "platform": data["platform"].strip(),
        "rating": float(data["rating"]),
        "travel_type": data["travel_type"],
    }

    deal = insert_deal(sanitised)
    logger.info(f"New deal created: {deal['id']} — {deal['destination']}")
    return deal, None


# ----------- Read -----------------------

def fetch_all_deals():
    deals = get_all_deals()
    logger.info(f"Fetched all deals — total: {len(deals)}")
    return deals


def fetch_deal(deal_id):
    deal = get_deal_by_id(deal_id)
    if deal:
        logger.info(f"Fetched deal: {deal_id}")
    else:
        logger.warning(f"Deal not found: {deal_id}")
    return deal


# ----------- Search -----------------------

def search_deals_service(destination=None, platform=None, travel_type=None):
    if not any([destination, platform, travel_type]):
        logger.warning("Search called with no parameters.")
        return None, "Please provide at least one search parameter (destination, platform, or travel_type)."

    results = search_deals(destination=destination, platform=platform, travel_type=travel_type)
    logger.info(f"Search executed — params: destination={destination}, platform={platform}, travel_type={travel_type} — results: {len(results)}")
    return results, None


# ------------- Filter -----------------------

def filter_deals_service(min_price=None, max_price=None):
    is_valid, errors = validate_filter_params(min_price, max_price)
    if not is_valid:
        logger.warning(f"Filter failed — validation errors: {errors}")
        return None, errors

    results = filter_deals_by_price(min_price=min_price, max_price=max_price)
    logger.info(f"Filter executed — min_price={min_price}, max_price={max_price} — results: {len(results)}")
    return results, None


# ----------- Sort -----------------------

def sort_deals_service(sort_by=None, order=None):
    sort_by = sort_by or "price"
    order = order or "asc"

    is_valid, errors = validate_sort_params(sort_by, order)
    if not is_valid:
        logger.warning(f"Sort failed — validation errors: {errors}")
        return None, errors

    results = sort_deals(sort_by=sort_by, order=order)
    logger.info(f"Sort executed — sort_by={sort_by}, order={order} — results: {len(results)}")
    return results, None


# ----------- Recently Viewed -----------------------

def fetch_recently_viewed():
    deals = get_recently_viewed()
    logger.info(f"Fetched recently viewed deals — total: {len(deals)}")
    return deals