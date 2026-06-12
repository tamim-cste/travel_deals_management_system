VALID_TRAVEL_TYPES = {"Budget", "Luxury", "Adventure", "Family"}

REQUIRED_FIELDS = ["destination", "price", "platform", "rating", "travel_type"]


def validate_deal(data):
    """
    Validates incoming deal data.
    Returns (is_valid: bool, errors: list[str])
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            errors.append(f"'{field}' is required.")

    if errors:
        return False, errors

    # destination cannot be empty
    if not isinstance(data["destination"], str) or not data["destination"].strip():
        errors.append("'destination' cannot be empty.")

    # platform cannot be empty
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


    # travel_type must be one of the allowed values
    if data.get("travel_type") not in VALID_TRAVEL_TYPES:
        errors.append(
            f"'travel_type' must be one of: {', '.join(sorted(VALID_TRAVEL_TYPES))}."
        )

    return (len(errors) == 0), errors


def build_response(success, message, data=None, status_code=200):
    response = {"success": success, "message": message}
    if data is not None:
        response["data"] = data
    return response, status_code
