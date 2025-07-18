# 📖 MANUAL.md — Malicious URL Detection

This manual provides a user-friendly guide for running and understanding the **Malicious URL Detection System** built with machine learning.

---

## 🧭 Project Structure

```
Capstone-Malicous_URL_Detection/
├── data/                        # Dataset files (after extracting data.zip)
│   └── cleaned_data.csv
├── model/                       # Trained XGBoost model (.pkl)
├── visuals/                     # Output visualizations
│   ├── confusion_matrix.png
│   └── feature_importance.png
├── data_cleaning_and_features.py  # Data preprocessing script
├── train_model.py               # Model training script
├── inference.py                 # URL prediction script
├── README.md
└── MANUAL.md                    # This file
```

---

## ⚙️ Environment Setup

1. Clone the repo  
```bash
git clone https://github.com/Knox1983/Capstone-Malicous_URL_Detection.git
cd Capstone-Malicous_URL_Detection
```

2. (Optional) Create a virtual environment  
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install required libraries  
```bash
pip install -r requirements.txt
```

---

## 📂 Data Preparation

1. Download the dataset:
👉 [Download from Google Drive](https://drive.google.com/uc?export=download&id=1CEEghOidlx3ZKLbr0e76PEmyOjTtwWpl)

2. Unzip and place the contents into the `data/` folder.

3. Run the cleaning + feature engineering script:
```bash
python data_cleaning_and_features.py
```
Output: `data/cleaned_data.csv`

---

## 🎯 Model Training

Train the XGBoost model and generate visualizations:

```bash
python train_model.py
```

Outputs:
- Model: `model/xgboost_model.pkl`
- Visuals:
  - `visuals/confusion_matrix.png`
  - `visuals/feature_importance.png`

---

## 🔍 URL Inference

Edit `inference.py` to set your input path:
```python
input_path = "Data/new_urls.csv"  # or new_urls.txt
```

Then run:
```bash
python inference.py
```

Optional: Enhance with probabilities or filter malicious results.

---

## 💡 Troubleshooting

- **FileNotFoundError**: Check that paths like `data/cleaned_data.csv` or `model/xgboost_model.pkl` exist.
- **Large CSV not uploading to GitHub**: Use Google Drive and link in README.
- **`venv` folder should not be pushed**: Add it to `.gitignore`.

---

## 📌 Notes

- Do not commit large files like `.csv` or `.pkl` to GitHub — store externally.
- All outputs are saved locally and not pushed to the repo.

---

## 👤 Author

Louis Knox  
GitHub: [Knox1983](https://github.com/Knox1983)
