from decimal import Decimal
import os
import requests
import logging
from requests.auth import HTTPBasicAuth
from flask import request, jsonify, current_app
import base64
from datetime import datetime
# from backend.app import socketio
from backend.controllers.insertcontrollers import insertMpesaSession

logger = logging.getLogger(__name__)


def trigger_mpesa_stk(data):
    phone = data.get("phone")
    amount = data.get("amount")
    user_id = data.get("user_id")
    order_id = data.get("order_id")
    TransactionType = data.get("TransactionType", "CustomerPayBillOnline")  # default to paybill

    socketio = current_app.extensions["socketio"]

    try:
        if not phone or not amount or not user_id:
            return {"error": "Phone, amount and user_id required"}, 400

        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                return {"error": "Invalid amount"}, 400
        except:
            return {"error": "Amount must be numeric"}, 400

        # credentials
        consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        passkey = os.getenv("MPESA_PASSKEY")
        short_code = os.getenv("BUSINESS_SHORT_CODE")
        callback_url = os.getenv("MPESA_CALLBACK_URL")

        if not all([consumer_key, consumer_secret, passkey, short_code]):
            return {"error": "MPESA credentials not configured"}, 500

        # 🔐 AUTH
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        auth_response = requests.get(
            auth_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
            timeout=10
        )

        access_token = auth_response.json().get("access_token")

        # 🔐 PASSWORD
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        raw = f"{short_code}{passkey}{timestamp}"
        encoded_pwd = base64.b64encode(raw.encode()).decode()

        payload = {
            "BusinessShortCode": short_code,
            "Password": encoded_pwd,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone,
            "PartyB": short_code,
            "PhoneNumber": phone,
            "CallBackURL": callback_url,
            "AccountReference": user_id,
            "TransactionDesc": f"Payment of {amount} for user {user_id}"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        # stk_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        response = requests.post(stk_url, json=payload, headers=headers, timeout=15)
        mpesa_response = response.json()

        # ❌ FAILED
        if mpesa_response.get("ResponseCode") != "0":
            socketio.emit("mpesa:status", {
                "status": "failed",
                "details": mpesa_response
            })

            return {"error": "STK push failed", "details": mpesa_response}, 400

        # ✅ SUCCESS
        checkout_request_id = mpesa_response.get("CheckoutRequestID")

        insertMpesaSession(checkout_request_id, amount, order_id, user_id, TransactionType)

        socketio.emit("mpesa:status", {
            "status": "pending",
            "checkout_request_id": checkout_request_id,
            "user_id": user_id
        })

        return {
            "message": "STK sent",
            "checkout_request_id": checkout_request_id
        }, 200

    except Exception as e:
        logger.exception("MPESA error")
        return {"error": "Internal server error"}, 500