import pandas as pd
urls = [
    'https://raw.githubusercontent.com/laxmimerit/twitter-disaster-prediction-dataset/master/train.csv',
    'https://huggingface.co/datasets/mehdiiraqui/twitter_disaster/resolve/main/train.csv',
    'https://raw.githubusercontent.com/susanli2016/NLP-with-Python/master/data/disaster_tweets.csv',
    'https://raw.githubusercontent.com/AyoubB-64/Disaster-Tweets/main/train.csv'
]
success = False
for url in urls:
    try:
        print(f"Trying {url}")
        df = pd.read_csv(url)
        if 'text' in df.columns and 'target' in df.columns:
            print(f"Success! {len(df)} rows.")
            df.to_csv('data/kaggle_train.csv', index=False)
            success = True
            break
    except:
        pass
if not success:
    print("Could not download.")
