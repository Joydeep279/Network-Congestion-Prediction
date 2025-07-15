from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_traffic(n=50000):
    peak_hours = [7, 8, 9, 17, 18, 19]  # morning & evening peak

    # Define protocols and services with their probabilities
    protocols = ["TCP", "UDP", "ICMP"]
    protocol_probs = [0.8, 0.15, 0.05]  # TCP is most common

    services = ["http", "ftp", "ssh", "dns", "smtp", "ntp", "other"]
    service_probs = [0.4, 0.1, 0.1, 0.15, 0.1, 0.05, 0.1]  # http is most common

    data = []

    for _ in range(n):
        hour = np.random.randint(0, 24)
        is_peak = hour in peak_hours

        duration = np.random.exponential(scale=8 if is_peak else 4)
        src_bytes = int(np.random.normal(loc=5000 if is_peak else 1000, scale=800))
        dst_bytes = int(np.random.normal(loc=3000 if is_peak else 700, scale=500))
        packet_count = np.random.poisson(lam=60 if is_peak else 20)

        # Generate protocol and service
        protocol = np.random.choice(protocols, p=protocol_probs)
        service = np.random.choice(services, p=service_probs)

        # ICMP doesn't use services
        if protocol == "ICMP":
            service = "none"

        congestion = 1 if (is_peak and packet_count > 50) else 0

        data.append(
            [
                duration,
                max(0, src_bytes),
                max(0, dst_bytes),
                packet_count,
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
                "hour",
                "protocol",
                "service",
                "congestion",
            ]
        ),
    )
    return df


if __name__ == "__main__":
    # Generate and save to CSV
    df = generate_synthetic_traffic()

    # Ensure the datasets directory exists
    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "synthetic_network_data.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Dataset created and saved as '{output_path}'")
    print("\nSample of generated data:")
    print(df.head())

    print("\nData Statistics:")
    print(f"Total records: {len(df)}")
    print("\nProtocol distribution:")
    print(df["protocol"].value_counts(normalize=True))
    print("\nService distribution:")
    print(df["service"].value_counts(normalize=True))
