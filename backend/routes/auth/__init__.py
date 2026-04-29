# routes/auth
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Import the route modules so they are registered with the blueprint eg
# from . import login, register, logout

from . import clerk_sync