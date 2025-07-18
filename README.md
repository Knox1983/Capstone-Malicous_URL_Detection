Capstone_Malicious_URL_Detection/
│
├── Data/
│ ├── cleaned_data.csv # Full cleaned dataset with features
│ ├── new_urls.csv / .txt # Input URLs for prediction
│ ├── balanced_urls.csv # Malicious URL's data 
│ ├── malicious_phish.csv # Malicious URL's data 
│ ├── openphish_urls_sample.txt # Malicious URL's data 
├── model/
│ └── xgboost_model.pkl # Trained XGBoost model
├── logs/
│   └── predictions_log.jsonl
│   └── error_log.txt
├── visuals/
│ ├── confusion_matrix.png # Model performance visualization
│ └── feature_importance.png # Top 10 feature importances
├── templates/
│   └── index.html  # Web UI
├── static/
│   └── style.css   # Optional styling
├── app.py
├── utils.py
├── train_model.py # Model training script
├── inference.py # URL prediction script (CSV or TXT)
├── data_cleaning_and_features.py # Dataset cleaning + feature script
├── Malicious_URL_API_Demo.ipynb
├── README.md # Project documentation
├── API_DOCUMENTATION.md # Project documentation
├── summary.md # Project documentation
