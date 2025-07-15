import numpy as np
import pandas as pd


def generate_synthetic_traffic(n=50000):
    peak_hours = [7, 8, 9, 17, 18, 19]  # morning & evening peak
    data = []

    for _ in range(n):
        hour = np.random.randint(0, 24)
        is_peak = hour in peak_hours

        duration = np.random.exponential(scale=8 if is_peak else 4)
        src_bytes = int(np.random.normal(loc=5000 if is_peak else 1000, scale=800))
        dst_bytes = int(np.random.normal(loc=3000 if is_peak else 700, scale=500))
        packet_count = np.random.poisson(lam=60 if is_peak else 20)

        congestion = 1 if (is_peak and packet_count > 50) else 0

        data.append(
            [
                duration,
                max(0, src_bytes),
                max(0, dst_bytes),
                packet_count,
                hour,
                congestion,
            ]
        )

    df = pd.DataFrame(
        data,
        columns=pd.Index(
            ["duration", "src_bytes", "dst_bytes", "packet_count", "hour", "congestion"]
        ),
    )
    return df


# Generate and save to CSV
df = generate_synthetic_traffic()
df.to_csv("synthetic_network_data.csv", index=False)
print("✅ Dataset created and saved as 'synthetic_network_data.csv'")
print(df.head())

# Run this in Python:
from core.trainer import TrafficModelTrainer

trainer = TrafficModelTrainer()
trainer.train("assets/datasets/synthetic_network_data.csv")
