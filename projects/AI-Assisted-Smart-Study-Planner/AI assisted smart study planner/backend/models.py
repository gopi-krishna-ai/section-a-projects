"""
models.py — SQLAlchemy ORM models for the Smart Study Planner.

Models:
  - User            : Student accounts
  - Subject         : Study subjects/courses
  - StudySession    : Individual timed study sessions
  - Task            : To-do tasks per subject
  - ProductivityRecord : Daily AI-computed productivity scores
"""

from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    """Student user account."""

    __tablename__ = "users"

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(100), nullable=False)
    email           = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash   = db.Column(db.String(256), nullable=False)
    university      = db.Column(db.String(200))
    daily_goal_hrs  = db.Column(db.Float, default=6.0)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    last_login      = db.Column(db.DateTime)
    is_active       = db.Column(db.Boolean, default=True)

    # Relationships
    subjects             = db.relationship("Subject",           backref="user", lazy=True, cascade="all,delete-orphan")
    study_sessions       = db.relationship("StudySession",      backref="user", lazy=True, cascade="all,delete-orphan")
    tasks                = db.relationship("Task",              backref="user", lazy=True, cascade="all,delete-orphan")
    productivity_records = db.relationship("ProductivityRecord", backref="user", lazy=True, cascade="all,delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id":             self.id,
            "name":           self.name,
            "email":          self.email,
            "university":     self.university,
            "daily_goal_hrs": self.daily_goal_hrs,
            "created_at":     self.created_at.isoformat() if self.created_at else None,
            "last_login":     self.last_login.isoformat() if self.last_login else None,
        }

    def __repr__(self):
        return f"<User {self.email}>"


class Subject(db.Model):
    """A student's study subject or course."""

    __tablename__ = "subjects"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name           = db.Column(db.String(150), nullable=False)
    daily_hours    = db.Column(db.Float, default=2.0)
    preferred_time = db.Column(db.String(10), default="18:00")   # "HH:MM" format
    difficulty     = db.Column(db.String(10), default="Medium")  # Easy / Medium / Hard
    emoji          = db.Column(db.String(10), default="📚")
    color          = db.Column(db.String(10), default="#4F8EF7")
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    study_sessions = db.relationship("StudySession", backref="subject", lazy=True)
    tasks          = db.relationship("Task",          backref="subject", lazy=True)

    def to_dict(self) -> dict:
        return {
            "id":             self.id,
            "user_id":        self.user_id,
            "name":           self.name,
            "daily_hours":    self.daily_hours,
            "preferred_time": self.preferred_time,
            "difficulty":     self.difficulty,
            "emoji":          self.emoji,
            "color":          self.color,
            "is_active":      self.is_active,
            "created_at":     self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Subject {self.name}>"


class StudySession(db.Model):
    """
    A timed study session linked to a subject.
    Tracks start/end times, duration, and focus score.
    """

    __tablename__ = "study_sessions"

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id       = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    started_at       = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ended_at         = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)        # calculated on session end
    focus_score      = db.Column(db.Integer)        # 0-100, user-reported or auto
    notes            = db.Column(db.Text)
    is_active        = db.Column(db.Boolean, default=True)

    def to_dict(self) -> dict:
        return {
            "id":               self.id,
            "user_id":          self.user_id,
            "subject_id":       self.subject_id,
            "started_at":       self.started_at.isoformat() if self.started_at else None,
            "ended_at":         self.ended_at.isoformat() if self.ended_at else None,
            "duration_minutes": self.duration_minutes,
            "focus_score":      self.focus_score,
            "notes":            self.notes,
            "is_active":        self.is_active,
            "hour_of_day":      self.started_at.hour if self.started_at else None,
        }

    def __repr__(self):
        return f"<StudySession {self.id} user={self.user_id}>"


class Task(db.Model):
    """
    An individual study task (to-do item) for a student.
    Can be linked to a subject or standalone.
    """

    __tablename__ = "tasks"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id   = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True)
    title        = db.Column(db.String(300), nullable=False)
    duration     = db.Column(db.String(10), default="1h")       # "1h", "30m", etc.
    priority     = db.Column(db.String(10), default="medium")   # high / medium / low
    category     = db.Column(db.String(50), default="Study")    # Study / Practice / Revision
    completed    = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    due_date     = db.Column(db.Date)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "user_id":      self.user_id,
            "subject_id":   self.subject_id,
            "title":        self.title,
            "duration":     self.duration,
            "priority":     self.priority,
            "category":     self.category,
            "completed":    self.completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "due_date":     str(self.due_date) if self.due_date else None,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Task {self.title[:30]}>"


class ProductivityRecord(db.Model):
    """
    Daily AI-computed productivity record for a user.
    Aggregates study quality metrics per day.
    """

    __tablename__ = "productivity_records"

    id                 = db.Column(db.Integer, primary_key=True)
    user_id            = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    date               = db.Column(db.Date, nullable=False)
    productivity_score = db.Column(db.Float, default=0.0)  # 0.0 – 100.0
    total_hours        = db.Column(db.Float, default=0.0)
    sessions_count     = db.Column(db.Integer, default=0)
    notes              = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("user_id", "date", name="uq_user_date"),
    )

    def to_dict(self) -> dict:
        return {
            "id":                 self.id,
            "user_id":            self.user_id,
            "date":               str(self.date),
            "productivity_score": self.productivity_score,
            "total_hours":        self.total_hours,
            "sessions_count":     self.sessions_count,
        }

    def __repr__(self):
        return f"<ProductivityRecord {self.date} user={self.user_id} score={self.productivity_score}>"
