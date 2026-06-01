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


def get_all_campuses():
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT id, name, campus, color, initials, coordinates
            FROM campuses
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# def check_rooms(campus_id):
#     conn, cursor = get_db_cursor()
#     try:
#         cursor.execute("""
#             SELECT  FROM rooms WHERE campus_id = %s
#         """, (campus_id,))
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         conn.close()


def get_room_accommodation(room_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT beds, baths, wifi, furnished, self_contained
            FROM accommodation
            WHERE room_id = %s
        """, (room_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_room_images(room_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT image_url
            FROM images
            WHERE room_id = %s
        """, (room_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_room_amenities(room_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT 
                a.amenity_key,
                a.label
            FROM room_amenities ra
            JOIN amenities a ON ra.amenity_id = a.id
            WHERE ra.room_id = %s
        """, (room_id,))

        rows = cursor.fetchall()

        # convert to clean JSON object
        amenities = {}
        for row in rows:
            amenities[row["amenity_key"]] = row["label"]

        return amenities

    finally:
        cursor.close()
        conn.close()


def get_room_location(room_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT *
            FROM location_data
            WHERE room_id = %s
        """, (room_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def check_rooms(campus_id):
    conn, cursor = get_db_cursor()
    try:
        cursor.execute("""
            SELECT 
                r.id,
                r.title,
                r.room_type,
                r.distance,
                r.price,
                r.room_description,

                COALESCE(a.beds, 0) AS beds,
                COALESCE(a.baths, 0) AS baths,
                COALESCE(a.wifi, false) AS wifi,
                COALESCE(a.furnished, false) AS furnished,
                COALESCE(a.self_contained, false) AS self_contained,

                COALESCE(l.address, '') AS location,

                COALESCE(
                    json_agg(DISTINCT i.image_url) 
                    FILTER (WHERE i.image_url IS NOT NULL),
                    '[]'
                ) AS images,

                COALESCE(
                    json_agg(DISTINCT jsonb_build_object(
                        'key', am.amenity_key,
                        'label', am.label
                    )) FILTER (WHERE am.id IS NOT NULL),
                    '[]'
                ) AS amenities

            FROM rooms r

            LEFT JOIN accomodatives a ON a.room_id = r.id
            LEFT JOIN location_data l ON l.room_id = r.id
            LEFT JOIN images i ON i.room_id = r.id
            LEFT JOIN room_amenities ra ON ra.room_id = r.id
            LEFT JOIN amenities am ON am.id = ra.amenity_id

            WHERE r.campus_id = %s

            GROUP BY r.id, a.id, l.id
        """, (campus_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()