import logging
import os

import json
from upstash_redis import Redis
from backend.controllers.getcontrollers import check_rooms
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

logger = logging.getLogger(__name__)

def fetch_rooms(campus_id):
    try:
        cache_key = f"campus_rooms:{campus_id}"
        cached = None
        try:
            cached = redis_client.get(cache_key)
        except Exception as redis_error:
            logger.warning(f"REDIS_GET_FAILED: {redis_error}")

        if cached:
            rows = json.loads(cached)
            return rows
        else:
            rooms = check_rooms(campus_id)
            if not rooms:
                return {"error": "No rooms found for the given campus_id"}, 404
            
            response = []

            for room in rooms:
                # room_id = room["id"]

                response.append({
                    "id": room["id"],
                    "title": room["title"],
                    "type": room["room_type"],
                    "distance": room["distance"],
                    "price": float(room["price"]),
                    "currency": "KES",

                    "location": room["location"],

                    "beds": room["beds"],
                    "baths": room["baths"],
                    "wifi": room["wifi"],
                    "furnished": room["furnished"],
                    "selfContained": room["self_contained"],

                    "images": room["images"],
                    "amenities": room["amenities"],

                    "description": room["room_description"],
                    "deposits": room["deposits"],
                    "extras": room["extras"]
                })    
            # Cache the response for 1 hour
            try:
                redis_client.set(cache_key, json.dumps(response), ex=900)
            except Exception as redis_error:
                logger.warning(f"REDIS_SET_FAILED: {redis_error}")
            return response
    except Exception as e:
        logger.error(f"ERROR_FETCHING_ROOMS: {e}")
        return {"error": "An error occurred while fetching rooms"}, 500

