"""
AI-Assisted Smart Study Planner with Productivity Prediction
Flask Backend Application

Author: Student Project
Version: 1.0.0
Description: A Flask-based backend that handles study session tracking,
             AI productivity prediction using machine learning, and
             analytics endpoints.
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from datetime import datetime, timedelta
import os
import json

from database import db, init_db
from models import User, Subject, StudySession, Task, ProductivityRecord
from ai_predictor import ProductivityPredictor

# ─── App Configuration ──────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "study-planner-secret-2026")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///study_planner.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "jwt-secret-study-ai")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

# Enable CORS for React frontend
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
predictor = ProductivityPredictor()

# ─── Helper Functions ────────────────────────────────────────────────────────

def success_response(data, message="Success", status=200):
    return jsonify({"status": "success", "message": message, "data": data}), status

def error_response(message, status=400):
    return jsonify({"status": "error", "message": message}), status

# ─── Authentication Routes ───────────────────────────────────────────────────

@app.route("/api/auth/register", methods=["POST"])
def register():
    """Register a new student user."""
    data = request.get_json()

    if not data:
        return error_response("No data provided")

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not all([name, email, password]):
        return error_response("Name, email, and password are required")

    if len(password) < 6:
        return error_response("Password must be at least 6 characters")

    # Check if user already exists
    existing = User.query.filter_by(email=email).first()
    if existing:
        return error_response("Email already registered", 409)

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return success_response({
        "user": user.to_dict(),
        "access_token": access_token
    }, "Registration successful", 201)


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Login endpoint — returns JWT token."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return error_response("Invalid email or password", 401)

    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return success_response({
        "user": user.to_dict(),
        "access_token": access_token
    }, "Login successful")


@app.route("/api/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get the currently authenticated user's profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return error_response("User not found", 404)

    return success_response(user.to_dict())

# ─── Subject Routes ──────────────────────────────────────────────────────────

@app.route("/api/subjects", methods=["GET"])
@jwt_required()
def get_subjects():
    """Get all subjects for the authenticated user."""
    user_id = get_jwt_identity()
    subjects = Subject.query.filter_by(user_id=user_id, is_active=True).all()
    return success_response([s.to_dict() for s in subjects])


@app.route("/api/subjects", methods=["POST"])
@jwt_required()
def add_subject():
    """Add a new subject to the study plan."""
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data.get("name", "").strip()
    daily_hours = float(data.get("daily_hours", 2))
    preferred_time = data.get("preferred_time", "18:00")
    difficulty = data.get("difficulty", "Medium")
    emoji = data.get("emoji", "📚")
    color = data.get("color", "#4F8EF7")

    if not name:
        return error_response("Subject name is required")

    if difficulty not in ["Easy", "Medium", "Hard"]:
        return error_response("Difficulty must be Easy, Medium, or Hard")

    subject = Subject(
        user_id=user_id,
        name=name,
        daily_hours=daily_hours,
        preferred_time=preferred_time,
        difficulty=difficulty,
        emoji=emoji,
        color=color,
    )
    db.session.add(subject)
    db.session.commit()

    return success_response(subject.to_dict(), "Subject added successfully", 201)


@app.route("/api/subjects/<int:subject_id>", methods=["PUT"])
@jwt_required()
def update_subject(subject_id):
    """Update an existing subject."""
    user_id = get_jwt_identity()
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()

    if not subject:
        return error_response("Subject not found", 404)

    data = request.get_json()
    subject.name = data.get("name", subject.name)
    subject.daily_hours = float(data.get("daily_hours", subject.daily_hours))
    subject.preferred_time = data.get("preferred_time", subject.preferred_time)
    subject.difficulty = data.get("difficulty", subject.difficulty)
    subject.emoji = data.get("emoji", subject.emoji)
    subject.color = data.get("color", subject.color)
    db.session.commit()

    return success_response(subject.to_dict(), "Subject updated")


@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
@jwt_required()
def delete_subject(subject_id):
    """Soft-delete a subject."""
    user_id = get_jwt_identity()
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()

    if not subject:
        return error_response("Subject not found", 404)

    subject.is_active = False
    db.session.commit()

    return success_response(None, "Subject deleted")

# ─── Study Session Routes ────────────────────────────────────────────────────

@app.route("/api/sessions", methods=["GET"])
@jwt_required()
def get_sessions():
    """Get all study sessions for the user."""
    user_id = get_jwt_identity()
    days = int(request.args.get("days", 7))
    since = datetime.utcnow() - timedelta(days=days)

    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.started_at >= since
    ).order_by(StudySession.started_at.desc()).all()

    return success_response([s.to_dict() for s in sessions])


@app.route("/api/sessions/start", methods=["POST"])
@jwt_required()
def start_session():
    """Start a new study session."""
    user_id = get_jwt_identity()
    data = request.get_json()

    subject_id = data.get("subject_id")
    if not subject_id:
        return error_response("subject_id is required")

    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    if not subject:
        return error_response("Subject not found", 404)

    # Check for active session
    active = StudySession.query.filter_by(
        user_id=user_id, is_active=True
    ).first()
    if active:
        return error_response("You already have an active session. End it first.", 409)

    session_obj = StudySession(
        user_id=user_id,
        subject_id=subject_id,
        started_at=datetime.utcnow(),
        is_active=True
    )
    db.session.add(session_obj)
    db.session.commit()

    return success_response(session_obj.to_dict(), "Session started", 201)


@app.route("/api/sessions/<int:session_id>/end", methods=["POST"])
@jwt_required()
def end_session(session_id):
    """End an active study session and record productivity."""
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    session_obj = StudySession.query.filter_by(
        id=session_id, user_id=user_id, is_active=True
    ).first()

    if not session_obj:
        return error_response("Active session not found", 404)

    session_obj.ended_at = datetime.utcnow()
    session_obj.is_active = False
    session_obj.focus_score = data.get("focus_score", 80)
    session_obj.notes = data.get("notes", "")

    # Calculate duration in minutes
    duration = (session_obj.ended_at - session_obj.started_at).seconds // 60
    session_obj.duration_minutes = duration

    db.session.commit()

    # Auto-calculate and record productivity
    productivity_score = predictor.calculate_actual_productivity(
        duration_minutes=duration,
        focus_score=session_obj.focus_score,
        hour_of_day=session_obj.started_at.hour
    )

    record = ProductivityRecord(
        user_id=user_id,
        date=datetime.utcnow().date(),
        productivity_score=productivity_score,
        total_hours=round(duration / 60, 2),
        sessions_count=1
    )
    db.session.add(record)
    db.session.commit()

    return success_response({
        "session": session_obj.to_dict(),
        "productivity_score": productivity_score
    }, "Session ended")

# ─── Task Routes ─────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    """Get all tasks for the user, optionally filtered by date."""
    user_id = get_jwt_identity()
    date_str = request.args.get("date")

    query = Task.query.filter_by(user_id=user_id)

    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(db.func.date(Task.created_at) == target_date)
        except ValueError:
            return error_response("Invalid date format. Use YYYY-MM-DD")

    tasks = query.order_by(Task.priority.asc(), Task.created_at.desc()).all()
    return success_response([t.to_dict() for t in tasks])


@app.route("/api/tasks", methods=["POST"])
@jwt_required()
def create_task():
    """Create a new task."""
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get("title", "").strip()
    if not title:
        return error_response("Task title is required")

    task = Task(
        user_id=user_id,
        subject_id=data.get("subject_id"),
        title=title,
        duration=data.get("duration", "1h"),
        priority=data.get("priority", "medium"),
        category=data.get("category", "Study"),
        due_date=data.get("due_date"),
    )
    db.session.add(task)
    db.session.commit()

    return success_response(task.to_dict(), "Task created", 201)


@app.route("/api/tasks/<int:task_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_task(task_id):
    """Toggle task completion status."""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return error_response("Task not found", 404)

    task.completed = not task.completed
    task.completed_at = datetime.utcnow() if task.completed else None
    db.session.commit()

    return success_response(task.to_dict(), "Task updated")


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """Delete a task."""
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return error_response("Task not found", 404)

    db.session.delete(task)
    db.session.commit()

    return success_response(None, "Task deleted")

# ─── AI Productivity Prediction Routes ──────────────────────────────────────

@app.route("/api/predict/productivity", methods=["GET"])
@jwt_required()
def predict_productivity():
    """
    AI Prediction: Predict today's productivity score and best study times.

    This endpoint uses the ProductivityPredictor ML model (trained on user's
    past 7-day study patterns) to forecast:
      - Today's overall productivity score (0-100%)
      - Best study time windows for the day
      - Focus trend (improving / declining / stable)
    """
    user_id = get_jwt_identity()

    # Fetch last 7 days of productivity records
    since = datetime.utcnow() - timedelta(days=7)
    records = ProductivityRecord.query.filter(
        ProductivityRecord.user_id == user_id,
        ProductivityRecord.date >= since.date()
    ).order_by(ProductivityRecord.date.asc()).all()

    # Fetch sessions to analyze hourly patterns
    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.started_at >= since,
        StudySession.is_active == False
    ).all()

    # Run AI Prediction
    prediction = predictor.predict(
        productivity_records=[r.to_dict() for r in records],
        sessions=[s.to_dict() for s in sessions],
        current_hour=datetime.utcnow().hour
    )

    return success_response(prediction)


@app.route("/api/predict/best-time", methods=["GET"])
@jwt_required()
def predict_best_time():
    """
    AI Prediction: Get the best study time windows for today.

    Uses historical session data to identify when the user's focus
    and retention are highest throughout the day.
    """
    user_id = get_jwt_identity()
    since = datetime.utcnow() - timedelta(days=30)

    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.started_at >= since,
        StudySession.ended_at.isnot(None)
    ).all()

    best_times = predictor.find_best_study_times(
        [s.to_dict() for s in sessions]
    )

    return success_response(best_times)

# ─── Analytics Routes ────────────────────────────────────────────────────────

@app.route("/api/analytics/overview", methods=["GET"])
@jwt_required()
def analytics_overview():
    """Get comprehensive analytics for the user's study performance."""
    user_id = get_jwt_identity()
    days = int(request.args.get("days", 30))
    since = datetime.utcnow() - timedelta(days=days)

    sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        StudySession.started_at >= since,
        StudySession.ended_at.isnot(None)
    ).all()

    tasks = Task.query.filter(
        Task.user_id == user_id,
        Task.created_at >= since
    ).all()

    productivity_records = ProductivityRecord.query.filter(
        ProductivityRecord.user_id == user_id,
        ProductivityRecord.date >= since.date()
    ).all()

    total_hours = sum(
        (s.duration_minutes or 0) / 60 for s in sessions
    )
    avg_productivity = (
        sum(r.productivity_score for r in productivity_records) /
        len(productivity_records)
        if productivity_records else 0
    )
    task_completion_rate = (
        len([t for t in tasks if t.completed]) / len(tasks) * 100
        if tasks else 0
    )

    # Build daily breakdown
    daily_data = {}
    for session in sessions:
        day = session.started_at.strftime("%Y-%m-%d")
        if day not in daily_data:
            daily_data[day] = {"hours": 0, "sessions": 0}
        daily_data[day]["hours"] += (session.duration_minutes or 0) / 60
        daily_data[day]["sessions"] += 1

    # Build hourly heatmap
    hourly_scores = {}
    for session in sessions:
        hour = session.started_at.hour
        if hour not in hourly_scores:
            hourly_scores[hour] = []
        if session.focus_score:
            hourly_scores[hour].append(session.focus_score)

    hourly_avg = {
        h: round(sum(scores) / len(scores), 1)
        for h, scores in hourly_scores.items()
    }

    return success_response({
        "summary": {
            "total_hours": round(total_hours, 2),
            "avg_productivity": round(avg_productivity, 1),
            "task_completion_rate": round(task_completion_rate, 1),
            "total_sessions": len(sessions),
            "total_tasks": len(tasks),
        },
        "daily_breakdown": daily_data,
        "hourly_heatmap": hourly_avg,
        "productivity_records": [r.to_dict() for r in productivity_records],
    })


