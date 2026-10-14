import urllib.request
import json
import pandas as pd

search_url = 'https://api.github.com/search/code?q=filename:train.csv+target+text+keyword+location+disaster'
try:
    req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    
    for item in data.get('items', [])[:5]:
        raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        print(f"Checking {raw_url}")
        try:
            df = pd.read_csv(raw_url)
            if 'text' in df.columns and 'target' in df.columns and len(df) > 5000:
                print(f"Successfully downloaded {len(df)} rows from {raw_url}")
                df.to_csv('data/kaggle_train.csv', index=False)
                break
        except:
            pass
except Exception as e:
    print(f"Search failed: {e}")
