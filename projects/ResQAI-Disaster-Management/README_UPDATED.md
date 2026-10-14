# ResQAI — Intelligent Disaster Relief Management System

## 1. Project Overview

ResQAI is an Intelligent Disaster Relief Management System. During natural disasters, people post on platforms like Twitter/X faster than official channels report. ResQAI screens incoming disaster-related posts, uses Machine Learning to estimate whether a post describes a real incident, prioritizes the urgency of the report, and presents a Dashboard for actionable intelligence. It separates genuine emergency reports from jokes, news headlines, and figurative language.

## 2. Problem Statement

Emergency response teams face an information overload during disasters. While social media provides real-time ground truth, the sheer volume of posts makes it impossible to manually separate life-threatening emergencies from noise. ResQAI solves this by automatically filtering noise, classifying genuine emergencies, assigning a priority score based on severity/casualties, and enabling operators to cross-check claims with independent news coverage.

## 3. Features

- **Text Disaster Classification:** Accurately classifies incoming text as "Disaster" or "Not Disaster" using a Support Vector Machine (SVM).
- **Urgency Prioritization:** Assigns a 0-100 priority score and band (CRITICAL, HIGH, MEDIUM, LOW) based on model confidence and a specialized emergency lexicon (e.g., "trapped", "casualties").
- **Model Explainability:** Shows the exact words that influenced the prediction (positive or negative contribution) so operators know *why* the decision was made.
- **Automated Reaction / Decision Support:** Recommends appropriate actions (e.g., "URGENT ESCALATION", "SUPPORT") based on classification and priority.
- **Incident Monitoring Dashboard:** Surfaces confirmed incidents in an administrative queue.
- **Live Trends & Analytics:** Displays a compact operational snapshot of incident categories, priority mix, and volume.
- **Corroboration Verification:** Uses Google News discovery to retrieve related publisher coverage for an X post to aid human verification.

## 4. System Architecture

The project follows a clean local ML pipeline architecture connected to a Flask web application:

User Input / Live Post
 ↓
FRONTEND (HTML/JS)
 ↓
FLASK API (/api/classify)
 ↓
PYTHON BACKEND (resqai_engine)
 ↓
TEXT PREPROCESSING (Clean → Tokenize → Stop-words → Stem)
 ↓
TF-IDF VECTORIZER
 ↓
SAVED ML MODEL (Support Vector Machine)
 ↓
PREDICTION + EXPLAINABILITY (Word Influence) + REACTION RULES
 ↓
JSON RESPONSE
 ↓
JAVASCRIPT (fetch)
 ↓
UI RESULT

*(Note: Audio analysis is not implemented in this application variant. The pipeline strictly handles text-based post/report screening.)*

## 5. Technology Stack

- **Backend:** Python, Flask
- **Machine Learning:** scikit-learn (Support Vector Machine, Logistic Regression, Naive Bayes, Random Forest)
- **Natural Language Processing:** NLTK (PorterStemmer, RegexpTokenizer), TF-IDF
- **Data Manipulation:** pandas, numpy
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (No heavy frameworks)
- **Live Integrations:** X API v2 (Recent Search), Google News RSS

## 6. Project Structure

```
ResQAI_Fixed/
├── app.py                      # Main Flask application and API routes
├── requirements.txt            # Python dependencies
├── README.md                   # Original project reference documentation
├── README_UPDATED.md           # This documentation file
├── data/
│   └── kaggle_reference/       # Dataset files (train.csv, test.csv)
├── model/
│   ├── train_models.py         # Script to train, evaluate, and save models
│   ├── resqai_classifier.pkl   # Saved best model (SVM)
│   ├── tfidf_vectorizer.pkl    # Saved TF-IDF vectorizer
│   └── model_metrics.pkl       # Saved metrics for dashboard rendering
├── utils/
│   ├── preprocessing.py        # Text cleaning, stop-word removal, stemming
│   ├── resqai_engine.py        # Classification, explainability, priorities, stats
│   └── live_sources.py         # X API integration and News corroboration
├── templates/
│   └── index.html              # Frontend dashboard
└── static/
    ├── css/
    │   └── style.css           # UI Styling
    └── js/
        └── script.js           # Frontend logic and API integration
```

## 7. Machine Learning Model

- **Dataset:** Kaggle "Natural Language Processing with Disaster Tweets" (7,613 records).
- **Preprocessing:** Text is lowercased, URLs/mentions/HTML entities are stripped, followed by RegExp tokenization. NLTK's English stop-words are removed, and words are stemmed using NLTK `PorterStemmer`.
- **TF-IDF:** The preprocessed text is transformed into TF-IDF vectors (up to 20,000 features, 1-2 ngrams).
- **Training:** `train_models.py` compares SVM, Logistic Regression, Naive Bayes, and Random Forest using cross-validation.
- **Evaluation:** SVM achieves the best F1-score and Recall, which is crucial to minimize false negatives (missed emergencies).
- **Model saving & loading:** The best model and vectorizer are saved via `joblib` into the `model/` directory, and loaded into memory by `resqai_engine.py` during inference.

