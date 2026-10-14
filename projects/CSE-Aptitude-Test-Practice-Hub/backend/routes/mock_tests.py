from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.database import get_db
from backend.models import Question, Topic, LearningSession, QuestionAttempt
from backend.services.evaluator import evaluate_answer
from backend.services.diagnosis import diagnose_mistake

router = APIRouter(prefix="/api/mock_tests", tags=["Mock Tests"])

COMPANY_PROFILES = {
    "tcs_nqt": {
        "name": "TCS NQT Style Assessment",
        "description": "Standard numerical and reasoning section with 20 questions and 25-minute timer.",
        "question_count": 20,
        "time_limit_minutes": 25,
        "categories": ["Quantitative Aptitude", "Logical Reasoning", "Verbal Ability"],
        "level_distribution": {"Basic": 8, "Intermediate": 9, "Advanced": 3}
    },
    "infosys_sp": {
        "name": "Infosys Specialist Prep",
        "description": "Heavy on mathematical reasoning, data interpretation, and technical logic.",
        "question_count": 15,
        "time_limit_minutes": 20,
        "categories": ["Quantitative Aptitude", "Logical Reasoning", "Technical Aptitude"],
        "level_distribution": {"Basic": 4, "Intermediate": 7, "Advanced": 4}
    },
    "accenture_cognitive": {
        "name": "Accenture Cognitive Assessment",
        "description": "Focus on verbal comprehension, abstract reasoning, and critical thinking.",
        "question_count": 20,
        "time_limit_minutes": 20,
        "categories": ["Verbal Ability", "Abstract Reasoning", "Data Interpretation and Analysis"],
        "level_distribution": {"Basic": 10, "Intermediate": 8, "Advanced": 2}
    }
}

class StartMockTestRequest(BaseModel):
    user_id: str = "default_user"
    profile_id: Optional[str] = "tcs_nqt"
    custom_categories: Optional[List[str]] = None
    question_count: int = 15
    time_limit_minutes: int = 20

class SubmitMockTestItem(BaseModel):
    question_id: str
    submitted_answer: str
    time_spent: float = 0.0
    is_marked_for_review: bool = False

class SubmitMockTestRequest(BaseModel):
    user_id: str = "default_user"
    session_id: str
    answers: List[SubmitMockTestItem]

@router.get("/profiles")
def get_company_profiles():
    return COMPANY_PROFILES

@router.post("/start")
def start_mock_test(payload: StartMockTestRequest, db: Session = Depends(get_db)):
    profile = COMPANY_PROFILES.get(payload.profile_id)
    if profile:
        cats = profile["categories"]
        count = profile["question_count"]
        time_limit = profile["time_limit_minutes"]
    else:
        cats = payload.custom_categories or ["Quantitative Aptitude", "Logical Reasoning"]
        count = max(5, min(payload.question_count, 40))
        time_limit = max(5, payload.time_limit_minutes)

    # Pick balanced questions across selected categories
    questions = (
        db.query(Question)
        .filter(Question.category.in_(cats))
        .order_by(func.random())
        .limit(count)
        .all()
    )

    session = LearningSession(
        user_id=payload.user_id,
        mode="exam",
        started_at=datetime.utcnow(),
        total_questions=len(questions),
        meta_info={"profile_id": payload.profile_id, "time_limit_minutes": time_limit}
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Return test questions (WITHOUT solutions/answers)
    q_list = []
    for idx, q in enumerate(questions, 1):
        q_list.append({
            "test_index": idx,
            "id": q.id,
            "category": q.category,
            "subtopic_name": q.subtopic_name,
            "level": q.level,
            "stimulus_context": q.stimulus_context,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options
        })

    return {
        "session_id": session.id,
        "title": profile["name"] if profile else "Custom Placement Mock Test",
        "time_limit_seconds": time_limit * 60,
        "total_questions": len(q_list),
        "questions": q_list
    }

@router.post("/submit")
def submit_mock_test(payload: SubmitMockTestRequest, db: Session = Depends(get_db)):
    session = db.query(LearningSession).filter_by(id=payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Exam session not found")

    session.completed_at = datetime.utcnow()

    score = 0
    total = len(payload.answers)
    question_results = []
    category_breakdown = {}

    for item in payload.answers:
        q = db.query(Question).filter_by(id=item.question_id).first()
        if not q:
            continue

        eval_res = evaluate_answer(
            submitted=item.submitted_answer,
            correct=q.correct_answer,
            question_type=q.question_type,
            options=q.options
        )
        is_correct = eval_res["is_correct"]
        if is_correct:
            score += 1

        # Track category performance
        cat = q.category
        if cat not in category_breakdown:
            category_breakdown[cat] = {"total": 0, "correct": 0}
        category_breakdown[cat]["total"] += 1
        if is_correct:
            category_breakdown[cat]["correct"] += 1

        # Record attempt
        diag = None
        if not is_correct and item.submitted_answer:
            diag = diagnose_mistake(
                question_text=q.question_text,
                submitted_answer=item.submitted_answer,
                correct_answer=q.correct_answer,
                reference_solution=q.reference_solution,
                category=q.category,
                time_spent=item.time_spent
            )

        att = QuestionAttempt(
            user_id=payload.user_id,
            question_id=q.id,
            session_id=session.id,
            submitted_answer=item.submitted_answer,
            is_correct=is_correct,
            hints_used=0,
            time_spent=item.time_spent,
            error_category=diag["error_category"] if diag else None,
            attempted_at=datetime.utcnow()
        )
        db.add(att)

        question_results.append({
            "question_id": q.id,
            "category": q.category,
            "question_text": q.question_text,
            "submitted_answer": item.submitted_answer,
            "correct_answer": q.correct_answer,
            "reference_solution": q.reference_solution,
            "is_correct": is_correct,
            "time_spent": item.time_spent,
            "error_diagnosis": diag
        })

    session.score = score
    db.commit()

    accuracy = round((score / total * 100.0), 1) if total > 0 else 0.0

    return {
        "session_id": session.id,
        "score": score,
        "total_questions": total,
        "accuracy": accuracy,
        "category_breakdown": category_breakdown,
        "question_results": question_results
    }
