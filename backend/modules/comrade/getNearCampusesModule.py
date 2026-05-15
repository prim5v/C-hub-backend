import math
import logging
import json
from flask import request, jsonify
from backend.utils.db import get_db_cursor
from backend.utils.extraFunctions import haversine_distance
from upstash_redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

logger = logging.getLogger(__name__)

def get_nearby_campuses():
    conn = None
    cursor = None

    try:
        data = request.get_json()

        user_lat = data.get("lat")
        user_lng = data.get("lng")

        if user_lat is None or user_lng is None:
            return jsonify({"error": "lat and lng required"}), 400

        user_lat = float(user_lat)
        user_lng = float(user_lng)

        # 🔥 CACHE CAMPUSES (NOT USER LOCATION)
        cache_key = "campuses:all"

        cached = None
        try:
            cached = redis_client.get(cache_key)
        except Exception:
            pass

        if cached:
            rows = json.loads(cached)
        else:
            conn, cursor = get_db_cursor()

            cursor.execute("""
                SELECT id, name, campus, color, initials, coordinates
                FROM campuses
            """)

            rows = cursor.fetchall()

            # store raw DB result in cache
            try:
                redis_client.set(cache_key, json.dumps(rows), ex=3600)
            except Exception:
                pass

        results = []
        nearest_index = None
        nearest_distance = float("inf")

        for i, row in enumerate(rows):
            coords = row["coordinates"]

            lat2 = float(coords["lat"])
            lng2 = float(coords["lng"])

            distance_m = haversine_distance(
                user_lat, user_lng,
                lat2, lng2
            )

            is_near = distance_m <= 30000

            if distance_m < nearest_distance:
                nearest_distance = distance_m
                nearest_index = i

            results.append({
                "id": str(row["id"]),
                "name": row["name"],
                "campus": row["campus"],
                "distance": f"{round(distance_m / 1000, 1)} km",
                "isNear": is_near,
                "initial": row["initials"],
                "color": row["color"],
                "coordinate": {
                    "latitude": lat2,
                    "longitude": lng2
                }
            })

        if nearest_index is not None:
            results[nearest_index]["isNear"] = True

        return jsonify(results), 200

    except Exception as e:
        logger.exception("NEARBY_CAMPUSES_FAILED")
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()