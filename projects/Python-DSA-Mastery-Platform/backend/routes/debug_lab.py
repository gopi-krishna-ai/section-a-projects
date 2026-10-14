from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from backend.database import get_db
from backend.models import DebugExercise, DebugSubmission
from backend.schemas import DebugExerciseResponse, DebugSubmitRequest, DebugSubmitResponse
from backend.services.executor import run_problem_test_cases

router = APIRouter(prefix="/api/debug_lab", tags=["Debugging Laboratory"])

@router.get("", response_model=List[DebugExerciseResponse])
def list_debug_exercises(db: Session = Depends(get_db)):
    exercises = db.query(DebugExercise).all()
    return [
        DebugExerciseResponse(
            id=e.id,
            title=e.title,
            topic=e.topic,
            difficulty=e.difficulty,
            buggy_code=e.buggy_code,
            bug_category=e.bug_category,
            description=e.description,
            hint=e.hint,
            test_cases=e.test_cases or []
        )
        for e in exercises
    ]

@router.get("/{exercise_id}", response_model=DebugExerciseResponse)
def get_debug_exercise(exercise_id: str, db: Session = Depends(get_db)):
    e = db.query(DebugExercise).filter_by(id=exercise_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Debug exercise not found")
    return DebugExerciseResponse(
        id=e.id,
        title=e.title,
        topic=e.topic,
        difficulty=e.difficulty,
        buggy_code=e.buggy_code,
        bug_category=e.bug_category,
        description=e.description,
        hint=e.hint,
        test_cases=e.test_cases or []
    )

@router.post("/{exercise_id}/submit", response_model=DebugSubmitResponse)
def submit_debug_solution(
    exercise_id: str,
    payload: DebugSubmitRequest,
    db: Session = Depends(get_db)
):
    e = db.query(DebugExercise).filter_by(id=exercise_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Debug exercise not found")

    user_id = payload.user_id or "default_user"
    eval_res = run_problem_test_cases(payload.code, e.test_cases or [])
    is_fixed = (eval_res["status"] == "Passed")

    sub = DebugSubmission(
        user_id=user_id,
        exercise_id=e.id,
        submitted_code=payload.code,
        is_fixed=is_fixed,
        submitted_at=datetime.now(timezone.utc)
    )
    db.add(sub)
    db.commit()

    return DebugSubmitResponse(
        is_fixed=is_fixed,
        stdout=f"Passed {eval_res['passes_count']}/{eval_res['total_tests']} tests." if is_fixed else f"Only passed {eval_res['passes_count']}/{eval_res['total_tests']} tests.",
        error=eval_res.get("error_output"),
        explanation=e.explanation if is_fixed else "Keep checking the bug hint or run single test cases."
    )
