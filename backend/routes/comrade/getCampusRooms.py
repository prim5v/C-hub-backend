from backend.routes.comrade import comrade_bp
from backend.modules.comrade.getCampusRoomsModule import fetch_rooms

@comrade_bp.route("/comrade/campusrooms/<int:campus_id>/rooms", methods=["GET"])
def get_campus_rooms(campus_id):

    if campus_id <= 0:
        return {"error": "Invalid campus_id"}, 400

    result = fetch_rooms(campus_id)

    # if fetch_rooms already returns error tuple
    if isinstance(result, tuple):
        return result

    return {"data": result}, 200