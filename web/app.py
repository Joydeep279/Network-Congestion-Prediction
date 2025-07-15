import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
from typing import Any, Dict

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from loguru import logger

from core.predictor import TrafficPredictor

from .email_service import EmailService

load_dotenv()

app = Flask(__name__)
CORS(app)
predictor = TrafficPredictor()
email_service = EmailService()


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        result = predictor.predict(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/feature_importance", methods=["GET"])
def api_feature_importance():
    import os

    import pandas as pd

    fi_path = os.path.join(
        os.path.dirname(predictor.model_path), "feature_importance.csv"
    )
    if not os.path.exists(fi_path):
        return jsonify({"error": "Feature importance not found"}), 404
    fi = pd.read_csv(fi_path)
    return Response(fi.to_json(orient="records"), mimetype="application/json")


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
