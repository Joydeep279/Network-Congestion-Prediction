import os
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd
import yaml
from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


class TrafficPredictor:
    """Handles congestion predictions using a trained pipeline"""

    def __init__(self, config_path: str = ""):
        if not config_path:
            config_path = os.getenv(
                "MODEL_CONFIG", str(PROJECT_ROOT / "core" / "config.yaml")
            )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self.model_path = config.get(
            "model_path",
            os.getenv(
                "MODEL_PATH", str(PROJECT_ROOT / "assets" / "models" / "gb_model.pkl")
            ),
        )
        self.pipeline = self._load_pipeline()

    def _load_pipeline(self):
        """Load the trained pipeline from disk"""
        try:
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Pipeline file not found at {self.model_path}")
            return joblib.load(self.model_path)
        except Exception as e:
            logger.error(f"Failed to load pipeline: {e}")
            raise

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a congestion prediction from raw input data."""
        try:
            df = pd.DataFrame([input_data])

            # The pipeline handles all preprocessing and prediction
            prediction = self.pipeline.predict(df)[0]
            probability = self.pipeline.predict_proba(df)[0][1]

            return {
                "congestion": bool(prediction),
                "probability": float(probability),
            }

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
