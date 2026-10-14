from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models import MistakeRecord, Question, Topic, QuestionAttempt
from backend.schemas import MistakeResponse, RetestMistakeRequest
from backend.services.evaluator import evaluate_answer
from backend.services.mastery import calculate_topic_mastery

router = APIRouter(prefix="/api/mistakes", tags=["Mistake Notebook"])

@router.get("", response_model=List[MistakeResponse])
def get_mistakes(
    user_id: str = "default_user",
    topic_id: Optional[str] = None,
    error_category: Optional[str] = None,
    retest_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = (
        db.query(MistakeRecord)
        .join(Question, MistakeRecord.question_id == Question.id)
        .join(Topic, MistakeRecord.topic_id == Topic.id)
        .filter(MistakeRecord.user_id == user_id)
    )

    if topic_id:
        query = query.filter(MistakeRecord.topic_id == topic_id)
    if error_category:
        query = query.filter(MistakeRecord.error_category == error_category)
    if retest_status:
        query = query.filter(MistakeRecord.retest_status == retest_status)

    mistakes = query.order_by(MistakeRecord.created_at.desc()).offset(skip).limit(limit).all()

    results = []
    for m in mistakes:
        q = db.query(Question).filter_by(id=m.question_id).first()
        t = db.query(Topic).filter_by(id=m.topic_id).first()
        att = db.query(QuestionAttempt).filter_by(id=m.attempt_id).first()

        results.append(MistakeResponse(
            id=m.id,
            attempt_id=m.attempt_id,
            question_id=m.question_id,
            topic_id=m.topic_id,
            topic_name=t.name if t else "General",
            category=t.category if t else "Quantitative Aptitude",
            question_text=q.question_text if q else "Question text unavailable",
            submitted_answer=att.submitted_answer if att else "",
            correct_answer=q.correct_answer if q else "",
            error_category=m.error_category,
            what_went_wrong=m.what_went_wrong,
            why_it_went_wrong=m.why_it_went_wrong,
            correct_reasoning=m.correct_reasoning,
            how_to_avoid=m.how_to_avoid,
            corrective_exercise=m.corrective_exercise,
            retest_status=m.retest_status,
            created_at=m.created_at
        ))

    return results

@router.post("/{mistake_id}/retest")
def retest_mistake(
    mistake_id: str,
    payload: RetestMistakeRequest,
    db: Session = Depends(get_db)
):
    m = db.query(MistakeRecord).filter_by(id=mistake_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mistake record not found")

    q = db.query(Question).filter_by(id=m.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    eval_result = evaluate_answer(
        submitted=payload.submitted_answer,
        correct=q.correct_answer,
        question_type=q.question_type,
        options=q.options
    )

    is_correct = eval_result["is_correct"]
    m.retest_status = "retested_passed" if is_correct else "retested_failed"

    # Record retest attempt
    retest_att = QuestionAttempt(
        user_id=payload.user_id,
        question_id=q.id,
        submitted_answer=payload.submitted_answer,
        is_correct=is_correct,
        hints_used=0,
        time_spent=payload.time_spent,
        attempted_at=datetime.utcnow()
    )
    db.add(retest_att)
    db.commit()

    # Update Topic Mastery
    calculate_topic_mastery(db, payload.user_id, q.topic_id)

    return {
        "mistake_id": m.id,
        "is_correct": is_correct,
        "feedback": eval_result["feedback"],
        "new_retest_status": m.retest_status
    }
