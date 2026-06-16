from database.store import get_api_usage_stats, record_api_request
from utils.logger import logger


def fetch_api_stats():
    stats = get_api_usage_stats()
    logger.info(
        f"Stats retrieved — total={stats['total_requests']}, "
        f"success={stats['successful_requests']}, failed={stats['failed_requests']}"
    )
    return stats


def track_request(status_code):
    success = 200 <= status_code < 400
    record_api_request(success)