import urllib.request
import pandas as pd

urls = [
    "https://raw.githubusercontent.com/dkhundley/nlp-disaster-tweets/master/data/train.csv",
    "https://raw.githubusercontent.com/sebischair/NLU-Disaster-Tweets/master/data/train.csv",
    "https://raw.githubusercontent.com/jorgearanda/disaster-tweets/master/train.csv"
]

for url in urls:
    try:
        print(f"Trying {url}...")
        df = pd.read_csv(url)
        if 'text' in df.columns and 'target' in df.columns:
            print(f"Success! Found {len(df)} rows.")
            df.to_csv('data/kaggle_train.csv', index=False)
            break
    except Exception as e:
        print(f"Failed: {e}")
