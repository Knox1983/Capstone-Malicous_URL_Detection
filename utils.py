import pandas as pd
import re

def preprocess_url(url):
    url = url.strip().lower()

    features = {
        'url_length': len(url),
        'num_digits': len(re.findall(r'\d', url)),
        'num_special_chars': len(re.findall(r'[-_%@]', url)),
        'has_ip': 1 if re.search(r'(?:\d{1,3}\.){3}\d{1,3}', url) else 0,
        'keyword_flag': int(any(keyword in url for keyword in ['login', 'verify', 'secure']))
    }

    return pd.DataFrame([features])
