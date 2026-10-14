import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib
import time

print("--- STARTING KAGGLE DATASET TRAINING ---")

stop_words = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])

def clean_text(text):
    text = str(text)
    text = re.sub(r'http\S+', '', text) # URLs
    text = re.sub(r'@\w+', '', text)    # Mentions
    text = re.sub(r'#\w+', '', text)    # Hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Special chars
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

print("Loading Kaggle Dataset...")
df = pd.read_csv('data/kaggle_train.csv')
print(f"Loaded {len(df)} tweets.")

print("Cleaning text...")
df['clean_text'] = df['text'].apply(clean_text)

# Drop missing values if any
df = df.dropna(subset=['clean_text', 'target'])

X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['target'], test_size=0.2, random_state=42)

print("Vectorizing text (TF-IDF)...")
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training SVM Model on Kaggle Data...")
start_time = time.time()
svm_model = LinearSVC(random_state=42, dual=False, C=1.0)
svm_model.fit(X_train_vec, y_train)
print(f"Training completed in {time.time() - start_time:.2f} seconds.")

y_pred = svm_model.predict(X_test_vec)
print("\n--- Kaggle Dataset Model Performance ---")
print(classification_report(y_test, y_pred))

print("Saving production models to ml/models/...")
joblib.dump(vectorizer, 'ml/models/vectorizer.pkl')
joblib.dump(svm_model, 'ml/models/model.pkl')
print("Done!")