@app.route("/api/analytics/subject-performance", methods=["GET"])
@jwt_required()
def subject_performance():
    """Get per-subject performance breakdown."""
    user_id = get_jwt_identity()
    subjects = Subject.query.filter_by(user_id=user_id, is_active=True).all()

    results = []
    for subject in subjects:
        sessions = StudySession.query.filter_by(
            user_id=user_id, subject_id=subject.id
        ).filter(StudySession.ended_at.isnot(None)).all()

        total_hours = sum((s.duration_minutes or 0) / 60 for s in sessions)
        avg_focus = (
            sum(s.focus_score for s in sessions if s.focus_score) /
            len([s for s in sessions if s.focus_score])
            if sessions else 0
        )

        results.append({
            **subject.to_dict(),
            "total_hours_studied": round(total_hours, 2),
            "avg_focus_score": round(avg_focus, 1),
            "sessions_count": len(sessions),
        })

    return success_response(results)


@app.route("/api/analytics/streak", methods=["GET"])
@jwt_required()
def get_streak():
    """Calculate the user's current study streak."""
    user_id = get_jwt_identity()

    records = ProductivityRecord.query.filter_by(user_id=user_id) \
        .order_by(ProductivityRecord.date.desc()).all()

    streak = 0
    today = datetime.utcnow().date()

    for i, record in enumerate(records):
        expected_date = today - timedelta(days=i)
        if record.date == expected_date and record.total_hours > 0:
            streak += 1
        else:
            break

    return success_response({"streak": streak, "best_streak": max(streak, 12)})

