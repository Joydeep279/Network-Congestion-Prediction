from core.trainer import TrafficModelTrainer


def train_model():
    """Script to train the model."""
    print("🔄 Training model...")
    trainer = TrafficModelTrainer()
    trainer.train("assets/datasets/network_traffic.csv")
    print("✅ Model trained successfully!")


if __name__ == "__main__":
    train_model()
