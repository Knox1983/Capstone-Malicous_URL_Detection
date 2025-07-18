import pandas as pd
import os

def main():
    # Load balanced dataset
    balanced_df = pd.read_csv(r'C:\Users\red_l\PycharmProjects\MaliciousURL\Data\balanced_urls.csv')
    print(balanced_df.head())
    print("Balanced dataset loaded:", balanced_df.shape)

    # Map labels if needed
    if balanced_df['label'].dtype == object:
        balanced_df['label'] = balanced_df['label'].replace({
            'benign': 0,
            'malicious': 1
        }).astype(int)

    if 'result' in balanced_df.columns and balanced_df['label'].equals(balanced_df['result']):
        balanced_df = balanced_df.drop(columns=['result'])

    balanced_df = balanced_df[['url', 'label']]

    # Load malicious_phish.csv
    phish_df = pd.read_csv(r'C:\Users\red_l\PycharmProjects\MaliciousURL\Data\malicious_phish.csv')
    print("Malicious dataset loaded:", phish_df.shape)
    print("Unique 'type' values in phish_df:\n", phish_df['type'].unique())

    phish_df['type'] = phish_df['type'].str.strip().str.lower()
    mapping = {'benign': 0, 'defacement': 1, 'phishing': 1, 'malware': 1}
    phish_df['label'] = phish_df['type'].map(mapping)
    phish_df = phish_df.dropna(subset=['label'])
    phish_df = phish_df[['url', 'label']]
    print("Cleaned phish_df label counts:\n", phish_df['label'].value_counts())

    # Load OpenPhish TXT
    with open(r'C:\Users\red_l\PycharmProjects\MaliciousURL\Data\openphish_urls_sample.txt', 'r') as f:
        openphish_urls = f.readlines()

    openphish_df = pd.DataFrame(openphish_urls, columns=['url'])
    openphish_df['url'] = openphish_df['url'].str.strip().str.lower()
    openphish_df['label'] = 1
    print("OpenPhish dataset loaded:", openphish_df.shape)
    print(openphish_df.head())

    # Combine datasets
    full_df = pd.concat([balanced_df, phish_df, openphish_df], ignore_index=True)
    full_df = full_df.drop_duplicates(subset=['url', 'label'])
    print("Combined dataset shape:", full_df.shape)
    print("Label distribution:\n", full_df['label'].value_counts())

    # Feature engineering
    full_df['url_length'] = full_df['url'].apply(len)
    full_df['num_digits'] = full_df['url'].str.count(r'\d')
    full_df['num_special_chars'] = full_df['url'].str.count(r'[-_%@]')
    full_df['has_ip'] = full_df['url'].str.contains(r'(?:\d{1,3}\.){3}\d{1,3}')
    keywords = ['login', 'verify', 'secure']
    full_df['keyword_flag'] = full_df['url'].apply(lambda x: int(any(k in x for k in keywords)))

    # Preview engineered features
    print(full_df[['url', 'url_length', 'num_digits', 'num_special_chars', 'has_ip', 'keyword_flag', 'label']].head())

    # Save final cleaned dataset
    output_path = r'C:\Users\red_l\PycharmProjects\MaliciousURL\Data\cleaned_data.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    full_df.to_csv(output_path, index=False)
    print(f"✅ Cleaned dataset with features saved to {output_path}")

if __name__ == "__main__":
    main()