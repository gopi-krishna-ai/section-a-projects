from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth ---
class UserRegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    target_goal: Optional[str] = "FAANG & Competitive DSA"
    skill_level: Optional[str] = "intermediate"

class UserLoginRequest(BaseModel):
    username: str
    password: str

class SwitchDemoRequest(BaseModel):
    username: str

class UserProfileResponse(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    skill_level: str
    target_goal: str
    avatar: str

class AuthResponse(BaseModel):
    token: str
    user: UserProfileResponse

# --- Topics & Curriculum ---
class TopicSummary(BaseModel):
    id: str
    track: str
    level: str
    title: str
    description: str
    order_index: int
    icon: str
    total_problems: int = 0
    mastery_score: float = 0.0
    status: str = "not_started"

class LessonResponse(BaseModel):
    id: str
    topic_id: str
    title: str
    content: str
    runnable_snippets: List[Dict[str, Any]]
    key_takeaways: List[str]

# --- Problems & Code Execution ---
class TestCase(BaseModel):
    input: Any
    expected_output: Any
    is_hidden: bool = False
    explanation: Optional[str] = None

class ProblemSummary(BaseModel):
    id: str
    slug: str
    title: str
    topic_id: str
    track: str
    difficulty: str
    time_complexity: str
    space_complexity: str
    tags: List[str]
    has_attempted: bool = False
    is_solved: bool = False

class ProblemDetail(BaseModel):
    id: str
    slug: str
    title: str
    topic_id: str
    track: str
    difficulty: str
    description: str
    constraints: List[str]
    examples: List[Dict[str, Any]]
    starter_code: str
    time_complexity: str
    space_complexity: str
    hints: List[Dict[str, str]]
    visible_tests: List[Dict[str, Any]]
    tags: List[str]
    dry_run_steps: List[Dict[str, Any]]

class ExecuteCodeRequest(BaseModel):
    code: str
    stdin_input: Optional[str] = None

class ExecuteCodeResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: float
    error_type: Optional[str] = None

class TestResultItem(BaseModel):
    test_index: int
    input_str: str
    expected_output_str: str
    actual_output_str: Optional[str] = None
    passed: bool
    is_hidden: bool
    execution_time_ms: float
    error: Optional[str] = None

class SubmitSolutionRequest(BaseModel):
    code: str
    problem_id: str
    hints_used: int = 0
    solution_viewed: bool = False
    user_id: Optional[str] = None

class SubmitSolutionResponse(BaseModel):
    status: str # Passed, Failed, Runtime Error, Timeout
    passes_count: int
    total_tests: int
    execution_time_ms: float
    is_independent: bool
    test_results: List[TestResultItem]
    mistake_diagnosis: Optional[Dict[str, Any]] = None
    mastery_update: Optional[Dict[str, Any]] = None

# --- Mistake Notebook ---
class MistakeResponse(BaseModel):
    id: str
    problem_id: str
    problem_title: str
    topic_id: str
    error_category: str
    submitted_code: str
    failing_test_case: Optional[Dict[str, Any]] = None
    what_went_wrong: str
    why_it_went_wrong: str
    how_to_avoid: str
    retest_status: str
    created_at: datetime

class RetestMistakeRequest(BaseModel):
    code: str
    user_id: Optional[str] = None

class RetestMistakeResponse(BaseModel):
    mistake_id: str
    is_resolved: bool
    passes_count: int
    total_tests: int
    feedback: str

# --- Debug Lab ---
class DebugExerciseResponse(BaseModel):
    id: str
    title: str
    topic: str
    difficulty: str
    buggy_code: str
    bug_category: str
    description: str
    hint: str
    test_cases: List[Dict[str, Any]]

class DebugSubmitRequest(BaseModel):
    exercise_id: str
    code: str
    user_id: Optional[str] = None

class DebugSubmitResponse(BaseModel):
    is_fixed: bool
    stdout: str
    error: Optional[str] = None
    explanation: str

# --- Logic Gym ---
class LogicPuzzleResponse(BaseModel):
    id: str
    title: str
    category: str
    statement: str
    code_snippet: Optional[str] = None
    options: Optional[List[str]] = None
    reasoning_pattern: str

class LogicSubmitRequest(BaseModel):
    puzzle_id: str
    answer: str
    user_id: Optional[str] = None

class LogicSubmitResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str

# --- Spaced Revision ---
class RevisionItemResponse(BaseModel):
    id: str
    problem_id: str
    problem_title: str
    difficulty: str
    topic_title: str
    interval_days: int
    repetition_number: int
    due_at: datetime

# --- Dashboard & Analytics ---
class DashboardResponse(BaseModel):
    total_problems_in_bank: int
    total_attempted: int
    total_solved: int
    independent_solved: int
    independent_accuracy: float
    overall_accuracy: float
    streak_days: int
    active_topics: List[Dict[str, Any]]
    topics_needing_focus: List[Dict[str, Any]]
    top_mistake_patterns: List[Dict[str, Any]]
    due_revisions_count: int
    recent_submissions: List[Dict[str, Any]]
    recommended_next_task: Optional[Dict[str, Any]] = None
