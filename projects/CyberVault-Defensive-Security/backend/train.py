import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import pickle
import re

def train_url_model():
    df = pd.read_csv('phishing_dataset.csv')
    X = df[['length', 'has_ip', 'has_at', 'has_hyphen', 'is_https']]
    y = df['is_phishing']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    with open('phishing_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("URL model trained and saved as phishing_model.pkl")

def train_email_model():
    df = pd.read_csv('email_dataset.csv')
    X = df['text']
    y = df['label']
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', lowercase=True)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X, y)
    
    with open('email_phishing_model.pkl', 'wb') as f:
        pickle.dump(pipeline, f)
    print("Email model trained and saved as email_phishing_model.pkl")

if __name__ == '__main__':
    train_url_model()
    train_email_model()
