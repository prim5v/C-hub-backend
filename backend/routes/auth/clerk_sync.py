from flask import request
from backend.middleware.auth import require_auth, require_role
from backend.modules.auth.clerk_sync_module import clerk_syncing
from backend.routes.auth import auth_bp


@auth_bp.route("/clerk/sync", methods=['POST'])
@require_auth
def clerk_sync():
    print("🔥 ROUTE HIT")
    data = request.get_json()
    print("📥 REQUEST DATA:", data)
    email = data.get("email")
    print("📧 EMAIL:", email)
    response = clerk_syncing(email)
    return response

# http://127.0.0.1:5000/auth/clerk/sync