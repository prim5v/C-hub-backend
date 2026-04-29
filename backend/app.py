from flask import Flask, jsonify
from flask_cors import CORS
import logging
from flask_socketio import SocketIO

from backend.routes.auth import auth_bp
# from backend.routes.admin import admin_bp
from backend.routes.mpesaPayments import payments_bp
from backend.middleware.limiter import limiter
from backend.utils.db import check_db_connection

app = Flask(__name__)

CORS(app,
    supports_credentials=True,
    resources={r"/*": {
        "origins": [
            "http://localhost:5173"
        ]
    }}
    ) 

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

# expose it
app.extensions["socketio"] = socketio

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("Starting the Flask application...")
logging.info("Flask application started successfully.")



# ================= EXTENSIONS =================
limiter.init_app(app)


# ================= SOCKET EVENTS =================
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


# ================= ERROR HANDLERS =================
@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({
        "error": "Too many requests — slow down.",
        "details": str(e.description)
    }), 429

# ================= HEALTH CHECK =================
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "Server is alive"
    }), 200


# ================= Health Check =================

@app.route("/")
def health_check():
    return {"status": "healthy"}

# http://127.0.0.1:5000 or http://localhost:5000


@app.route("/health/db")
def db_health():
    is_connected = check_db_connection()

    if is_connected:
        return {
            "status": "healthy",
            "database": "connected"
        }, 200
    else:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }, 500
    
    # http://127.0.0.1:5000/health/db or http://localhost:5000/health/db

# ================= BLUEPRINTS =================
app.register_blueprint(auth_bp)
# app.register_blueprint(admin_bp)
app.register_blueprint(payments_bp)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)

# local runs
# python -m backend.app ---treating as a module, ensures correct imports
# python app.py ---entry point from the backend directory, may cause import issues if run from elsewhere
