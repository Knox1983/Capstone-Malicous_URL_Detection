from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from utils import preprocess_url
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load model
model = joblib.load('model/xgboost_model.pkl')
model_info = {
    "model_type": "XGBoost",
    "features": ['url_length', 'num_digits', 'num_special_chars', 'has_ip', 'keyword_flag']
}

# Ensure logs folder exists
os.makedirs('logs', exist_ok=True)

# Health check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK", "message": "API is running"}), 200

# Model info
@app.route('/model_info', methods=['GET'])
def model_details():
    return jsonify(model_info), 200

# Single prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'url' not in data:
            return jsonify({'error': 'Missing "url" in request'}), 400

        url = data['url']
        features_df = preprocess_url(url)
        prediction = int(model.predict(features_df)[0])
        proba = float(model.predict_proba(features_df)[0][1])

        log_entry = {
            'timestamp': str(datetime.utcnow()),
            'url': url,
            'prediction': prediction,
            'probability': proba
        }
        with open('logs/predictions_log.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        return jsonify({'prediction': prediction, 'probability': round(proba, 4)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Batch predictions
@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    try:
        data = request.get_json()
        urls = data.get("urls", [])

        if not isinstance(urls, list) or not urls:
            return jsonify({"error": "Provide a list of URLs under the 'urls' key"}), 400

        results = []
        for url in urls:
            features_df = preprocess_url(url)
            prediction = int(model.predict(features_df)[0])
            proba = float(model.predict_proba(features_df)[0][1])
            results.append({
                'url': url,
                'prediction': prediction,
                'probability': round(proba, 4)
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
