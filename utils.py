import pandas as pd
import re
from urllib.parse import urlparse

def preprocess_url(url):
    if not isinstance(url, str):
        url = ""
    url = url.strip().lower()
    ...


    # Base features
    url_length = len(url)
    num_digits = len(re.findall(r'\d', url))
    num_special_chars = len(re.findall(r'[-_%@]', url))
    has_ip = 1 if re.search(r'(?:\d{1,3}\.){3}\d{1,3}', url) else 0
    keyword_flag = int(any(keyword in url for keyword in ['login', 'verify', 'secure']))

    # NEW: contains '@'
    contains_at_symbol = 1 if '@' in url else 0

    # NEW: subdomain count
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    num_subdomains = max(len(hostname.split('.')) - 2, 0)  # At least 0

    # NEW: uses shortening service
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd']
    uses_shortener = 1 if any(short in hostname for short in shorteners) else 0

    features = {
        'url_length': url_length,
        'num_digits': num_digits,
        'num_special_chars': num_special_chars,
        'has_ip': has_ip,
        'keyword_flag': keyword_flag,
        'contains_at_symbol': contains_at_symbol,
        'num_subdomains': num_subdomains,
        'uses_shortener': uses_shortener
    }

    return pd.DataFrame([features])
