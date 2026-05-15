from flask import request
from backend.middleware.auth import require_auth, require_role
from backend.modules.comrade.getNearCampusesModule import get_nearby_campuses
from backend.routes.comrade import comrade_bp

@comrade_bp.route("/nearby-campuses", methods=["GET, POST"])
@require_auth
@require_role("comrade")
def get_nearby_campuses_route():
    return get_nearby_campuses()
