import pandas as pd

from core.feature_engineer import engineer_features


def test_engineer_features():
    df = pd.DataFrame(
        {
            "duration": [1, 2],
            "src_bytes": [100, 200],
            "dst_bytes": [50, 60],
            "packet_count": [10, 20],
            "service_count": [1, 2],
            "hour": [8, 15],
            "protocol": ["TCP", "UDP"],
            "service": ["http", "dns"],
        }
    )
    out = engineer_features(df)
    assert "protocol_UDP" in out.columns
    assert "service_dns" in out.columns
    assert not out.isnull().values.any()
