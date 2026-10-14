from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from backend.database import get_db
from backend.models import LogicPuzzle, LogicSubmission
from backend.schemas import LogicPuzzleResponse, LogicSubmitRequest, LogicSubmitResponse

router = APIRouter(prefix="/api/logic_gym", tags=["Logical Thinking Gym"])

@router.get("", response_model=List[LogicPuzzleResponse])
def list_logic_puzzles(db: Session = Depends(get_db)):
    puzzles = db.query(LogicPuzzle).all()
    return [
        LogicPuzzleResponse(
            id=p.id,
            title=p.title,
            category=p.category,
            statement=p.statement,
            code_snippet=p.code_snippet,
            options=p.options,
            reasoning_pattern=p.reasoning_pattern
        )
        for p in puzzles
    ]

@router.post("/{puzzle_id}/submit", response_model=LogicSubmitResponse)
def submit_logic_answer(
    puzzle_id: str,
    payload: LogicSubmitRequest,
    db: Session = Depends(get_db)
):
    p = db.query(LogicPuzzle).filter_by(id=puzzle_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Logic puzzle not found")

    user_id = payload.user_id or "default_user"
    clean_ans = payload.answer.strip()
    is_correct = (clean_ans == p.correct_answer.strip())

    sub = LogicSubmission(
        user_id=user_id,
        puzzle_id=p.id,
        answer=clean_ans,
        is_correct=is_correct,
        submitted_at=datetime.now(timezone.utc)
    )
    db.add(sub)
    db.commit()

    return LogicSubmitResponse(
        is_correct=is_correct,
        correct_answer=p.correct_answer,
        explanation=p.explanation
    )
