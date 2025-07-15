# Network Traffic Congestion Predictor 🚦

A machine learning application to predict network traffic congestion in real-time. Built with Python, Scikit-learn, and Flask, it features a complete ML pipeline from data generation to prediction via a REST API and an interactive web dashboard.

![Dashboard Screenshot](https://i.imgur.com/your-screenshot.png) <!-- Placeholder: Replace with a real screenshot of your dashboard -->

## ✨ Features

- **End-to-End ML Pipeline**: Unified preprocessing (scaling, one-hot encoding) and modeling using a robust `sklearn.Pipeline`.
- **Config-Driven Training**: Model hyperparameters and pipeline settings are managed centrally via `core/config.yaml`.
- **Hyperparameter Tuning**: Integrated `GridSearchCV` for automated model optimization.
- **Realistic Synthetic Data**: A CLI script (`generate_data.py`) that creates plausible network traffic data, linking services to their common protocols.
- **REST API**: A robust Flask API for serving predictions (`/api/predict`).
- **Interactive Dashboard**: A web UI built with Bootstrap and Chart.js to make live predictions and visualize results.

## 📂 Project Structure

```
├── assets/
│   ├── datasets/       # Stores the generated network_traffic.csv
│   └── models/         # Stores the trained model pipeline (gb_model.pkl)
├── core/
│   ├── config.yaml     # Model & pipeline configuration
│   ├── predictor.py    # Loads the full pipeline and serves predictions
│   └── trainer.py      # The ML training pipeline logic
├── tests/                # Unit and integration tests
├── web/
│   ├── app.py          # Flask application (API and UI routes)
│   ├── static/         # CSS and JS files
│   └── templates/      # HTML templates
├── generate_data.py      # CLI script for generating synthetic data
├── train.py              # Script to execute model training
└── requirements.txt
```

## 🚀 Local Development Setup

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
- Python 3.9+

### 2. Setup Virtual Environment
Create and activate a virtual environment.
```bash
# Create the virtual environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Or on Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required packages.
```bash
pip install -r requirements.txt
```

### 4. Generate Data
Run the data generation script. This will create `assets/datasets/network_traffic.csv`.
```bash
python generate_data.py
```

### 5. Train the Model
Run the training script. This reads the configuration from `core/config.yaml`, trains the model, and saves the entire pipeline to `assets/models/gb_model.pkl`.
```bash
python train.py
```

### 6. Run the Web App
Start the Flask server.
```bash
# Set Flask environment variables (macOS/Linux)
export FLASK_APP=web/app.py
export FLASK_ENV=development

# Or on Windows
set FLASK_APP=web/app.py
set FLASK_ENV=development

# Run the app
flask run
```

## Usage

### Web Dashboard
Once the app is running, navigate to `http://127.0.0.1:5000/dashboard` in your web browser to use the interactive prediction form.

### API Endpoint
You can also make predictions by sending a POST request to the `/api/predict` endpoint.

**Example using `curl`:**
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{
          "duration": 10.5,
          "src_bytes": 5120,
          "dst_bytes": 2400,
          "packet_count": 65,
          "hour": 9,
          "protocol": "TCP",
          "service": "http"
     }'
```
**Expected Response:**
```json
{
  "congestion": true,
  "probability": 0.87
}
```

## ⚙️ Configuration
The core training logic is configured via `core/config.yaml`. Here you can adjust:
- Model hyperparameters (`model_params`)
- Feature selection parameters (`feature_selection_k`)
- The grid for hyperparameter search (`grid_search_params`)

## ✅ Testing
Run the full suite of unit and integration tests using `pytest`.
```bash
pytest
``` 