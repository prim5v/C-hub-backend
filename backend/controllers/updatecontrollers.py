from backend.utils.db import get_db_cursor

def updateMpesaSessionFailed(checkout_request_id):
    conn, cursor = get_db_cursor()

    try:
        cursor.execute(
            """
            UPDATE mpesa_sessions
            SET status='failed'
            WHERE checkout_request_id=%s
            """(checkout_request_id,)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def updateMpesaSessionSuccess(checkout_request_id):
    conn, cursor = get_db_cursor()

    try:
        cursor.execute(
            """
            UPDATE mpesa_sessions
            SET status='success'
            WHERE checkout_request_id=%s
            """(checkout_request_id,)
        )
        conn.commit()

    finally:
        cursor.close()
        conn.close()