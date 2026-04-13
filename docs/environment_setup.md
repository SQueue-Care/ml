# ML Development Environment Setup

## 1. Introduction

This document provides a comprehensive guide for setting up a complete Python environment for Machine Learning model development in the SQueue-Care/ml project. The environment is designed to support the ML strategy and data schema defined in the accompanying documentation, ensuring compatibility with XGBoost-based regression models and time-series forecasting workflows.

---

## 2. Prerequisites

Before proceeding with the environment setup, ensure the following requirements are met:

*   **Python 3.10 or higher** — Required for compatibility with modern ML libraries
*   **pip** — Python package installer
*   **Git** — Version control system
*   **Virtual environment tool** — venv or conda

---

## 3. Virtual Environment Setup

### 3.1 Using venv

venv is the built-in Python virtual environment tool and is recommended for this project.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation
which python  # or where python on Windows
```

### 3.2 Using conda

If you prefer conda for environment management:

```bash
# Create conda environment
conda create -n ml-env python=3.10

# Activate environment
conda activate ml-env
```

---

## 4. Installing ML Libraries

### 4.1 Requirements Configuration

Create a `requirements.txt` file with the following dependencies:

```txt
# Core ML Libraries
scikit-learn==1.4.0
xgboost==2.0.2
pandas==2.1.4
numpy==1.26.3
tensorflow==2.15.0

# Data Processing
joblib==1.3.2
scipy==1.11.4

# Visualization
matplotlib==3.8.2
seaborn==0.13.1

# API Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3

# Jupyter
jupyter==1.0.0
notebook==7.0.6
ipykernel==6.29.0

# Development Tools
black==23.12.1
pylint==3.0.3
pytest==7.4.4
pytest-cov==4.1.0

# Model Versioning
mlflow==2.9.2
```

### 4.2 Installation

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. API Framework Setup

### 5.1 FastAPI Configuration

FastAPI is the recommended framework for building ML APIs due to its performance and async capabilities.

```bash
# Create a basic FastAPI app structure
mkdir -p api
touch api/__init__.py
touch api/main.py
```

### 5.2 Example API Implementation

Create `api/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SQueue ML API",
    description="Machine Learning API for SQueue-Care",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "SQueue ML API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 5.3 Running the API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 6. Jupyter Notebook Configuration

### 6.1 Kernel Setup

```bash
# Install IPython kernel
python -m ipykernel install --user --name=ml-env --display-name "Python (ml-env)"

# Start Jupyter
jupyter notebook
```

### 6.2 Jupyter Configuration

Create `.jupyter/jupyter_notebook_config.py`:

```python
c = get_config()

# Notebook settings
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888

# Security
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Display settings
c.DisplayShellHook.matplotlib = 'inline'
```

---

## 7. Model Storage and Versioning

### 7.1 MLflow Setup

MLflow is used for model tracking and versioning.

```bash
# Initialize MLflow tracking
mlflow ui --port 5000
```

### 7.2 Directory Structure

```
ml/
├── models/
│   ├── production/
│   ├── staging/
│   └── experiments/
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── notebooks/
├── api/
├── src/
│   ├── models/
│   ├── preprocessing/
│   └── utils/
└── tests/
```

### 7.3 Model Versioning Convention

```
models/
├── production/
│   └── queue_time_predictor_v1.0.0.pkl
├── staging/
│   └── queue_time_predictor_v1.1.0-rc1.pkl
└── experiments/
    └── queue_time_predictor_exp_20240413.pkl
```

---

## 8. Development Tools

### 8.1 Black (Code Formatter)

Configure Black in `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | \.eggs
  | build
  | dist
)/
'''
```

Format code:

```bash
black .
```

### 8.2 Pylint (Code Linter)

Configure Pylint in `.pylintrc`:

```ini
[MASTER]
extension-pkg-whitelist=numpy

[FORMAT]
max-line-length=120

[MESSAGES CONTROL]
disable=
    C0111,  # missing-docstring
    C0103,  # invalid-name
    R0903,  # too-few-public-methods
```

Run Pylint:

```bash
pylint src/
```

### 8.3 Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
```

Install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

---

## 9. Project Structure

### 9.1 Complete Directory Layout

```
ml/
├── .gitignore
├── .pre-commit-config.yaml
├── .pylintrc
├── pyproject.toml
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── data_schema.md
│   ├── ml_model_strategy.md
│   └── environment_setup.md
├── models/
│   ├── production/
│   ├── staging/
│   └── experiments/
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── health.py
│   └── models/
│       └── schemas.py
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── queue_time_predictor.py
│   │   └── base_model.py
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── feature_engineering.py
│   │   └── data_cleaning.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_preprocessing.py
│   └── test_api.py
└── scripts/
    ├── train_model.py
    ├── evaluate_model.py
    └── deploy_model.py
```

---

## 10. Environment Documentation

### 10.1 Environment Variables

Create `.env.example`:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENVIRONMENT=development

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/squeue_db

# MLflow Configuration
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=squeue-ml

# Model Configuration
MODEL_PATH=models/production
MODEL_VERSION=1.0.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 10.2 Quick Start Script

Create `scripts/setup.sh`:

```bash
#!/bin/bash

echo "Setting up ML Development Environment..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p models/{production,staging,experiments}
mkdir -p data/{raw,processed,features}
mkdir -p notebooks
mkdir -p api/routes
mkdir -p src/{models,preprocessing,utils}
mkdir -p tests
mkdir -p logs

# Install pre-commit hooks
pre-commit install

# Setup Jupyter kernel
python -m ipykernel install --user --name=ml-env --display-name "Python (ml-env)"

echo "Setup complete! Activate the environment with: source venv/bin/activate"
```

Make it executable:

```bash
chmod +x scripts/setup.sh
```

### 10.3 Verification Script

Create `scripts/verify_setup.sh`:

```bash
#!/bin/bash

echo "Verifying ML Development Environment..."

# Check Python version
python --version

# Check installed packages
pip list | grep -E "(scikit-learn|xgboost|pandas|numpy|tensorflow|fastapi|jupyter|black|pylint|mlflow)"

# Check directories
for dir in models data notebooks api src tests; do
    if [ -d "$dir" ]; then
        echo "✓ $dir directory exists"
    else
        echo "✗ $dir directory missing"
    fi
done

echo "Verification complete!"
```

---

## 11. Next Steps

1.  Activate your virtual environment
2.  Run the setup script: `bash scripts/setup.sh`
3.  Verify the installation: `bash scripts/verify_setup.sh`
4.  Start Jupyter Notebook: `jupyter notebook`
5.  Begin model development in the `notebooks/` directory

---

## 12. Troubleshooting

### 12.1 Common Issues

**Issue:** TensorFlow installation fails on macOS

```bash
# Solution: Install TensorFlow with Apple Silicon support
pip install tensorflow-macos
```

**Issue:** Jupyter kernel not found

```bash
# Solution: Reinstall the kernel
python -m ipykernel install --user --name=ml-env --display-name "Python (ml-env)"
```

**Issue:** MLflow UI not accessible

```bash
# Solution: Check firewall settings or use localhost
mlflow ui --port 5000 --host 127.0.0.1
```

---

## 13. Additional Resources

*   [FastAPI Documentation](https://fastapi.tiangolo.com/)
*   [Scikit-learn Documentation](https://scikit-learn.org/)
*   [MLflow Documentation](https://mlflow.org/)
*   [Black Documentation](https://black.readthedocs.io/)
*   [Pylint Documentation](https://pylint.org/)
