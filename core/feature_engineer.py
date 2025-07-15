from typing import Any, Dict, List

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.preprocessing import OneHotEncoder


class FeatureEngineer:
    """Handles feature engineering for network traffic data"""

    def __init__(self):
        self.required_columns = {
            "duration": "conn_duration",
            "src_bytes": "src_bytes",
            "dst_bytes": "dst_bytes",
            "packet_count": "packet_count",
            "service_count": "service_count",
        }
        self.peak_morning_hours = set(range(8, 11))  # 8-10
        self.peak_evening_hours = set(range(17, 20))  # 17-19

    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw data into engineered features"""
        try:
            # Validate input data
            self._validate_input(data)

            # Initialize features with basic mapping
            features = self._map_basic_features(data)

            # Add derived features
            features.update(
                {
                    "peak_hour_flag": self._is_peak_hour(data.get("hour", 0)),
                    "packet_size_variance": self._calculate_variance(data),
                    "bytes_ratio": self._calculate_bytes_ratio(data),
                    "avg_packet_size": self._calculate_avg_packet_size(data),
                    "traffic_intensity": self._calculate_traffic_intensity(data),
                }
            )

            # Validate output features
            self._validate_output(features)

            logger.debug("Engineered features", features=features)
            return features

        except ValueError as e:
            logger.error(f"Invalid input data: {e}")
            raise
        except Exception as e:
            logger.error(f"Feature engineering failed: {e}")
            raise

    def _validate_input(self, data: Dict[str, Any]) -> None:
        """Validate input data structure and values"""
        missing = [col for col in self.required_columns.keys() if col not in data]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        for col in self.required_columns:
            try:
                val = float(data[col])
                if val < 0:
                    raise ValueError(f"Negative value in column {col}: {val}")
            except (TypeError, ValueError):
                raise ValueError(f"Invalid value in column {col}: {data[col]}")

    def _validate_output(self, features: Dict[str, Any]) -> None:
        """Validate engineered features"""
        expected_features = list(self.required_columns.values()) + [
            "peak_hour_flag",
            "packet_size_variance",
            "bytes_ratio",
            "avg_packet_size",
            "traffic_intensity",
        ]
        missing = [feat for feat in expected_features if feat not in features]
        if missing:
            raise ValueError(f"Missing engineered features: {missing}")

    def _map_basic_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map basic features from input data"""
        return {new: float(data[orig]) for orig, new in self.required_columns.items()}

    def _is_peak_hour(self, hour: int) -> int:
        """Check if current hour is peak traffic time"""
        hour = int(hour) % 24
        return (
            1
            if hour in self.peak_morning_hours or hour in self.peak_evening_hours
            else 0
        )

    def _calculate_variance(self, data: Dict[str, Any]) -> float:
        """Calculate packet size variance"""
        packet_sizes = [
            data.get("src_bytes", 0),
            data.get("dst_bytes", 0),
            data.get("src_bytes", 0) / max(1, data.get("packet_count", 1)),
            data.get("dst_bytes", 0) / max(1, data.get("packet_count", 1)),
        ]
        return float(np.var(packet_sizes))

    def _calculate_bytes_ratio(self, data: Dict[str, Any]) -> float:
        """Calculate source to destination bytes ratio"""
        src = float(data.get("src_bytes", 0))
        dst = float(data.get("dst_bytes", 0))
        return src / max(1.0, dst)

    def _calculate_avg_packet_size(self, data: Dict[str, Any]) -> float:
        """Calculate average packet size"""
        total_bytes = float(data.get("src_bytes", 0) + data.get("dst_bytes", 0))
        packet_count = float(max(1, data.get("packet_count", 1)))
        return total_bytes / packet_count

    def _calculate_traffic_intensity(self, data: Dict[str, Any]) -> float:
        """Calculate traffic intensity (bytes per second)"""
        total_bytes = float(data.get("src_bytes", 0) + data.get("dst_bytes", 0))
        duration = float(max(0.1, data.get("duration", 0.1)))  # Avoid division by zero
        return total_bytes / duration


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    # One-hot encode protocol and service
    categorical = ["protocol", "service"]
    df = pd.get_dummies(df, columns=categorical, drop_first=True)
    # Validation: check for missing/invalid values
    if df.isnull().values.any():
        raise ValueError("Missing values found in features!")
    return df
