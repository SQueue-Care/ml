# Smart Queue ML Service

Predict queue wait times menggunakan Deep Learning Neural Network untuk sistem manajemen antrian rumah sakit.

## Overview

ML Service ini menyediakan endpoint prediksi waktu tunggu berbasis machine learning untuk pasien di rumah sakit. Model menggunakan kombinasi:
- **Numerical Features**: umur, jumlah antrian, jam kedatangan, peak hour indicator, durasi registrasi
- **Categorical Features**: jenis kelamin, asuransi, status pasien, prioritas, poli, hari

## Arsitektur Model

```
Input Features
    ↓
[Embedding Layers] → Categorical encoding
[Scaler] → Numerical normalization
    ↓
Concatenate
    ↓
Dense(128) + BatchNorm + Dropout(0.2)
Dense(64) + BatchNorm + Dropout(0.1)
Dense(32)
    ↓
Dense(1, linear) → Output (wait minutes)
```

---

## Quick Start

### Prerequisites

- **Python**: 3.11 atau lebih tinggi
- **pip**: Package manager
- **virtualenv** (recommended): `pip install virtualenv`

### Check Python Version
```bash
python --version
# atau
python3 --version
```

### Installation Steps
```bash
# 1. Navigate ke ml directory
cd ml/

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# atau
venv\Scripts\activate  # Windows

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -c "import tensorflow; print(f'TensorFlow: {tensorflow.__version__}')"
```

### Verify Installation

```bash
# 1. Check Python
python --version

# 2. Check TensorFlow
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"

# 3. Check model files
ls model_artifacts/
# Should show:
# - smart_queue_model.keras
# - scaler.joblib
# - encoder.joblib
```

---

## Running the Service

### Development Mode (with debug)
```bash
cd ml/
python app.py
```
Service berjalan di: `http://localhost:8000` (atau :5000 sesuai config)

### Test Service
```bash
curl http://localhost:8000/health

# Expected:
# {"status":"healthy","service":"smart-queue-predictor"}
```

---

## API Endpoints

### 1. Health Check
**GET** `/health`

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "smart-queue-predictor"
}
```

---

### 2. Predict Wait Time (Backend Compatible)

**GET** `/predict/wait-time?departmentId=1&waitingAhead=5&avgServiceMinutes=15`

**Query Parameters:**
- `departmentId` (required, int): Department/Poli ID
- `waitingAhead` (optional, int): Jumlah pasien di depan (default: 5)
- `avgServiceMinutes` (optional, int): Waktu layanan rata-rata (default: 15)

```bash
curl "http://localhost:8000/predict/wait-time?departmentId=1"
```

Response:
```json
{
  "estimatedMinutes": 19,
  "modelVersion": "1.0",
  "source": "ml-service",
  "waitingAhead": 5,
  "avgServiceMinutes": 15
}
```

---

### 3. Single Prediction (POST)

**POST** `/predict`

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "departmentId": 1,
    "dayOfWeek": 3,
    "hour": 10,
    "waitingAhead": 5,
    "avgServiceMinutes": 15
  }'
```

Response:
```json
{
  "estimatedWaitMinutes": 19,
  "modelVersion": "1.0",
  "source": "ml-service",
  "features": {...}
}
```

---

### 4. Batch Prediction

**POST** `/batch-predict`

```bash
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[
    {"departmentId": 1, "dayOfWeek": 3, "hour": 10, "waitingAhead": 5, "avgServiceMinutes": 15},
    {"departmentId": 2, "dayOfWeek": 3, "hour": 14, "waitingAhead": 8, "avgServiceMinutes": 20}
  ]'
```

Response:
```json
{
  "predictions": [
    {"estimatedWaitMinutes": 19},
    {"estimatedWaitMinutes": 25}
  ]
}
```

---

### 5. Service Info

**GET** `/info`

```bash
curl http://localhost:8000/info
```

---

## Model Details

### Arsitektur
- **Input**: 7 inputs (6 categorical + 1 numeric vector)
- **Embeddings**: Categorical features → dense vectors
- **Hidden Layers**: 
  - Dense(128) + BatchNorm + Dropout(0.2)
  - Dense(64) + BatchNorm + Dropout(0.1)
  - Dense(32)
- **Output**: Dense(1, linear)

### Training Specs
- **Optimizer**: Adam (learning_rate=0.005)
- **Loss**: Mean Squared Error (MSE)
- **Metrics**: Mean Absolute Error (MAE)
- **Callbacks**:
  - EarlyStopping (patience=15)
  - ReduceLROnPlateau (factor=0.5, patience=5)
- **Data Split**: 80% train, 10% val, 10% test
- **Total Records**: 10,032
- **Test MAE**: ~2-3 minutes accuracy

### Model Files
```
model_artifacts/
├── smart_queue_model.keras    # Neural Network (259 KB)
├── scaler.joblib              # StandardScaler untuk numeric features
├── encoder.joblib             # OrdinalEncoder untuk categorical
└── metadata.joblib            # Feature metadata
```

---

## Input/Output Format

### Input Features

| Feature | Type | Description |
|---------|------|-------------|
| departmentId | int | Department/Poli ID |
| umur | int | Patient age |
| jenis_kelamin | categorical | Gender (MALE/FEMALE) |
| asuransi | categorical | Insurance type |
| status_pasien | categorical | Patient status (BARU/LAMA) |
| prioritas | categorical | Priority level |
| nama_poli | categorical | Department name |
| hari | int | Day of week (0=Mon, 6=Sun) |
| jam_kedatangan | int | Hour (0-23) |
| is_peak | int | Peak hour (9-12, 14-16) |
| jumlah_antrian | int | Waiting queue count |
| durasi_registrasi | float | Registration duration (minutes) |

### Output

| Field | Type | Description |
|-------|------|-------------|
| estimatedMinutes | int | Predicted wait time (minutes) |
| modelVersion | string | Model version |
| source | string | "ml-service" |
| waitingAhead | int | Queue depth used |
| avgServiceMinutes | int | Average service time |

---

## Integration

### Backend Setup

Configure di backend `.env`:
```env
ML_SERVICE_URL=http://localhost:8000
```

Backend akan otomatis memanggil ML service saat:
- Queue creation (POST /queues)
- Predictions endpoint (GET /predictions/wait-time)

### Fallback Mechanism

Jika ML service tidak tersedia, backend pakai heuristik:
```
waitTime = waitingAhead × avgServiceMinutes + inProgressBuffer
```

---

## Configuration

### Environment Variables
```env
FLASK_ENV=production
ML_DEBUG=0
TF_CPP_MIN_LOG_LEVEL=2
```

### Performance Tuning

**High Traffic:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 8 --timeout 120 app:app
```

**With Resource Limits:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --max-requests 1000 app:app
```
---

## Testing

### Using cURL
```bash
# Health
curl http://localhost:8000/health

# Prediction
curl "http://localhost:8000/predict/wait-time?departmentId=1"

# Batch
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '[{"departmentId":1,"dayOfWeek":3,"hour":10,"waitingAhead":5,"avgServiceMinutes":15}]'
```

### Using Python
```python
import requests

response = requests.get(
  "http://localhost:8000/predict/wait-time",
  params={"departmentId": 1, "waitingAhead": 5}
)
print(response.json())
```
---
