# B-2: AI-Assisted Smart Study Planner (Advanced Edition)

The **AI-Assisted Smart Study Planner** is a highly personalized, adaptive scheduling web application. It uses a custom Machine Learning pipeline (Random Forest) combined with **Generative AI** (Google Gemini) to dynamically build, prioritize, and adjust your study plan. 

This Advanced Edition introduces a massive visual overhaul (Glassmorphism), Multi-User Authentication, an AI Chat Tutor, and a Smart Syllabus Extractor.

## 🚀 Advanced AI/ML Features Added

- **🤖 AI Chat Tutor (LLM Integration):** A dedicated chat interface where students can talk to a personalized AI Tutor. The tutor is aware of your specific study plan, completed topics, and exam dates (acting as context for the LLM) to provide highly personalized guidance.
- **📄 Smart Syllabus Extractor (NLP):** Upload your syllabus as a PDF or text file. The AI automatically parses the document, extracts the specific topics you need to study, and injects them directly into your Pomodoro study schedule on exact days.
- **🔐 Multi-User Authentication:** A fully functional registration and login system utilizing secure SHA-256 password hashing and Flask Session cookies. Each user gets an isolated JSON datastore (`data/<username>_store.json`), keeping study plans completely separate.
- **✨ Glassmorphism UI:** A complete aesthetic overhaul featuring dynamic frosted-glass panels, Lofi workspace backgrounds, and a clean, responsive layout.

## 🧠 Core Algorithmic Features

- **Random Forest Priority Prediction:** Every time you load the page or mark a session done, a locally-trained Random Forest model predicts the priority (High, Medium, Low) and a 0-100 urgency score for each subject based on days left to exam, completion percentage, difficulty, and weightage.
- **Adaptive Pomodoro Schedule:** A 7-day rolling plan is generated on the fly. It allocates your daily study hours across subjects in proportion to their AI-predicted urgency, using 25-minute study / 5-minute break sessions.
- **Topic-Level Granularity:** Thanks to the Syllabus Extractor, the schedule tells you *exactly what topic* to study during a specific Pomodoro session, rather than just giving you a generic subject block.
- **Evidence-Based Recommendations:** The recommendation engine parses real-world study data (from a 30k+ student Kaggle dataset) to warn you about burnout or suggest pre-exam revision strategies.

## 🛠️ Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| Backend            | Python, Flask                        |
| Machine Learning    | scikit-learn (Random Forest), Pandas |
| Generative AI      | `google-genai` SDK (Gemini-2.5-Flash) |
| Document Parsing   | `PyPDF2`                            |
| Frontend           | HTML, CSS (Glassmorphism), JavaScript|
| Database           | Isolated Local JSON Flat-Files       |

## 📂 Folder Structure

```
B-2-AI Assisted Smart Study Planner/
├── app.py                         Flask application (Auth, APIs, Views)
├── requirements.txt
├── data/
│   ├── users.json                 Stores registered users & hashed passwords
│   ├── <username>_store.json      Isolated study data per user
│   ├── generate_dataset.py        Generates the simulated ML training dataset
│   ├── priority_dataset.csv       Training data 
│   ├── process_kaggle_dataset.py  Computes real study benchmarks
│   ├── kaggle_reference/          Source CSVs for analytics
├── model/
│   ├── train_model.py             Trains and saves the Random Forest model
│   └── study_priority_rf_model.pkl
├── utils/
│   ├── ai_tutor.py                Handles Google GenAI context injection
│   ├── planner_engine.py          Topic allocation & Priority scoring
│   └── storage.py                 Handles Auth and JSON saving/loading
├── templates/
│   ├── login.html                 Auth / Landing Page
│   ├── index.html                 Main Dashboard
│   └── tutor.html                 AI Chat Interface
└── static/
    ├── css/style.css              Glassmorphism Styles
    ├── js/script.js               Frontend logic
    └── bg.jpg                     App Background
```

## ⚙️ Setup & Run

### Prerequisites
Make sure you have an active `GEMINI_API_KEY` to unlock the AI Tutor and Syllabus Extractor.

```bash
# Set your API Key in your terminal
set GEMINI_API_KEY="your_api_key_here"  # Windows
export GEMINI_API_KEY="your_api_key_here" # Mac/Linux
```

### Installation
```bash
cd "B-2-AI Assisted Smart Study Planner"
pip install -r requirements.txt
pip install google-genai PyPDF2

# 1. Generate the simulated priority-classifier training dataset
python data/generate_dataset.py

# 2. Train the Random Forest model
python model/train_model.py

# 3. Run the web app
python app.py
```

Open **http://127.0.0.1:5050/** in your browser. Register an account, add a subject, upload a syllabus, and start studying!

## 🔮 Future Enhancements
- **Computer Vision Focus Monitor:** Use OpenCV to track eye gaze and pause the Pomodoro timer if the user gets distracted.
- **Auto-Flashcard Generation:** Use the LLM to automatically generate quizzes based on the extracted syllabus topics.
- **Predictive Exam Scoring:** A regression model that predicts your final score based on completion rate.
