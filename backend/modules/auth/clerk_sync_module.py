import logging
import time
from backend.utils.db import get_db_cursor
from flask import jsonify, g

logger = logging.getLogger(__name__)

def clerk_syncing(email):
    start_time = time.time()

    clerk_id = getattr(g, "user_id", None)
    email = getattr(g, "email", None) or email

    logger.info(
        "SYNC_START",
        extra={
            "clerk_id": clerk_id,
            "email_present": bool(email)
        }
    )

    # 🔥 VALIDATION
    if not clerk_id:
        logger.warning("SYNC_ABORT_NO_USER_ID")
        return jsonify({"error": "Missing user_id from token"}), 401

    if not email:
        logger.warning(
            "SYNC_ABORT_NO_EMAIL",
            extra={"clerk_id": clerk_id}
        )
        return jsonify({"error": "Email is required"}), 400

    conn, cursor = get_db_cursor()

    if not conn:
        logger.error("DB_CONNECTION_FAILED")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # 🔍 check if user exists
        logger.debug("DB_CHECK_USER_EXISTS", extra={"clerk_id": clerk_id})

        cursor.execute(
            "SELECT * FROM users WHERE clerk_id = %s",
            (clerk_id,)
        )
        user = cursor.fetchone()

        if not user:
            logger.info(
                "USER_NOT_FOUND_CREATING",
                extra={"clerk_id": clerk_id, "email": email}
            )

            cursor.execute(
                """
                INSERT INTO users (clerk_id, email, role)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (clerk_id, email, "customer")
            )

            conn.commit()
            user = cursor.fetchone()

            logger.info(
                "USER_CREATED",
                extra={"clerk_id": clerk_id}
            )

            return jsonify({
                "message": "User created",
                "user": user
            }), 201

        logger.info(
            "USER_EXISTS",
            extra={"clerk_id": clerk_id}
        )

        return jsonify({
            "message": "User already exists",
            "user": user
        }), 200

    except Exception as e:
        conn.rollback()

        logger.exception(
            "SYNC_FAILED_EXCEPTION",
            extra={"clerk_id": clerk_id}
        )

        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

        logger.info(
            "SYNC_END",
            extra={
                "clerk_id": clerk_id,
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }
        )