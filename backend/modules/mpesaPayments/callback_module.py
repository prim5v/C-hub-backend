import logging
import json
from flask import jsonify, current_app
from backend.controllers.updatecontrollers import updateMpesaSessionFailed, updateMpesaSessionSuccess
# from backend.app import socketio
from backend.controllers.getcontrollers import get_transaction

logger = logging.getLogger(__name__)
def stk_callback(data):
    try:
        logger.info("📞 MPESA TRANSACTION CALLBACK RECEIVED")
        logger.info(f"📩 RAW DATA: {json.dumps(data)}")

        stk = data.get("Body", {}).get("stkCallback", {})

        result_code = stk.get("ResultCode")
        result_desc = stk.get("ResultDesc")
        checkout_request_id = stk.get("CheckoutRequestID")

        logger.info(f"ResultCode={result_code}, CheckoutRequestID={checkout_request_id}")
        socketio = current_app.extensions["socketio"]

        # ===============================
        # Payment Failed
        # ===============================
        if result_code != 0:
            logger.warning(f"❌ Payment failed: {result_desc}")
            updateMpesaSessionFailed(checkout_request_id)
            socketio.emit("callback:status", {
                "status": "failed",
                "ResultCode": 0
            })
            return jsonify({"ResultCode": 0, "ResultDesc": "Handled"}), 200
        

        # ===============================
        # Payment Successful
        # ===============================
        metadata_items = stk.get("CallbackMetadata", {}).get("Item", [])

        amount = None
        mpesa_receipt = None
        phone = None

        for item in metadata_items:
            name = item.get("Name")
            if name == "Amount":
                amount = item.get("Value")
            elif name == "MpesaReceiptNumber":
                mpesa_receipt = item.get("Value")
            elif name == "PhoneNumber":
                phone = item.get("Value")

        logger.info(f"💰 SUCCESS amount={amount}, receipt={mpesa_receipt}, phone={phone}")

        # Verify transaction exists
        response = get_transaction(checkout_request_id)
        if not response:
            logger.warning("⚠️ No matching transaction found")
            return jsonify({"ResultCode": 0, "ResultDesc": "No transaction"}), 200
        
        # Prevent double processing
        if response["status"] == "success":
            logger.info("ℹ️ Transaction already completed")
            return jsonify({"ResultCode": 0, "ResultDesc": "Already processed"}), 200
        
        # Update transaction
        updateMpesaSessionSuccess(checkout_request_id)
        logger.info("✅ Transaction marked completed")
        socketio.emit("callback:status", {
            "status":"success",
            "ResultCode": 1
        })

        return jsonify({"ResultCode": 1, "ResultDesc": "Success"}), 200


    except Exception:
        logger.exception("🔥 CALLBACK ERROR")

        # Always return 200 to Safaricom
        return jsonify({"ResultCode": 0, "ResultDesc": "Error handled"}), 200