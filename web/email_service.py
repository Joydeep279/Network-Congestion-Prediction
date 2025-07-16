import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


class EmailService:
    """Handles sending congestion alert emails"""

    def __init__(self):
        pass

    def send_alert(self, recipient: str, prediction_data: Dict[str, Any]) -> bool:
        """Send congestion alert email"""
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        if not smtp_server or not smtp_user or not smtp_password or not recipient:
            logger.warning(
                "Email alerts disabled - SMTP credentials or recipient not configured"
            )
            return False

        smtp_port = int(os.getenv("SMTP_PORT", 587))

        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_user
            msg["To"] = recipient
            msg["Subject"] = "Network Congestion Alert"

            body = f"""
            <h1>Network Congestion Predicted</h1>
            <p>High probability of network congestion detected:</p>
            <ul>
                <li>Probability: {prediction_data['probability']:.2%}</li>
                <li>Duration: {prediction_data.get('duration', 'N/A')}</li>
                <li>Source Bytes: {prediction_data.get('src_bytes', 'N/A')}</li>
                <li>Destination Bytes: {prediction_data.get('dst_bytes', 'N/A')}</li>
                <li>Packet Count: {prediction_data.get('packet_count', 'N/A')}</li>
                <li>Hour: {prediction_data.get('hour', 'N/A')}</li>
                <li>Protocol: {prediction_data.get('protocol', 'N/A')}</li>
                <li>Service: {prediction_data.get('service', 'N/A')}</li>
            </ul>
            """

            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            logger.success(f"Alert email sent to {recipient}")
            return True

        except Exception as e:
            logger.error(f"Failed to send alert email: {e}")
            return False
