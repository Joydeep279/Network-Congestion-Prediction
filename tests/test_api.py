import pytest

from web.app import app


def test_api_predict():
    client = app.test_client()
    # Test with a common TCP service
    payload_tcp = {
        "duration": 10,
        "src_bytes": 5000,
        "dst_bytes": 3000,
        "packet_count": 60,
        "hour": 8,
        "protocol": "TCP",
        "service": "http",
    }
    response_tcp = client.post("/api/predict", json=payload_tcp)
    assert response_tcp.status_code == 200
    data_tcp = response_tcp.get_json()
    assert "congestion" in data_tcp
    assert "probability" in data_tcp

    # Test with a common UDP service
    payload_udp = {
        "duration": 2,
        "src_bytes": 100,
        "dst_bytes": 100,
        "packet_count": 5,
        "hour": 14,
        "protocol": "UDP",
        "service": "dns",
    }
    response_udp = client.post("/api/predict", json=payload_udp)
    assert response_udp.status_code == 200
    data_udp = response_udp.get_json()
    assert "congestion" in data_udp
    assert "probability" in data_udp
