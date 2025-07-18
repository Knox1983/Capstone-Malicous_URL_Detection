import pandas as pd
import joblib
import os
import re

# Feature Engineering
def extract_features(df):
    df['url_length'] = df['url'].apply(len)
    df['num_digits'] = df['url'].str.count(r'\d')
    df['num_special_chars'] = df['url'].str.count(r'[-_%@]')
    df['has_ip'] = df['url'].str.contains(r'(?:\d{1,3}\.){3}\d{1,3}')
    keywords = ['login', 'verify', 'secure']
    df['keyword_flag'] = df['url'].apply(lambda x: int(any(k in x for k in keywords)))
    return df

# Load URLs from TXT or CSV
def load_input_file(path):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".txt":
        with open(path, "r") as f:
            urls = f.read().splitlines()
        df = pd.DataFrame(urls, columns=["url"])
    elif ext == ".csv":
        df = pd.read_csv(path)
        if "url" not in df.columns:
            raise ValueError("CSV must have a 'url' column.")
    else:
        raise ValueError("Unsupported file format. Use .txt or .csv")

    df['url'] = df['url'].astype(str).str.strip().str.lower()
    return df

# Main Prediction Logic
def main():
    # Load model
    model_path = r"C:\Users\red_l\PycharmProjects\MaliciousURL\model\xgboost_model.pkl"
    model = joblib.load(model_path)
    print(f"Loaded model from: {model_path}")

    # Input file (change this to test different formats txt or csv)
    input_path = r"C:\Users\red_l\PycharmProjects\MaliciousURL\Data\new_urls.csv"
    df = load_input_file(input_path)

    # Extract features and predict
    df = extract_features(df)
    features = df.drop(columns=["url"])
    predictions = model.predict(features)
    df['prediction'] = predictions

    # Show results
    print("\n Prediction Results:")
    print(df[["url", "prediction"]])

    # Save results
    output_path = r"C:\Users\red_l\PycharmProjects\MaliciousURL\Data\predicted_urls.csv"
    df.to_csv(output_path, index=False)
    print(f"\n Results saved to: {output_path}")

if __name__ == "__main__":
    main()