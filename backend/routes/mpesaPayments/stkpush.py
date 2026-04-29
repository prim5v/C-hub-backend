from flask import request, jsonify
from backend.routes.mpesaPayments import payments_bp
from backend.modules.mpesaPayments.stkpush_module import trigger_mpesa_stk
from backend.middleware.auth import require_auth, require_role
from backend.middleware.limiter import limiter

@payments_bp.route("/mpesa/stk/push", methods=['POST', 'GET'])
@require_auth
@require_role(['admin'])
@limiter.limit("10 per minute")
def stk_push():
    data = request.get_json()
    return trigger_mpesa_stk(data)