VALID_TRAVEL_TYPES = {"Budget", "Luxury", "Adventure", "Family"}
VALID_SORT_FIELDS = {"price", "rating", "destination", "created_at"}
VALID_SORT_ORDERS = {"asc", "desc"}

REQUIRED_FIELDS = ["destination", "price", "platform", "rating", "travel_type"]
DEFAULT_POPULAR_LIMIT = 10

# ---------------- Deal Creation Validation ---------------------

def validate_deal(data):
    """Validates incoming deal data. Returns (is_valid, errors)."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            errors.append(f"'{field}' is required.")

    if errors:
        return False, errors

    if not isinstance(data["destination"], str) or not data["destination"].strip():
        errors.append("'destination' cannot be empty.")

    if not isinstance(data["platform"], str) or not data["platform"].strip():
        errors.append("'platform' cannot be empty.")

    try:
        price = float(data["price"])
        if price <= 0:
            errors.append("'price' must be a positive number.")
    except (TypeError, ValueError):
        errors.append("'price' must be a valid number.")

    try:
        rating = float(data["rating"])
        if not (1 <= rating <= 5):
            errors.append("'rating' must be between 1 and 5.")
    except (TypeError, ValueError):
        errors.append("'rating' must be a valid number.")

    if data.get("travel_type") not in VALID_TRAVEL_TYPES:
        errors.append(
            f"'travel_type' must be one of: {', '.join(sorted(VALID_TRAVEL_TYPES))}."
        )

    return (len(errors) == 0), errors


# ------------------ Filter Validation ----------------------

def validate_filter_params(min_price, max_price):
    """Validates budget filter query params. Returns (is_valid, errors)."""
    errors = []

    if min_price is not None:
        try:
            min_price = float(min_price)
            if min_price < 0:
                errors.append("'min_price' cannot be negative.")
        except (TypeError, ValueError):
            errors.append("'min_price' must be a valid number.")

    if max_price is not None:
        try:
            max_price = float(max_price)
            if max_price < 0:
                errors.append("'max_price' cannot be negative.")
        except (TypeError, ValueError):
            errors.append("'max_price' must be a valid number.")

    # Cross-field validation
    if min_price is not None and max_price is not None:
        try:
            if float(max_price) < float(min_price):
                errors.append("'max_price' cannot be smaller than 'min_price'.")
        except (TypeError, ValueError):
            pass  # already caught above

    return (len(errors) == 0), errors



# ------------------ Sort Validation ----------------------

def validate_sort_params(sort_by, order):
    """Validates sort query params. Returns (is_valid, errors)."""
    errors = []

    if sort_by and sort_by not in VALID_SORT_FIELDS:
        errors.append(
            f"'sort_by' must be one of: {', '.join(sorted(VALID_SORT_FIELDS))}."
        )

    if order and order.lower() not in VALID_SORT_ORDERS:
        errors.append("'order' must be 'asc' or 'desc'.")

    return (len(errors) == 0), errors





#--------------------Limit -------------------------------

def validate_limit_param(limit):
    """Returns (is_valid, errors, parsed_limit)."""
    errors = []
    parsed_limit = DEFAULT_POPULAR_LIMIT

    if limit is not None:
        try:
            parsed_limit = int(limit)
            if parsed_limit <= 0:
                errors.append("'limit' must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("'limit' must be a valid integer.")

    return (len(errors) == 0), errors, parsed_limit



# ------------------ Response Helper ----------------------

def build_response(success, message, data=None, status_code=200):
    response = {"success": success, "message": message}
    if data is not None:
        response["data"] = data
    return response, status_code