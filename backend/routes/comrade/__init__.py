from flask import Blueprint

comrade_bp = Blueprint("comrade", __name__, url_prefix="/comrade")

from . import getNearCampuses, getCampusRooms

