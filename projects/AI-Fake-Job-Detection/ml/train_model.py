import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
import os

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'[^a-z\s]', '', text) # Remove special characters and numbers
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

def train():
    data_path = '../data/job_postings.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please place your EMSCAD dataset there.")
        print("For testing purposes, I will generate a small dummy dataset.")
        
        # Create dummy data if CSV doesn't exist just so the script runs
        os.makedirs('../data', exist_ok=True)
        dummy_data = {
            'description': [
                "We are looking for a software engineer with Python skills.",
                "URGENT!! Work from home, guaranteed placement, pay $5000 a week! Just pay $50 registration fee.",
                "Data scientist needed. Experience with Machine Learning and SQL required.",
                "Data entry clerk needed immediately. Must provide bank details before interview.",
                "Looking for a frontend developer. React and CSS experience is a must.",
                "Easy money! No experience needed. Start tomorrow. Send SSN for background check."
            ],
            'fraudulent': [0, 1, 0, 1, 0, 1]
        }
        df = pd.DataFrame(dummy_data)
        df.to_csv(data_path, index=False)
        print("Dummy dataset created.")

    df = pd.read_csv(data_path)
    
    # In EMSCAD, often 'description', 'requirements', 'benefits' are combined. 
    # For this script, we'll assume a 'description' and 'fraudulent' column exists.
    # If using real EMSCAD, you'd combine text columns here.
    if 'description' not in df.columns or 'fraudulent' not in df.columns:
         print("Warning: CSV must contain 'description' and 'fraudulent' columns.")
         return

    print("Cleaning text...")
    df['cleaned_text'] = df['description'].apply(clean_text)

    X = df['cleaned_text']
    y = df['fraudulent']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Building pipeline with TF-IDF, SMOTE, and Random Forest...")
    # ImbPipeline is used so SMOTE is only applied to training data during fit
    pipeline = ImbPipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('smote', SMOTE(random_state=42)),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    accuracy = pipeline.score(X_test, y_test)
    print(f"Model trained. Test Accuracy: {accuracy:.4f}")

    os.makedirs('../artifacts', exist_ok=True)
    joblib.dump(pipeline, '../artifacts/model_pipeline.pkl')
    print("Model saved to artifacts/model_pipeline.pkl")

if __name__ == '__main__':
    train()