## 8. How Prediction Works

User enters:
"Major earthquake destroyed the city, several people trapped."

1. **Frontend captures text** and the JavaScript sends a `POST` request to `/api/classify`.
2. **Flask receives JSON** containing `{"text": "..."}`.
3. **Text is cleaned** (lowercase, remove punctuation/URLs) and tokenized in `preprocessing.py`.
4. **TF-IDF transforms text** using the previously trained `tfidf_vectorizer.pkl`.
5. **Saved model predicts sentiment** by determining the distance from the SVM hyperplane.
6. **Probabilities are calculated** by squashing the margin through a logistic function (`math.exp`).
7. **Explainability & Rules:** `resqai_engine.py` extracts the SVM coefficients to highlight influential words (e.g., "earthquak", "trap"). It calculates a severity score using rule-based lexicons and assigns a recommended reaction.
8. **Backend creates JSON** and Flask returns it with HTTP 200.
9. **Frontend receives JSON** and updates the UI (rendering the classification card, priority bar, and word explanations).

## 9. Installation

Requirements: Python 3.10+

Open your terminal or command prompt:

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 10. Dataset Setup

The dataset should be located exactly at:
`data/kaggle_reference/train.csv`

The original dataset is provided in the repository. No further setup is required unless you want to update it.

## 11. Model Training

If you modify the preprocessing pipeline or want to retrain the model, run:
```powershell
python model\train_models.py
```
This script will preprocess the dataset, train all four models, compare their F1 scores, and overwrite the `.pkl` files in the `model/` folder with the best performing model.

## 12. Running the Application

To run the Flask application:
```powershell
python app.py
```
The terminal will display the local URL, usually:
`http://127.0.0.1:5400/`
Open this URL in your web browser. The app auto-selects a free port if 5400 is in use.

## 13. Audio Setup

Audio sentiment and emotion analysis is not part of this specific implementation. This application is dedicated strictly to text-based disaster relief management and short-message text intelligence.

## 14. API Documentation

### POST `/api/classify`
Analyzes a single text string.

**Request:**
```json
{
    "text": "Major earthquake destroyed the city, several people trapped",
    "location": "San Francisco"
}
```

**Response (Example):**
```json
{
    "text": "Major earthquake destroyed the city, several people trapped",
    "is_disaster": true,
    "label": "Disaster",
    "confidence": 98.4,
    "priority": 85.5,
    "priority_band": "CRITICAL",
    "category": "Earthquake / Landslide",
    "severity_score": 5.0,
    "reaction": "URGENT ESCALATION: Dispatch immediate emergency services.",
    "model_explanation": [
        {"word": "earthquak", "weight": 2.45, "contribution": "Positive (Disaster)"},
        {"word": "destroy", "weight": 1.25, "contribution": "Positive (Disaster)"}
    ]
}
```

## 15. Troubleshooting

- **`ModuleNotFoundError` or missing packages:** Ensure you have activated your virtual environment (`.\venv\Scripts\activate`) and ran `pip install -r requirements.txt`.
- **`FileNotFoundError` for `.pkl` files:** The models have not been trained. Run `python model\train_models.py`.
- **OverflowError in classification:** Fixed in the latest update; the logistic confidence margin handles extreme SVM distances gracefully.
- **Port already in use:** The app automatically finds a free port starting from 5400.
- **X API errors:** Ensure you have set your `X_BEARER_TOKEN` as an environment variable if you wish to use the live X feed.

## 16. Project Architecture Explanation

- **`app.py`:** The main entry point. Sets up Flask, defines the API endpoints, and coordinates HTTP requests.
- **`utils/preprocessing.py`:** The core NLP pipeline. Holds standard NLTK stop-words inline to avoid runtime download errors. Handles cleaning, tokenization, and stemming. Used by both training and inference.
- **`model/train_models.py`:** The offline training suite. Loads Kaggle data, runs TF-IDF vectorization, trains models, evaluates metrics, and saves the winner via Joblib.
- **`utils/resqai_engine.py`:** The live inference engine. Loads the trained models, runs text through `preprocessing`, makes predictions, generates model explainability, computes priority scores with lexicons, and formats the output dictionary.
- **`static/js/script.js`:** Connects the HTML to the Flask backend via `fetch` API, rendering results, feed cards, trends, and handling UI states like clear and word counts.

## 17. Future Improvements

- Map Geolocation: Extract geonames from the text to automatically place incoming disaster reports on a live interactive map.
- Transformer Models: Integrate Hugging Face transformers (e.g., BERT, RoBERTa) to improve recall rates, especially on ambiguous texts.
- Dedicated Database: Store incidents in SQLite/PostgreSQL instead of in-memory to persist data across restarts.
- WebSocket Integration: Push new X posts to the UI in real-time instead of requiring manual polling.
