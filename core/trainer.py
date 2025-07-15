import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
import yaml
from dotenv import load_dotenv
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


class TrafficModelTrainer:
    """Handles training and saving of the congestion prediction model"""

    def __init__(self, config_path: str = ""):
        if not config_path:
            config_path = os.getenv(
                "MODEL_CONFIG", str(PROJECT_ROOT / "core" / "config.yaml")
            )
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.config = config
        self.model_path = config.get(
            "model_path",
            os.getenv(
                "MODEL_PATH", str(PROJECT_ROOT / "assets" / "models" / "gb_model.pkl")
            ),
        )
        self.pipeline = None

    def load_data(self, data_path: str) -> pd.DataFrame:
        """Load training data"""
        try:
            full_data_path = PROJECT_ROOT / data_path
            df = pd.read_csv(full_data_path)
            return df
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

    def train(self, data_path: str) -> Dict[str, Any]:
        try:
            df = self.load_data(data_path)

            X = df.drop("congestion", axis=1)
            y = df["congestion"]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Identify categorical and numerical features
            categorical_features = ["protocol", "service"]
            numerical_features = X.select_dtypes(include=np.number).columns.tolist()

            # Create the preprocessing pipelines for both numeric and categorical data
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numerical_features),
                    (
                        "cat",
                        OneHotEncoder(handle_unknown="ignore"),
                        categorical_features,
                    ),
                ]
            )

            # Create the full pipeline
            self.pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    (
                        "selector",
                        SelectKBest(
                            f_classif, k=self.config.get("feature_selection_k", "all")
                        ),
                    ),
                    (
                        "model",
                        GradientBoostingClassifier(**self.config["model_params"]),
                    ),
                ]
            )

            # Hyperparameter tuning
            if self.config.get("grid_search_params"):
                grid = GridSearchCV(
                    self.pipeline,
                    self.config["grid_search_params"],
                    cv=3,  # Reduced CV for speed
                    scoring="roc_auc",
                    n_jobs=-1,
                )
                grid.fit(X_train, y_train)
                self.pipeline = grid.best_estimator_
                logger.info(f"Best params: {grid.best_params_}")
            else:
                self.pipeline.fit(X_train, y_train)

            y_pred = self.pipeline.predict(X_test)
            y_prob = self.pipeline.predict_proba(X_test)[:, 1]

            metrics = {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "precision": float(precision_score(y_test, y_pred)),
                "recall": float(recall_score(y_test, y_pred)),
                "f1": float(f1_score(y_test, y_pred)),
                "roc_auc": float(roc_auc_score(y_test, y_prob)),
            }

            logger.success("Model training completed successfully")
            for metric, value in metrics.items():
                logger.info(f"{metric}: {value:.3f}")

            self._save_pipeline()
            return metrics

        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise

    def _save_pipeline(self) -> None:
        """Save the entire pipeline to disk"""
        try:
            model_dir = Path(self.model_path).parent
            model_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(self.pipeline, self.model_path)
            logger.info(f"Pipeline saved to {self.model_path}")

        except Exception as e:
            logger.error(f"Failed to save pipeline: {e}")
            raise
