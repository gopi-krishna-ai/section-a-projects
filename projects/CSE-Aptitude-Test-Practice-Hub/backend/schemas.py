from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TopicBase(BaseModel):
    id: str
    name: str
    category: str
    parent_topic_id: Optional[str] = None
    description: Optional[str] = ""
    prerequisites: List[str] = []
    icon: Optional[str] = "BookOpen"
    order_index: int = 0

class TopicResponse(TopicBase):
    total_questions: int = 0
    mastery_score: float = 0.0
    status: str = "not_started"
    unassisted_accuracy: float = 0.0

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: str
    source_id: str
    source_file: str
    category: str
    topic_id: str
    subtopic_name: str
    level: str
    stimulus_context: Optional[str] = None
    question_text: str
    question_type: str
    options: Optional[List[str]] = None
    difficulty: float
    hints: List[str] = []
    formula_reference: Optional[str] = None
    is_bookmarked: bool = False

    class Config:
        from_attributes = True

class QuestionDetailResponse(QuestionResponse):
    correct_answer: Optional[str] = None
    reference_solution: Optional[str] = None

class SubmitAnswerRequest(BaseModel):
    user_id: str = "default_user"
    submitted_answer: str
    time_spent: float = 0.0
    hints_used: int = 0
    session_id: Optional[str] = None
    scratchpad_notes: Optional[str] = None

class SubmitAnswerResponse(BaseModel):
    is_correct: bool
    submitted_answer: str
    correct_answer: str
    reference_solution: str
    match_type: str
    feedback: str
    attempt_id: str
    hints_used: int
    error_diagnosis: Optional[Dict[str, Any]] = None
    mastery_update: Optional[Dict[str, Any]] = None

class ProgressiveHintRequest(BaseModel):
    hint_level: int = 1
    current_attempt: Optional[str] = None

class ProgressiveHintResponse(BaseModel):
    hint_level: int
    title: str
    content: str
    educational_takeaway: Optional[str] = None
    correct_answer: Optional[str] = None

class StepGuidanceRequest(BaseModel):
    step_name: str # understand, identify, plan, solve, verify, generalize, transfer

class StepGuidanceResponse(BaseModel):
    step: str
    title: str
    content: str
    guiding_question: Optional[str] = None

class AskTutorRequest(BaseModel):
    query: str

class AskTutorResponse(BaseModel):
    provider: str
    explanation: str
    source: str

class BookmarkToggleRequest(BaseModel):
    user_id: str = "default_user"
    notes: Optional[str] = None

class BookmarkResponse(BaseModel):
    is_bookmarked: bool
    notes: Optional[str] = None

class MistakeResponse(BaseModel):
    id: str
    attempt_id: str
    question_id: str
    topic_id: str
    topic_name: str
    category: str
    question_text: str
    submitted_answer: str
    correct_answer: str
    error_category: str
    what_went_wrong: str
    why_it_went_wrong: str
    correct_reasoning: str
    how_to_avoid: str
    corrective_exercise: Optional[Dict[str, Any]] = None
    retest_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class RetestMistakeRequest(BaseModel):
    user_id: str = "default_user"
    submitted_answer: str
    time_spent: float = 0.0

class RevisionItemResponse(BaseModel):
    id: str
    question_id: str
    topic_id: str
    topic_name: str
    category: str
    question_text: str
    stimulus_context: Optional[str] = None
    options: Optional[List[str]] = None
    due_at: datetime
    interval_days: int
    repetition_number: int
    review_status: str

class CompleteRevisionRequest(BaseModel):
    user_id: str = "default_user"
    submitted_answer: str

class StartSessionRequest(BaseModel):
    user_id: str = "default_user"
    topic_id: Optional[str] = None
    mode: str = "topic" # topic, guided, independent, weakness, mixed, timed, challenge, revision, exam
    num_questions: int = 10
    level: Optional[str] = None # Basic, Intermediate, Advanced
    meta_info: Optional[Dict[str, Any]] = None

class SessionResponse(BaseModel):
    session_id: str
    mode: str
    topic_id: Optional[str] = None
    total_questions: int
    questions: List[QuestionResponse]

class ConceptLessonResponse(BaseModel):
    id: str
    topic_id: str
    category: str
    title: str
    concept_summary: str
    why_needed: str
    simple_explanation: str
    real_world_example: str
    intuition: str
    important_terms: List[Dict[str, str]] = []
    formulas: List[Dict[str, str]] = []
    step_by_step_example: Dict[str, Any] = {}
    placement_example: Dict[str, Any] = {}
    common_traps: List[str] = []
    key_takeaways: List[str] = []

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    total_repository_questions: int
    total_attempted_unique: int
    total_solved_correct: int
    overall_accuracy: float
    unassisted_accuracy: float
    current_studying_topics: List[Dict[str, Any]]
    topics_needing_improvement: List[Dict[str, Any]]
    top_repeated_mistakes: List[Dict[str, Any]]
    due_revisions_count: int
    recent_attempts: List[Dict[str, Any]]
    recommended_next_lesson: Optional[Dict[str, Any]] = None
