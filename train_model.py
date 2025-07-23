import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from utils import preprocess_url
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib

def main():
    # Create visuals directory if it doesn't exist
    visual_dir = r"C:\Users\red_l\PycharmProjects\MaliciousURL\visuals"
    os.makedirs(visual_dir, exist_ok=True)

    # Load cleaned dataset
    file_path = r"C:\Users\red_l\PycharmProjects\MaliciousURL\Data\cleaned_data.csv"
    dataset = pd.read_csv(file_path)
    print(f"Loaded dataset with shape: {dataset.shape}")

    # Prepare features and labels
    feature_rows = [preprocess_url(url).iloc[0] for url in dataset['url']]
    X = pd.DataFrame(feature_rows)
    y = dataset['label']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("Data split complete. Training model...")

    # Train model
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=2.35,
        eval_metric="logloss",
        random_state=42,
        use_label_encoder=False,
    )
    model.fit(X_train, y_train)
    print("Training complete.")

    # Predictions & evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benign", "Malicious"], yticklabels=["Benign", "Malicious"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    conf_matrix_path = os.path.join(visual_dir, "confusion_matrix.png")
    plt.savefig(conf_matrix_path)
    plt.show()

    # Feature Importance
    xgb.plot_importance(model, importance_type='weight', max_num_features=10)
    plt.title("Top 10 Feature Importances")
    plt.tight_layout()
    feat_importance_path = os.path.join(visual_dir, "feature_importance.png")
    plt.savefig(feat_importance_path)
    plt.show()

    # Save model
    model_dir = r"C:\Users\red_l\PycharmProjects\MaliciousURL\model"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "xgboost_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to: {model_path}")
    print(f"Visuals saved to: {visual_dir}")
    print(dataset['label'].value_counts())

if __name__ == "__main__":
    main()
