import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from typing import Any, Dict

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from loguru import logger

from core.predictor import TrafficPredictor

from .email_service import EmailService

load_dotenv()

app = Flask(__name__)
CORS(app)
predictor = TrafficPredictor()
email_service = EmailService()


@app.route("/")
def index():
    """Render the introduction page."""
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        result = predictor.predict(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Handle prediction requests"""
    try:
        data = request.get_json()
        logger.info("Received prediction request", data=data)

        result = predictor.predict(data)

        # Send email alert if congestion predicted with high probability
        alert_email = os.getenv("ALERT_EMAIL")
        if alert_email and result["congestion"] and result["probability"] > 0.9:
            email_service.send_alert(recipient=alert_email, prediction_data=result)

        return (
            jsonify(
                {
                    "congestion": result["congestion"],
                    "probability": result["probability"],
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Prediction API error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
    app.run(debug=debug_mode)
