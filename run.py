import numpy as np
import pandas as pd

from core.trainer import TrafficModelTrainer


def generate_synthetic_traffic(n=50000):
    peak_hours = [7, 8, 9, 17, 18, 19]
    protocols = ["TCP", "UDP", "ICMP"]
    services = ["http", "ftp", "ssh", "dns", "smtp", "other"]
    data = []

    for _ in range(n):
        hour = np.random.randint(0, 24)
        is_peak = hour in peak_hours
        protocol = np.random.choice(protocols, p=[0.7, 0.2, 0.1])
        service = np.random.choice(services, p=[0.5, 0.1, 0.1, 0.1, 0.1, 0.1])

        duration = np.random.exponential(scale=8 if is_peak else 4)
        src_bytes = int(np.random.normal(loc=5000 if is_peak else 1000, scale=800))
        dst_bytes = int(np.random.normal(loc=3000 if is_peak else 700, scale=500))
        packet_count = np.random.poisson(lam=60 if is_peak else 20)
        service_count = np.random.poisson(lam=3)

        congestion = 1 if (is_peak and packet_count > 50) else 0

        data.append(
            [
                duration,
                max(0, src_bytes),
                max(0, dst_bytes),
                packet_count,
                service_count,
                hour,
                protocol,
                service,
                congestion,
            ]
        )

    df = pd.DataFrame(
        data,
        columns=pd.Index(
            [
                "duration",
                "src_bytes",
                "dst_bytes",
                "packet_count",
                "service_count",
                "hour",
                "protocol",
                "service",
                "congestion",
            ]
        ),
    )
    return df


if __name__ == "__main__":
    print("🔄 Generating data...")
    df = generate_synthetic_traffic()
    df.to_csv("synthetic_network_data.csv", index=False)
    print("✅ Dataset created!")

    print("🔄 Training model...")
    trainer = TrafficModelTrainer()
    trainer.train("synthetic_network_data.csv")
    print("✅ Model trained!")
    print("\n🚀 Now run these commands to start the web app:")
    print("export FLASK_APP=web/app.py")
    print("export FLASK_ENV=development")
    print("flask run")
