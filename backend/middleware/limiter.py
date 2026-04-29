# backend/utils/limiter.py

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import g


def get_user_or_ip():
    """
    Use authenticated user_id if available,
    otherwise fallback to IP address.
    """

    return getattr(g, "user_id", None) or get_remote_address()


limiter = Limiter(
    key_func=get_user_or_ip,
    default_limits=["200 per day", "50 per hour"],
)