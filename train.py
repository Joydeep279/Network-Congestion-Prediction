import pandas as pd

from core.trainer import TrafficModelTrainer


def train_model():
    """Script to train the model."""
    print("🔄 Training model...")

    # Load and check data
    data_file = "assets/datasets/synthetic_network_data.csv"
    df = pd.read_csv(data_file)
    print(f"\nDataset shape: {df.shape}")
    print(f"Congestion distribution:\n{df['congestion'].value_counts()}")

    trainer = TrafficModelTrainer()
    metrics = trainer.train(data_file)

    print("\n✅ Model trained successfully!")
    print("\nModel Performance Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")


if __name__ == "__main__":
    train_model()
