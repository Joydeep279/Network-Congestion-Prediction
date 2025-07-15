import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_synthetic_traffic(n=50000, seed=42):
    """Generate synthetic network traffic data with realistic patterns."""
    np.random.seed(seed)

    peak_hours = [7, 8, 9, 17, 18, 19]
    protocols = ["TCP", "UDP", "ICMP"]

    # Services are often tied to specific protocols
    service_protocol_map = {
        "http": "TCP",
        "ftp": "TCP",
        "ssh": "TCP",
        "smtp": "TCP",
        "dns": "UDP",
        "ntp": "UDP",
        "other": "UDP",
    }
    services = list(service_protocol_map.keys())

    data = []

    for _ in range(n):
        hour = np.random.randint(0, 24)
        is_peak = hour in peak_hours

        # Select service and determine its protocol
        service = np.random.choice(services, p=[0.4, 0.05, 0.05, 0.1, 0.2, 0.1, 0.1])
        protocol = service_protocol_map[service]

        # Add a small chance of ICMP traffic, which has no service
        if np.random.random() < 0.05:
            protocol = "ICMP"
            service = "none"

        duration = np.random.exponential(scale=8 if is_peak else 4)
        src_bytes = int(np.random.normal(loc=5000 if is_peak else 1000, scale=800))
        dst_bytes = int(np.random.normal(loc=3000 if is_peak else 700, scale=500))
        packet_count = np.random.poisson(lam=60 if is_peak else 20)

        # More sophisticated congestion determination
        load_factor = (packet_count / 100) * (duration / 10)
        congestion = 1 if (load_factor > 1.0 or (is_peak and packet_count > 80)) else 0

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
    parser = argparse.ArgumentParser(
        description="Generate synthetic network traffic data."
    )
    parser.add_argument(
        "--n", type=int, default=100000, help="Number of samples to generate."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="assets/datasets/network_traffic.csv",
        help="Output file path.",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility."
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🔄 Generating {args.n} samples of synthetic data...")
    df = generate_synthetic_traffic(n=args.n, seed=args.seed)
    df.to_csv(output_path, index=False)

    print(f"✅ Dataset created and saved to '{output_path}'")
    print("\nSample data:")
    print(df.head())
    print(
        f"\nCongestion distribution:\n{df['congestion'].value_counts(normalize=True).round(3)}"
    )
    print(
        f"\nProtocol distribution:\n{df['protocol'].value_counts(normalize=True).round(3)}"
    )
