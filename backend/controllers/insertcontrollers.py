import uuid

from backend.utils.db import get_db_cursor

def insertMpesaSession(checkout_request_id, amount, order_id, user_id, TransactionType):
    conn, cursor = get_db_cursor()

    try:
        session_id = uuid.uuid4().hex[:8].upper()
        cursor.execute(
            """
            INSERT INTO mpesa_sessions
            (session_id, checkout_request_id, amount, order_id, user_id, TransactionType)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (session_id, checkout_request_id, amount, order_id, user_id, TransactionType)
        )

        conn.commit()

    finally:
        cursor.close()
        conn.close()

def insertMpesaSession(mpesa_code, total_price, order_id, user_id, TransactionType):
    conn, cursor = get_db_cursor()

    try:
        session_id = uuid.uuid4().hex[:8].upper()
        cursor.execute(
            """
            INSERT INTO mpesa_sessions
            (session_id, mpesa_receipt_code, amount, order_id, user_id, TransactionType)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (session_id, mpesa_code, total_price, order_id, user_id, TransactionType)
        )

        conn.commit()

    finally:
        cursor.close()
        conn.close()


def insertOrder(user_id, order_id, products, total_price, delivery_address, status, payment_method):
    conn, cursor = get_db_cursor()

    try:
        cursor.execute(
            """
            INSERT INTO orders (user_id, order_id, products, delivery_address, total_price, status, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, order_id, products, delivery_address, total_price, status)
        )

        conn.commit()

    finally:
        cursor.close()
        conn.close()