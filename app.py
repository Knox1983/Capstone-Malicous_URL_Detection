from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime, timezone
import joblib
from utils import preprocess_url
import json
import os

# Initialize Flask app
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

# Health Check Route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK", "message": "API is running"}), 200

# Model Info Route
@app.route('/model_info', methods=['GET'])
def model_details():
    return jsonify(model_info), 200

# Single Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if 'url' not in data:
            return jsonify({'error': 'Missing "url" in request'}), 400

        url = data['url']
        if not url or not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400

        features_df = preprocess_url(url)
        print("Extracted features:", features_df.to_dict(orient='records')[0])
        prediction = int(model.predict(features_df)[0])
        proba = float(model.predict_proba(features_df)[0][1])

        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'url': url,
            'features': features_df.to_dict(orient='records')[0],
            'prediction': prediction,
            'probability': proba
        }
        with open('logs/predictions_log.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        return jsonify({'prediction': prediction, 'probability': round(proba, 4)}), 200

    except Exception as e:
        with open('logs/error_log.txt', 'a') as err_log:
            err_log.write(f"{datetime.utcnow()} - {str(e)}\n")
        return jsonify({'error': str(e)}), 500

# Batch Prediction Route
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
            print("Extracted features:", features_df.to_dict(orient='records')[0])
            prediction = int(model.predict(features_df)[0])
            proba = float(model.predict_proba(features_df)[0][1])
            results.append({
                'url': url,
                'features': features_df.to_dict(orient='records')[0],
                'prediction': prediction,
                'probability': round(proba, 4)
            })

        return jsonify(results), 200

    except Exception as e:
        with open('logs/error_log.txt', 'a') as err_log:
            err_log.write(f"{datetime.utcnow()} - {str(e)}\n")
        return jsonify({'error': str(e)}), 500

# UI interface
@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        urls_text = request.form['urls']
        url_list = [u.strip() for u in urls_text.strip().splitlines() if u.strip()]
        for url in url_list:
            try:
                features_df = preprocess_url(url)
                prediction = int(model.predict(features_df)[0])
                proba = float(model.predict_proba(features_df)[0][1])
                results.append({
                    'url': url,
                    'prediction': prediction,
                    'probability': round(proba, 4)
                })
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
    return render_template('index.html', results=results)


# Run the App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
