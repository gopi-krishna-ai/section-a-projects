from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from backend.database import get_db
from backend.models import RevisionSchedule, Problem, Topic
from backend.schemas import RevisionItemResponse

router = APIRouter(prefix="/api/revisions", tags=["Spaced Revision"])

@router.get("/due", response_model=List[RevisionItemResponse])
def get_due_revisions(user_id: str = "default_user", db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    revisions = (
        db.query(RevisionSchedule)
        .filter(RevisionSchedule.user_id == user_id, RevisionSchedule.review_status == "pending")
        .all()
    )

    results = []
    for r in revisions:
        p = db.query(Problem).filter_by(id=r.problem_id).first()
        if p:
            t = db.query(Topic).filter_by(id=p.topic_id).first()
            results.append(RevisionItemResponse(
                id=r.id,
                problem_id=p.id,
                problem_title=p.title,
                difficulty=p.difficulty,
                topic_title=t.title if t else "General",
                interval_days=r.interval_days,
                repetition_number=r.repetition_number,
                due_at=r.due_at
            ))
    return results

@router.post("/{revision_id}/complete")
def complete_revision(revision_id: str, db: Session = Depends(get_db)):
    r = db.query(RevisionSchedule).filter_by(id=revision_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Revision schedule not found")
    r.review_status = "completed"
    r.last_reviewed_at = datetime.now(timezone.utc)
    db.commit()
    return {"message": "Revision marked as completed"}
