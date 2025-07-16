from unittest.mock import MagicMock, patch

import pytest

from core.predictor import TrafficPredictor


class TestTrafficPredictor:
    @pytest.fixture
    def predictor(self):
        with patch("core.predictor.joblib.load") as mock_load:
            # Create a mock pipeline
            mock_pipeline = MagicMock()
            mock_load.return_value = mock_pipeline
            return TrafficPredictor()

    def test_predict(self, predictor):
        # Mock the pipeline's predict and predict_proba methods
        predictor.pipeline.predict.return_value = [1]
        predictor.pipeline.predict_proba.return_value = [[0.2, 0.8]]

        input_data = {
            "duration": 10.5,
            "src_bytes": 1024,
            "dst_bytes": 2048,
            "packet_count": 5,
            "hour": 9,
            "protocol": "TCP",
            "service": "http",
        }

        result = predictor.predict(input_data)

        assert result["congestion"] is True
        assert result["probability"] == 0.8  # Using exact match since we're mocking

        # Verify the pipeline was called with correct feature order
        predictor.pipeline.predict.assert_called_once()
        predictor.pipeline.predict_proba.assert_called_once()
