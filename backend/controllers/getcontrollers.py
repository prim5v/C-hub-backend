from backend.utils.db import get_db_cursor

def get_transaction(checkout_requets_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("SELECT * From mpesa_sessions WHERE checkout_requets_id=%s", (checkout_requets_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# from backend.utils.db import get_db_cursor

def get_all_orders(page=1, limit=10):
    conn, cursor = get_db_cursor()
    try:
        offset = (page - 1) * limit

        query = """
        SELECT 
            o.created_at,
            p.product_name,
            (prod->>'quantity')::int AS quantity,
            o.total_price,
            o.payment_method,
            o.status
        FROM orders o
        CROSS JOIN LATERAL jsonb_array_elements(o.products->'products') AS prod
        JOIN products p 
            ON p.product_id = prod->>'product_id'
        ORDER BY o.created_at DESC
        LIMIT %s OFFSET %s;
        """

        cursor.execute(query, (limit, offset))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()