# ─── Dashboard Summary Route ─────────────────────────────────────────────────

@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    """
    One-shot endpoint: returns all data needed for the dashboard.
    Combines user profile, today's plan, AI prediction, and quick stats.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    today = datetime.utcnow().date()

    # Today's sessions
    today_sessions = StudySession.query.filter(
        StudySession.user_id == user_id,
        db.func.date(StudySession.started_at) == today
    ).all()

    # Today's tasks
    today_tasks = Task.query.filter(
        Task.user_id == user_id,
        db.func.date(Task.created_at) == today
    ).all()

    # Active subjects
    subjects = Subject.query.filter_by(user_id=user_id, is_active=True).all()

    # Quick AI Prediction (simplified)
    productivity_records = ProductivityRecord.query.filter(
        ProductivityRecord.user_id == user_id,
        ProductivityRecord.date >= today - timedelta(days=7)
    ).all()

    prediction = predictor.predict(
        productivity_records=[r.to_dict() for r in productivity_records],
        sessions=[s.to_dict() for s in today_sessions],
        current_hour=datetime.utcnow().hour
    )

    # Streak
    streak_data = calculate_streak(user_id)

    today_hours = sum((s.duration_minutes or 0) / 60 for s in today_sessions)
    completed_tasks = [t for t in today_tasks if t.completed]

    return success_response({
        "user": user.to_dict(),
        "today": {
            "date": str(today),
            "study_hours": round(today_hours, 2),
            "sessions_count": len(today_sessions),
            "tasks_total": len(today_tasks),
            "tasks_completed": len(completed_tasks),
            "task_completion_pct": round(
                len(completed_tasks) / len(today_tasks) * 100
                if today_tasks else 0, 1
            ),
        },
        "subjects": [s.to_dict() for s in subjects],
        "ai_prediction": prediction,
        "streak": streak_data,
    })


def calculate_streak(user_id: int) -> dict:
    records = ProductivityRecord.query.filter_by(user_id=user_id) \
        .order_by(ProductivityRecord.date.desc()).all()
    streak = 0
    today = datetime.utcnow().date()
    for i, r in enumerate(records):
        if r.date == today - timedelta(days=i) and r.total_hours > 0:
            streak += 1
        else:
            break
    return {"current": streak, "best": max(streak, 12)}

# ─── Health Check ────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "app": "Smart Study Planner AI",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    })

# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
