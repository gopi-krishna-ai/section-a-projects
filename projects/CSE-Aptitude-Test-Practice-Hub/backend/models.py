import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, JSON, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from backend.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False, default="learner")
    email = Column(String(150), nullable=True)
    full_name = Column(String(150), nullable=True)
    password_hash = Column(String(255), nullable=True)
    salt = Column(String(64), nullable=True)
    target_company = Column(String(100), default="TCS / Infosys")
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    attempts = relationship("QuestionAttempt", back_populates="user", cascade="all, delete-orphan")
    masteries = relationship("TopicMastery", back_populates="user", cascade="all, delete-orphan")
    mistakes = relationship("MistakeRecord", back_populates="user", cascade="all, delete-orphan")
    revisions = relationship("RevisionSchedule", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("LearningSession", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(100), primary_key=True) # e.g. "percentages", "series"
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False) # e.g. "Quantitative Aptitude"
    parent_topic_id = Column(String(100), ForeignKey("topics.id"), nullable=True)
    description = Column(Text, default="")
    prerequisites = Column(JSON, default=list) # List of topic IDs
    icon = Column(String(50), default="BookOpen")
    order_index = Column(Integer, default=0)

    questions = relationship("Question", back_populates="topic")
    masteries = relationship("TopicMastery", back_populates="topic")
    lesson = relationship("ConceptLesson", back_populates="topic", uselist=False)

class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(120), unique=True, nullable=False, index=True)
    source_file = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    subtopic_name = Column(String(150), nullable=False)
    level = Column(String(50), nullable=False, index=True) # Basic, Intermediate, Advanced
    stimulus_context = Column(Text, nullable=True) # Tables, Passages, Charts
    question_text = Column(Text, nullable=False)
    raw_question = Column(Text, nullable=True)
    question_type = Column(String(50), default="short_answer") # mcq, numeric, text_correction, short_answer
    options = Column(JSON, nullable=True) # list of option strings e.g. ["A) ...", "B) ..."]
    correct_answer = Column(Text, nullable=False)
    reference_solution = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Float, default=1.0) # 1.0 (Basic), 2.0 (Intermediate), 3.0 (Advanced)
    provenance = Column(String(100), default="original_repository")
    validation_status = Column(String(50), default="verified") # verified, flagged_review
    hints = Column(JSON, default=list) # 3 progressive hint strings
    formula_reference = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="questions")
    attempts = relationship("QuestionAttempt", back_populates="question")
    bookmarks = relationship("Bookmark", back_populates="question")
    revisions = relationship("RevisionSchedule", back_populates="question")

class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=True)
    mode = Column(String(50), nullable=False) # topic, guided, independent, weakness, mixed, timed, challenge, revision, exam
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    meta_info = Column(JSON, default=dict) # e.g. time_limit, company_profile

    user = relationship("User", back_populates="sessions")
    attempts = relationship("QuestionAttempt", back_populates="session")

class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    session_id = Column(String(36), ForeignKey("learning_sessions.id"), nullable=True, index=True)
    submitted_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    hints_used = Column(Integer, default=0)
    time_spent = Column(Float, default=0.0) # seconds
    error_category = Column(String(100), nullable=True) # 12 taxonomies
    scratchpad_notes = Column(Text, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")
    session = relationship("LearningSession", back_populates="attempts")
    mistake = relationship("MistakeRecord", back_populates="attempt", uselist=False)

class TopicMastery(Base):
    __tablename__ = "topic_mastery"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0) # 0 to 100
    status = Column(String(50), default="not_started") # not_started, learning, needs_practice, improving, proficient, needs_revision
    total_attempted = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    unassisted_correct = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="masteries")
    topic = relationship("Topic", back_populates="masteries")

class MistakeRecord(Base):
    __tablename__ = "mistake_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    attempt_id = Column(String(36), ForeignKey("question_attempts.id"), nullable=False, unique=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    error_category = Column(String(100), nullable=False)
    what_went_wrong = Column(Text, nullable=False)
    why_it_went_wrong = Column(Text, nullable=False)
    correct_reasoning = Column(Text, nullable=False)
    how_to_avoid = Column(Text, nullable=False)
    corrective_exercise = Column(JSON, nullable=True) # Small practice check
    retest_status = Column(String(50), default="pending") # pending, retested_passed, retested_failed
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    attempt = relationship("QuestionAttempt", back_populates="mistake")
    user = relationship("User", back_populates="mistakes")

class RevisionSchedule(Base):
    __tablename__ = "revision_schedules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    interval_days = Column(Integer, default=1) # 1, 3, 7, 14
    repetition_number = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    due_at = Column(DateTime, nullable=False, index=True)
    review_status = Column(String(50), default="pending") # pending, completed, dismissed
    last_reviewed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="revisions")
    question = relationship("Question", back_populates="revisions")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")
    question = relationship("Question", back_populates="bookmarks")

class ConceptLesson(Base):
    __tablename__ = "concept_lessons"

    id = Column(String(100), primary_key=True) # same as topic_id
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    title = Column(String(150), nullable=False)
    concept_summary = Column(Text, nullable=False)
    why_needed = Column(Text, nullable=False)
    simple_explanation = Column(Text, nullable=False)
    real_world_example = Column(Text, nullable=False)
    intuition = Column(Text, nullable=False)
    important_terms = Column(JSON, default=list) # [{term: str, definition: str}]
    formulas = Column(JSON, default=list) # [{name: str, formula: str, why_works: str, when_to_use: str}]
    step_by_step_example = Column(JSON, default=dict) # {question: str, steps: list[str], solution: str}
    placement_example = Column(JSON, default=dict) # {question: str, approach: str, solution: str, trap: str}
    common_traps = Column(JSON, default=list) # [str]
    key_takeaways = Column(JSON, default=list) # [str]

    topic = relationship("Topic", back_populates="lesson")
