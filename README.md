Capstone_Malicious_URL_Detection/
├── Data/
│   ├── cleaned_data.csv             # Full cleaned dataset with features
│   ├── new_urls.csv / .txt          # Input URLs for prediction
│   ├── balanced_urls.csv            # Malicious URL's data
│   ├── malicious_phish.csv          # Malicious URL's data
│   ├── openphish_urls_sample.txt    # Malicious URL's data
│   ├── whitelist_top100.csv         # Trusted whitelist domains
│   ├── predicted_urls.csv           # Output: all URL predictions
│   └── malicious_only.csv           # Output: filtered malicious predictions
├── model/
│   └── xgboost_model.pkl            # Trained XGBoost model
├── logs/
│   ├── predictions_log.jsonl        # Logged prediction results
│   └── error_log.txt                # Error tracking
├── visuals/
│   ├── confusion_matrix.png         # Model performance visualization
│   └── feature_importance.png       # Top 10 feature importances
├── templates/
│   └── index.html                   # Web UI
├── static/
│   └── style.css                    # Optional styling
├── app.py                           # Flask app
├── utils.py                         # Feature extraction logic
├── train_model.py                   # Model training script
├── inference.py                     # URL prediction script (CSV or TXT)
├── data_cleaning_and_features.py   # Dataset cleaning + feature script
├── Malicious_URL_API_Demo.ipynb    # Notebook demo
├── README.md                        # Project documentation
├── API_DOCUMENTATION.md            # Project documentation
└── summary.md                       # Final project summary
└── Malicious_URL_Detection_Capstone_Presentation.pptx
