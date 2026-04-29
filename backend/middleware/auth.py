from functools import wraps
from flask import request, jsonify, g
from jose import jwt
import requests

from backend.utils.db import get_db_cursor

import logging

logger = logging.getLogger(__name__)

# ================= CONFIG =================

CLERK_JWKS_URL = "https://well-ladybird-60.clerk.accounts.dev/.well-known/jwks.json"
CLERK_ISSUER = "https://well-ladybird-60.clerk.accounts.dev"

_jwks_cache = None


# ================= JWT HELPERS =================

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        _jwks_cache = requests.get(CLERK_JWKS_URL).json()
    return _jwks_cache


def verify_clerk_token(token):
    jwks = get_jwks()

    try:
        headers = jwt.get_unverified_header(token)

        key = next(
            k for k in jwks["keys"]
            if k["kid"] == headers["kid"]
        )

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=CLERK_ISSUER
        )

        return payload

    except Exception as e:
        print("Invalid token:", e)
        return None


# ================= DECORATORS =================

# backend/middleware/auth.py



def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        logger.info("AUTH_MIDDLEWARE_START")

        auth_header = request.headers.get("Authorization")

        logger.debug(
            "Authorization header received",
            extra={"has_auth_header": bool(auth_header)}
        )

        if not auth_header:
            logger.warning("Missing Authorization header")
            return jsonify({"error": "Missing Authorization header"}), 401

        parts = auth_header.split(" ")
        if len(parts) != 2:
            logger.warning(
                "Invalid Authorization format",
                extra={"auth_header": auth_header}
            )
            return jsonify({"error": "Invalid Authorization format"}), 401

        token = parts[1]

        logger.debug(
            "Token extracted",
            extra={"token_length": len(token)}
        )

        try:
            payload = verify_clerk_token(token)
            logger.info("RAW_CLAIM_DEBUG: %s", payload)
            
        except Exception as e:
            logger.exception("Token verification crashed")
            return jsonify({"error": "Token verification error"}), 401

        if not payload:
            logger.warning("Invalid or expired token")
            return jsonify({"error": "Invalid or expired token"}), 401

        user_id = payload.get("sub")
        if not user_id:
            logger.warning(
                "Missing user_id in payload",
                extra={"payload": payload}
            )
            return jsonify({"error": "Invalid token payload"}), 401

        # email = None
        # email_addresses = payload.get("email_addresses")

        # if isinstance(email_addresses, list) and email_addresses:
        #     email = email_addresses[0].get("email_address")
        email = payload.get("email")

        if not email:
            email = payload.get("primary_email_address")

        if not email:
            email_addresses = payload.get("email_addresses")

            if isinstance(email_addresses, list) and email_addresses:
                email = email_addresses[0].get("email_address")

        g.user = payload
        g.user_id = user_id
        g.email = email

        logger.info(
            "AUTH_SUCCESS",
            extra={
                "user_id": user_id,
                "email_present": email is not None
            }
        )

        return f(*args, **kwargs)

    return decorated





def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # get user_id from require_auth
            user_id = getattr(g, "user_id", None)

            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            conn, cursor = get_db_cursor()

            if not conn:
                return jsonify({"error": "Database connection failed"}), 500

            try:
                cursor.execute(
                    "SELECT role FROM users WHERE clerk_id = %s",
                    (user_id,)
                )
                user = cursor.fetchone()

                if not user:
                    return jsonify({"error": "User not found"}), 403

                if user["role"] != required_role:
                    return jsonify({
                        "error": "Forbidden: insufficient permissions"
                    }), 403

            finally:
                cursor.close()
                conn.close()

            return f(*args, **kwargs)

        return wrapper
    return decorator
