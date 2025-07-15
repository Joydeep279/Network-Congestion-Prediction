import pytest
from unittest.mock import patch, MagicMock
from core.predictor import TrafficPredictor
from core.feature_engineer import FeatureEngineer

class TestTrafficPredictor:
    @pytest.fixture
    def predictor(self):
        with patch('core.predictor.joblib.load'):
            return TrafficPredictor()
    
    def test_predict(self, predictor):
        predictor.model.predict.return_value = [1]
        predictor.model.predict_proba.return_value = [[0.2, 0.8]]
        
        with patch.object(FeatureEngineer, 'transform', return_value={
            'conn_duration': 10.5,
            'src_bytes': 1024,
            'dst_bytes': 2048,
            'packet_count': 5,
            'service_count': 3,
            'peak_hour_flag': 1,
            'packet_size_variance': 25.0,
            'bytes_ratio': 0.5
        }):
            result = predictor.predict({
                'duration': 10.5,
                'src_bytes': 1024,
                'dst_bytes': 2048,
                'packet_count': 5,
                'service_count': 3,
                'hour': 9
            })
            
            assert result['congestion'] is True
            assert 0.79 < result['probability'] <= 0.81