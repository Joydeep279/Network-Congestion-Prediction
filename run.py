import argparse
import os
import subprocess
import sys

from loguru import logger


def run_data_generation():
    """Runs the data generation script."""
    logger.info("▶️ Starting data generation...")
    try:
        subprocess.run([sys.executable, "generate_data.py"], check=True)
        logger.success("✅ Data generation complete.")
    except FileNotFoundError:
        logger.error(
            "Could not find generate_data.py. Make sure you are in the project root."
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logger.error(f"Data generation failed with exit code {e.returncode}.")
        sys.exit(1)


def run_training():
    """Runs the model training script."""
    logger.info("▶️ Starting model training...")
    try:
        subprocess.run([sys.executable, "train.py"], check=True)
        logger.success("✅ Model training complete.")
    except FileNotFoundError:
        logger.error("Could not find train.py. Make sure you are in the project root.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        logger.error(f"Model training failed with exit code {e.returncode}.")
        sys.exit(1)


def run_web_app():
    """Runs the Flask web application."""
    logger.info("▶️ Starting Flask web server...")
    logger.info("Visit http://127.0.0.1:5000/dashboard in your browser.")
    logger.info("Press CTRL+C to stop the server.")
    try:
        env = os.environ.copy()
        env["FLASK_APP"] = "web/app.py"
        env["FLASK_ENV"] = "development"
        subprocess.run(
            [sys.executable, "-m", "flask", "run"],
            check=True,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start web app with exit code {e.returncode}.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Web server stopped.")


def main():
    """Main execution function with command-line parsing."""
    parser = argparse.ArgumentParser(
        description="Run pipeline for the Traffic Congestion App.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "step",
        nargs="?",
        default="all",
        choices=["data", "train", "web", "all"],
        help=(
            "Choose which part of the pipeline to run:\n"
            "  data  - Generate synthetic data\n"
            "  train - Train the prediction model\n"
            "  web   - Run the Flask web application\n"
            "  all   - (Default) Run all steps in order: data -> train -> web"
        ),
    )
    args = parser.parse_args()

    if args.step == "all":
        run_data_generation()
        run_training()
        run_web_app()
    elif args.step == "data":
        run_data_generation()
    elif args.step == "train":
        run_training()
    elif args.step == "web":
        run_web_app()


if __name__ == "__main__":
    main()
