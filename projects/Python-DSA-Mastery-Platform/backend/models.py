import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from backend.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(60), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=True)
    full_name = Column(String(120), nullable=True)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(64), nullable=False)
    skill_level = Column(String(50), default="intermediate") # intermediate, advanced
    target_goal = Column(String(100), default="FAANG & Competitive DSA")
    avatar = Column(String(10), default="PY")
    preferences = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

    submissions = relationship("ProblemSubmission", back_populates="user", cascade="all, delete-orphan")
    mistakes = relationship("MistakeRecord", back_populates="user", cascade="all, delete-orphan")
    masteries = relationship("TopicMastery", back_populates="user", cascade="all, delete-orphan")
    revisions = relationship("RevisionSchedule", back_populates="user", cascade="all, delete-orphan")
    debug_submissions = relationship("DebugSubmission", back_populates="user", cascade="all, delete-orphan")
    logic_submissions = relationship("LogicSubmission", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(100), primary_key=True) # e.g. py_comprehensions, dsa_arrays_strings
    track = Column(String(50), nullable=False, index=True) # python, dsa, logic, projects
    level = Column(String(50), nullable=False) # Level 1, Level 2, Level 3, Stage 1-13
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    prerequisites = Column(JSON, default=list) # list of topic ids
    icon = Column(String(50), default="Code")

    lessons = relationship("Lesson", back_populates="topic", cascade="all, delete-orphan")
    problems = relationship("Problem", back_populates="topic", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    runnable_snippets = Column(JSON, default=list) # [{title, code, output, explanation}]
    key_takeaways = Column(JSON, default=list)
    order_index = Column(Integer, default=0)

    topic = relationship("Topic", back_populates="lessons")

class Problem(Base):
    __tablename__ = "problems"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    title = Column(String(150), nullable=False)
    topic_id = Column(String(100), ForeignKey("topics.id"), nullable=False, index=True)
    track = Column(String(50), default="dsa", index=True)
    difficulty = Column(String(20), nullable=False, index=True) # Easy, Medium, Hard
    description = Column(Text, nullable=False)
    constraints = Column(JSON, default=list)
    examples = Column(JSON, default=list) # [{input, output, explanation}]
    starter_code = Column(Text, nullable=False)
    reference_solution = Column(Text, nullable=False)
    brute_force_solution = Column(Text, nullable=True)
    time_complexity = Column(String(50), default="O(N)")
    space_complexity = Column(String(50), default="O(1)")
    hints = Column(JSON, default=list) # [Hint 1 - Clarify, ..., Hint 6 - Full Solution]
    test_cases = Column(JSON, default=list) # [{input, expected_output, is_hidden, explanation}]
    tags = Column(JSON, default=list) # ['two_pointers', 'sliding_window']
    dry_run_steps = Column(JSON, default=list) # [{step: 1, explanation: '...', state: {...}}]
    created_at = Column(DateTime, default=utc_now)

    topic = relationship("Topic", back_populates="problems")
    submissions = relationship("ProblemSubmission", back_populates="problem", cascade="all, delete-orphan")
    mistakes = relationship("MistakeRecord", back_populates="problem", cascade="all, delete-orphan")
    revisions = relationship("RevisionSchedule", back_populates="problem", cascade="all, delete-orphan")

class ProblemSubmission(Base):
    __tablename__ = "problem_submissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    code = Column(Text, nullable=False)
    status = Column(String(50), nullable=False) # Passed, Failed, Runtime Error, Timeout
    passes_count = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    execution_time_ms = Column(Float, default=0.0)
    is_independent = Column(Boolean, default=True) # false if hints used or solution viewed
    hints_used = Column(Integer, default=0)
    solution_viewed = Column(Boolean, default=False)
    error_output = Column(Text, nullable=True)
    failing_test_case = Column(JSON, nullable=True)
    submitted_at = Column(DateTime, default=utc_now, index=True)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

class MistakeRecord(Base):
    __tablename__ = "mistake_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    submission_id = Column(String(36), nullable=True)
    error_category = Column(String(100), nullable=False) # 22 mistake taxonomies
    submitted_code = Column(Text, nullable=False)
    failing_test_case = Column(JSON, nullable=True)
    what_went_wrong = Column(Text, nullable=False)
    why_it_went_wrong = Column(Text, nullable=False)
    how_to_avoid = Column(Text, nullable=False)
    corrective_exercise = Column(JSON, nullable=True)
    retest_status = Column(String(30), default="pending") # pending, resolved
    created_at = Column(DateTime, default=utc_now, index=True)

    user = relationship("User", back_populates="mistakes")
    problem = relationship("Problem", back_populates="mistakes")

class TopicMastery(Base):
    __tablename__ = "topic_mastery"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    topic_id = Column(String(100), nullable=False, index=True)
    mastery_score = Column(Float, default=0.0) # 0.0 to 100.0
    status = Column(String(50), default="not_started") # not_started, learning, practising, needs_revision, developing_independence, proficient, mastered
    total_attempted = Column(Integer, default=0)
    independent_solved = Column(Integer, default=0)
    assisted_solved = Column(Integer, default=0)
    last_practiced_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="masteries")

class RevisionSchedule(Base):
    __tablename__ = "revision_schedules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    problem_id = Column(String(36), ForeignKey("problems.id"), nullable=False, index=True)
    interval_days = Column(Integer, default=1)
    repetition_number = Column(Integer, default=1)
    ease_factor = Column(Float, default=2.5)
    due_at = Column(DateTime, nullable=False, index=True)
    review_status = Column(String(30), default="pending") # pending, completed
    last_reviewed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="revisions")
    problem = relationship("Problem", back_populates="revisions")

class DebugExercise(Base):
    __tablename__ = "debug_exercises"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(150), nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), default="Medium")
    buggy_code = Column(Text, nullable=False)
    bug_category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    test_cases = Column(JSON, default=list)
    hint = Column(Text, nullable=False)
    fixed_code = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)

class DebugSubmission(Base):
    __tablename__ = "debug_submissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(String(36), ForeignKey("debug_exercises.id"), nullable=False, index=True)
    submitted_code = Column(Text, nullable=False)
    is_fixed = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="debug_submissions")

class LogicPuzzle(Base):
    __tablename__ = "logic_puzzles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False) # loop_trace, output_pred, counterexample, invariant, deduction
    statement = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    options = Column(JSON, nullable=True) # MCQ choices if applicable
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    reasoning_pattern = Column(String(150), nullable=False)

class LogicSubmission(Base):
    __tablename__ = "logic_submissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    puzzle_id = Column(String(36), ForeignKey("logic_puzzles.id"), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="logic_submissions")
