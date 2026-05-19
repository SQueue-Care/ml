from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load models dari model_artifacts directory
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model_artifacts')

scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.joblib'))
encoder = joblib.load(os.path.join(MODEL_DIR, 'encoder.joblib'))
model = load_model(os.path.join(MODEL_DIR, 'smart_queue_model.keras'))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'smart-queue-predictor'}), 200

@app.route('/predict/wait-time', methods=['GET'])
def predict_wait_time():
    """Endpoint yang match dengan backend expectations"""
    try:
        from datetime import datetime

        # Get query parameters
        department_id_param = request.args.get('departmentId')

        if not department_id_param:
            return jsonify({'error': 'Missing departmentId parameter'}), 400

        # Convert departmentId to integer hash for the model
        # Handle both UUID strings and integer IDs
        try:
            department_id = int(department_id_param)
        except ValueError:
            # If it's a UUID string, hash it to get a stable integer
            department_id = hash(department_id_param) % 5

        # Default values untuk numeric features
        now = datetime.now()
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        hour = now.hour
        waiting_ahead = int(request.args.get('waitingAhead', 5))
        avg_service_minutes = int(request.args.get('avgServiceMinutes', 15))
        is_peak = 1 if 9 <= hour <= 12 or 14 <= hour <= 16 else 0
        age = 30  # Default age

        # Numeric features scaling
        numeric_features = np.array([[
            age,
            waiting_ahead,
            hour,
            is_peak,
            10  # durasi_registrasi_menit default
        ]])

        numeric_features_scaled = scaler.transform(numeric_features)

        # Categorical features (dengan default encoding)
        cat_inputs = {
            'jenis_kelamin': np.array([0]),  # 0: MALE (default)
            'asuransi': np.array([0]),        # 0: BPJS (default)
            'status_pasien': np.array([0]),   # 0: BARU (default)
            'prioritas': np.array([0]),       # 0: NORMAL (default)
            'nama_poli': np.array([int(department_id % 5)]),  # Based on dept ID
            'hari': np.array([day_of_week]),
            'numeric_inputs': numeric_features_scaled
        }

        prediction = model.predict(cat_inputs, verbose=0)
        estimated_minutes = max(0, int(prediction[0][0]))

        return jsonify({
            'estimatedMinutes': estimated_minutes,
            'modelVersion': '1.0',
            'source': 'ml-service',
            'waitingAhead': waiting_ahead,
            'avgServiceMinutes': avg_service_minutes
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'message': 'Prediction failed'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Alternative POST endpoint untuk flexibility"""
    try:
        data = request.get_json()
        required_fields = ['departmentId', 'dayOfWeek', 'hour', 'waitingAhead', 'avgServiceMinutes']

        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields', 'required': required_fields}), 400

        features = np.array([[
            data['departmentId'],
            data['dayOfWeek'],
            data['hour'],
            data['waitingAhead'],
            data['avgServiceMinutes']
        ]])

        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled, verbose=0)
        estimated_wait_minutes = max(0, int(prediction[0][0]))

        return jsonify({
            'estimatedWaitMinutes': estimated_wait_minutes,
            'modelVersion': '1.0',
            'source': 'ml-service',
            'features': {
                'departmentId': int(data['departmentId']),
                'dayOfWeek': int(data['dayOfWeek']),
                'hour': int(data['hour']),
                'waitingAhead': int(data['waitingAhead']),
                'avgServiceMinutes': int(data['avgServiceMinutes'])
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Prediction failed'}), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'error': 'Expected list of prediction requests'}), 400

        results = []
        for item in data:
            try:
                features = np.array([[
                    item['departmentId'],
                    item['dayOfWeek'],
                    item['hour'],
                    item['waitingAhead'],
                    item['avgServiceMinutes']
                ]])
                features_scaled = scaler.transform(features)
                prediction = model.predict(features_scaled, verbose=0)
                estimated_wait_minutes = max(0, int(prediction[0][0]))
                results.append({'estimatedWaitMinutes': estimated_wait_minutes})
            except Exception as e:
                results.append({'error': str(e)})

        return jsonify({'predictions': results}), 200

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Batch prediction failed'}), 500

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'service': 'SQueue Care - Wait Time Predictor',
        'version': '1.0',
        'endpoints': {
            'health': 'GET /health',
            'predict': 'POST /predict',
            'batch_predict': 'POST /batch-predict',
            'info': 'GET /info'
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
