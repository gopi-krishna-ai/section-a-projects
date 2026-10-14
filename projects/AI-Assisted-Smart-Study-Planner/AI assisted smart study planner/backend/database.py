"""
database.py — Database initialization and configuration.

Uses SQLAlchemy ORM with SQLite (default) or PostgreSQL (production).
"""

from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance — imported by app.py and models.py
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database:
    - Creates all tables if they don't exist.
    - Seeds initial demo data if the DB is empty.
    """
    with app.app_context():
        db.create_all()
        _seed_demo_data()
        print("✅ Database initialized successfully.")


def _seed_demo_data():
    """Seed the database with a demo student account for testing."""
    from models import User, Subject, Task, ProductivityRecord
    from datetime import datetime, timedelta
    import random

    # Skip seeding if data already exists
    if User.query.first():
        return

    print("🌱 Seeding demo data...")

    # Create demo user
    demo_user = User(name="Alex Johnson", email="demo@studyai.com")
    demo_user.set_password("demo1234")
    db.session.add(demo_user)
    db.session.flush()

    # Demo subjects
    demo_subjects = [
        {"name": "Mathematics",       "daily_hours": 4, "preferred_time": "18:00", "difficulty": "Hard",   "emoji": "📐", "color": "#4F8EF7"},
        {"name": "Physics",            "daily_hours": 3, "preferred_time": "08:00", "difficulty": "Hard",   "emoji": "⚛️", "color": "#7B61FF"},
        {"name": "Data Structures",    "daily_hours": 5, "preferred_time": "19:00", "difficulty": "Medium", "emoji": "💻", "color": "#10b981"},
        {"name": "English Literature", "daily_hours": 2, "preferred_time": "10:00", "difficulty": "Easy",   "emoji": "📚", "color": "#f59e0b"},
        {"name": "Chemistry",          "daily_hours": 3, "preferred_time": "16:00", "difficulty": "Medium", "emoji": "🔬", "color": "#ef4444"},
    ]

    subjects = []
    for s_data in demo_subjects:
        subject = Subject(user_id=demo_user.id, **s_data)
        db.session.add(subject)
        subjects.append(subject)

    db.session.flush()

    # Demo tasks for today
    demo_tasks = [
        {"title": "Complete Chapter 5 – Differential Equations", "duration": "2h",    "priority": "high",   "category": "Study",      "completed": True},
        {"title": "Solve 20 Physics problems from Module 3",      "duration": "1.5h",  "priority": "high",   "category": "Practice",   "completed": True},
        {"title": "Review Binary Tree algorithms",                 "duration": "1h",    "priority": "medium", "category": "Revision",   "completed": True},
        {"title": "Read Hamlet Act 2 & 3 with annotations",        "duration": "45m",   "priority": "medium", "category": "Reading",    "completed": False},
        {"title": "Write summary of Chemical Bonding",             "duration": "1h",    "priority": "low",    "category": "Study",      "completed": False},
        {"title": "Practice 10 Calculus integration problems",     "duration": "1.5h",  "priority": "high",   "category": "Practice",   "completed": False},
    ]

    for t_data in demo_tasks:
        task = Task(user_id=demo_user.id, subject_id=subjects[0].id, **t_data)
        if t_data["completed"]:
            task.completed_at = datetime.utcnow() - timedelta(hours=random.randint(1, 6))
        db.session.add(task)

    # Demo productivity records for last 7 days
    scores = [65, 72, 68, 78, 75, 85, 82]
    hours  = [3.5, 5.0, 2.5, 5.5, 4.0, 7.0, 4.5]
    for i, (score, hour) in enumerate(zip(scores, hours)):
        record = ProductivityRecord(
            user_id=demo_user.id,
            date=(datetime.utcnow() - timedelta(days=6 - i)).date(),
            productivity_score=score,
            total_hours=hour,
            sessions_count=random.randint(2, 5)
        )
        db.session.add(record)

    db.session.commit()
    print(f"✅ Demo user created: email=demo@studyai.com  password=demo1234")


def reset_db(app):
    """
    Drop all tables and reinitialize. USE CAREFULLY — only for development.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        _seed_demo_data()
        print("🔄 Database reset complete.")
