import json
from flask import request
from backend.routes.mpesaPayments import payments_bp
from backend.modules.mpesaPayments.callback_module import stk_callback

@payments_bp.route("/mpesa/stk/callback", methods=['POST', 'GET'])
def callback():
    data = request.get_json()
    return stk_callback(data)

    