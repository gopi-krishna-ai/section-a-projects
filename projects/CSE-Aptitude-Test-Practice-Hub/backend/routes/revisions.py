from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from backend.database import get_db
from backend.models import RevisionSchedule, Question, Topic, QuestionAttempt
from backend.schemas import RevisionItemResponse, CompleteRevisionRequest
from backend.services.evaluator import evaluate_answer
from backend.services.mastery import schedule_spaced_revision

router = APIRouter(prefix="/api/revisions", tags=["Spaced Revision"])

@router.get("/due", response_model=List[RevisionItemResponse])
def get_due_revisions(user_id: str = "default_user", db: Session = Depends(get_db)):
    revisions = (
        db.query(RevisionSchedule)
        .filter(RevisionSchedule.user_id == user_id, RevisionSchedule.review_status == "pending")
        .order_by(RevisionSchedule.due_at.asc())
        .limit(30)
        .all()
    )

    results = []
    for r in revisions:
        q = db.query(Question).filter_by(id=r.question_id).first()
        t = db.query(Topic).filter_by(id=r.topic_id).first()
        if q:
            results.append(RevisionItemResponse(
                id=r.id,
                question_id=q.id,
                topic_id=r.topic_id,
                topic_name=t.name if t else "General",
                category=t.category if t else "Quantitative Aptitude",
                question_text=q.question_text,
                stimulus_context=q.stimulus_context,
                options=q.options,
                due_at=r.due_at,
                interval_days=r.interval_days,
                repetition_number=r.repetition_number,
                review_status=r.review_status
            ))

    return results

@router.post("/{revision_id}/review")
def review_revision_item(
    revision_id: str,
    payload: CompleteRevisionRequest,
    db: Session = Depends(get_db)
):
    rev = db.query(RevisionSchedule).filter_by(id=revision_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revision schedule not found")

    q = db.query(Question).filter_by(id=rev.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    eval_result = evaluate_answer(
        submitted=payload.submitted_answer,
        correct=q.correct_answer,
        question_type=q.question_type,
        options=q.options
    )

    is_correct = eval_result["is_correct"]

    # Re-schedule interval
    schedule_spaced_revision(db, payload.user_id, q.id, q.topic_id, is_correct)

    return {
        "revision_id": rev.id,
        "is_correct": is_correct,
        "feedback": eval_result["feedback"],
        "correct_answer": q.correct_answer,
        "reference_solution": q.reference_solution
    }
