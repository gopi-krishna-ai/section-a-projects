"""
AI-Assisted Smart Study Planner
Flask web application entry point.
"""

import os

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

from utils.planner_engine import get_full_view, mark_session_complete, mark_session_missed
from utils.storage import load_store, save_store, register_user, verify_user
from utils.ai_tutor import start_loading, get_tutor_response

app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(16)

# Start loading the LLM model in the background
start_loading()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("login.html", error="Username and password required")
        
        if action == "register":
            if register_user(username, password):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Username already exists")
        elif action == "login":
            if verify_user(username, password):
                session["username"] = username
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/app")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    store = load_store(username)
    return render_template("index.html", view=get_full_view(store))

@app.route("/tutor")
def tutor_page():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    return render_template("tutor.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    
    store = load_store(username)
    reply = get_tutor_response(store, message)
    return jsonify({"reply": reply})


@app.route("/view")
def view():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    store = load_store(username)
    return jsonify(get_full_view(store))


@app.route("/subjects", methods=["POST"])
def add_subject():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    exam_date = (data.get("exam_date") or "").strip()
    try:
        total_topics = int(data.get("total_topics"))
        completed_topics = int(data.get("completed_topics", 0))
        difficulty = int(data.get("difficulty"))
        weightage = int(data.get("weightage"))
    except (TypeError, ValueError):
        return jsonify({"error": "total_topics, completed_topics, difficulty and weightage must be numbers."}), 400

    if not name or not exam_date:
        return jsonify({"error": "Please provide a subject name and exam date."}), 400
    if total_topics <= 0:
        return jsonify({"error": "Total topics must be greater than 0."}), 400
    if not (1 <= difficulty <= 5) or not (1 <= weightage <= 5):
        return jsonify({"error": "Difficulty and weightage must be between 1 and 5."}), 400

    store = load_store(username)
    store["subjects"][name] = {
        "exam_date": exam_date,
        "total_topics": total_topics,
        "completed_topics": min(completed_topics, total_topics),
        "difficulty": difficulty,
        "weightage": weightage,
    }
    save_store(store, username)
    return jsonify(get_full_view(store))


@app.route("/subjects/<name>", methods=["DELETE"])
def delete_subject(name):
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    store = load_store(username)
    store["subjects"].pop(name, None)
    save_store(store, username)
    return jsonify(get_full_view(store))


@app.route("/upload_syllabus", methods=["POST"])
def upload_syllabus():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    subject = request.form.get("subject")
    if not subject:
        return jsonify({"error": "Subject name is required."}), 400
    
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded."}), 400
    
    text = ""
    if file.filename.endswith(".pdf"):
        import PyPDF2
        try:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            return jsonify({"error": f"Failed to read PDF: {e}"}), 400
    else:
        text = file.read().decode("utf-8", errors="ignore")
        
    # Extract topics
    topics = []
    import os
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"Extract a list of specific study topics from the following syllabus text. Return ONLY a JSON list of strings (e.g. [\"Topic 1\", \"Topic 2\"]). Keep topics concise.\n\nSyllabus:\n{text[:10000]}"
            resp = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            import json
            import re
            match = re.search(r'\[.*\]', resp.text, re.DOTALL)
            if match:
                topics = json.loads(match.group(0))
        except Exception as e:
            print("AI Extraction error:", e)
            
    if not topics:
        # Fallback heuristic
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 3 and len(line.strip()) < 50]
        topics = lines[:15] if lines else ["General Revision"]
        
    store = load_store(username)
    if subject not in store["subjects"]:
        return jsonify({"error": f"Subject '{subject}' not found. Please add it first."}), 400
        
    store["subjects"][subject]["topic_names"] = topics
    store["subjects"][subject]["total_topics"] = len(topics)
    save_store(store, username)
    
    return jsonify(get_full_view(store))


@app.route("/session/complete", methods=["POST"])
def session_complete():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    session_date = (data.get("session_date") or "").strip() or None
    store = load_store(username)
    try:
        mark_session_complete(store, subject, session_date)
    except KeyError:
        return jsonify({"error": f"Unknown subject '{subject}'."}), 400
    save_store(store, username)
    return jsonify(get_full_view(store))


@app.route("/session/missed", methods=["POST"])
def session_missed():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    data = request.get_json(silent=True) or {}
    subject = (data.get("subject") or "").strip()
    session_date = (data.get("session_date") or "").strip() or None
    store = load_store(username)
    try:
        mark_session_missed(store, subject, session_date)
    except KeyError:
        return jsonify({"error": f"Unknown subject '{subject}'."}), 400
    save_store(store, username)
    return jsonify(get_full_view(store))


@app.route("/settings", methods=["POST"])
def update_settings():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    username = session["username"]
    data = request.get_json(silent=True) or {}
    try:
        daily_hours = float(data.get("daily_hours"))
    except (TypeError, ValueError):
        return jsonify({"error": "daily_hours must be a number."}), 400
    if not (0.5 <= daily_hours <= 16):
        return jsonify({"error": "daily_hours must be between 0.5 and 16."}), 400

    store = load_store(username)
    store["settings"]["daily_hours"] = daily_hours
    save_store(store, username)
    return jsonify(get_full_view(store))


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5050)))
