import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier
from utils import preprocess_url
from urllib.parse import urlparse

# Paths
raw_data_path = "C:/Users/red_l/PycharmProjects/MaliciousURL/Data/cleaned_data.csv"
whitelist_path = "C:/Users/red_l/PycharmProjects/MaliciousURL/Data/whitelist_top100.csv"
model_dir = "C:/Users/red_l/PycharmProjects/MaliciousURL/model"
visual_dir = "C:/Users/red_l/PycharmProjects/MaliciousURL/visuals"
os.makedirs(model_dir, exist_ok=True)
os.makedirs(visual_dir, exist_ok=True)

# Load data
df = pd.read_csv(raw_data_path)
df = df.dropna(subset=['url'])
df = df[df['url'].apply(lambda x: isinstance(x, str))]

# Load whitelist
df_whitelist = pd.read_csv(whitelist_path)
whitelist = set(df_whitelist['domain'].str.lower().str.lstrip("www."))

# Feature extraction and label handling
features = []
labels = []
for url, label in zip(df['url'], df['label']):
    try:
        url = str(url)
        row = preprocess_url(url).iloc[0]

        hostname = urlparse(url).hostname or ""
        hostname = hostname.lower().lstrip("www.")
        if hostname in whitelist:
            label = 0  # Force benign label for trusted domains

        features.append(row)
        labels.append(label)
    except Exception as e:
        print(f"⚠️ Skipped: {url} → {e}")

X = pd.DataFrame(features)
y = pd.Series(labels)

# Class balance
malicious = sum(y == 1)
benign = sum(y == 0)
scale_weight = benign / malicious
print(f"Class balance → Benign: {benign}, Malicious: {malicious}")
print(f"Using scale_pos_weight = {scale_weight:.2f}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train XGBoost model
print("🧠 Training XGBoost model...")
model = XGBClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_weight,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
print("📊 Evaluation Results:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}")

# Save model
joblib.dump(model, os.path.join(model_dir, "xgboost_model.pkl"))
print("✅ Model saved to model/xgboost_model.pkl")

# Save visuals
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benign", "Malicious"], yticklabels=["Benign", "Malicious"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(os.path.join(visual_dir, "confusion_matrix.png"))

xgb_importance = model.get_booster().get_score(importance_type='weight')
importance_df = pd.DataFrame(xgb_importance.items(), columns=['feature', 'importance']).sort_values(by='importance', ascending=False)
plt.figure(figsize=(8, 5))
sns.barplot(x='importance', y='feature', data=importance_df.head(10))
plt.title("Top 10 Feature Importances")
plt.tight_layout()
plt.savefig(os.path.join(visual_dir, "feature_importance.png"))
print(f"📊 Visuals saved to: {visual_dir}")
