import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import joblib
import pandas as pd
from lime.lime_text import LimeTextExplainer
from PyPDF2 import PdfReader
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_PATH = 'artifacts/model_pipeline.pkl'
try:
    model_pipeline = joblib.load(MODEL_PATH)
    explainer = LimeTextExplainer(class_names=['Genuine', 'Fraudulent'])
    print("Model loaded successfully.")
except Exception as e:
    model_pipeline = None
    print(f"Warning: Could not load model. Error: {e}")

COMMON_SKILLS = ['python', 'java', 'c++', 'sql', 'machine learning', 'deep learning', 'react', 'node', 'aws', 'docker', 'kubernetes', 'html', 'css', 'javascript', 'communication', 'leadership', 'data analysis', 'excel']

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + " "
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/analyze_job', methods=['POST'])
def analyze_job():
    if model_pipeline is None:
         return jsonify({"error": "Model not trained."}), 500

    text_input = request.form.get('job_text', '')
    
    if not text_input and 'job_pdf' in request.files:
        pdf_file = request.files['job_pdf']
        if pdf_file.filename != '':
            text_input = extract_text_from_pdf(pdf_file)

    if not text_input.strip():
        return jsonify({"error": "No text provided."}), 400

    # Prediction
    pred = model_pipeline.predict([text_input])[0]
    prob = model_pipeline.predict_proba([text_input])[0]
    confidence_score = round(prob[pred] * 100, 2)
    is_scam = bool(pred == 1)

    # Explainable AI (LIME)
    scam_words = []
    if is_scam:
        try:
            exp = explainer.explain_instance(text_input, model_pipeline.predict_proba, num_features=5)
            scam_words = [word for word, weight in exp.as_list() if weight > 0]
        except:
            pass

    # Extract required skills
    job_text_lower = text_input.lower()
    required_skills = [skill for skill in COMMON_SKILLS if skill in job_text_lower]

    return jsonify({
        "is_scam": is_scam,
        "confidence": confidence_score,
        "scam_words": scam_words,
        "required_skills": required_skills
    })

@app.route('/api/match_resume', methods=['POST'])
def match_resume():
    required_skills = request.form.get('required_skills', '').split(',')
    required_skills = [s.strip() for s in required_skills if s.strip()]
    
    resume_text = request.form.get('resume_text', '')
    if not resume_text and 'resume_pdf' in request.files:
        pdf_file = request.files['resume_pdf']
        if pdf_file.filename != '':
            resume_text = extract_text_from_pdf(pdf_file)

    if not resume_text.strip():
         return jsonify({"error": "No resume provided."}), 400
         
    resume_text_lower = resume_text.lower()
    
    found_skills = []
    missing_skills = []
    
    if not required_skills:
        return jsonify({"readiness": 100, "found": [], "missing": []})
        
    for skill in required_skills:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    readiness = int(((len(required_skills) - len(missing_skills)) / len(required_skills)) * 100)
    
    return jsonify({
        "readiness": readiness,
        "found": found_skills,
        "missing": missing_skills
    })

if __name__ == '__main__':
    app.run(debug=True)
