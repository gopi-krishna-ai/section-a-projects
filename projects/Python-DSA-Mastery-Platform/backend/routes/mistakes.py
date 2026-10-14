from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import MistakeRecord, Problem
from backend.schemas import MistakeResponse, RetestMistakeRequest, RetestMistakeResponse
from backend.services.executor import run_problem_test_cases

router = APIRouter(prefix="/api/mistakes", tags=["Mistakes"])

@router.get("", response_model=List[MistakeResponse])
def get_mistakes(
    user_id: str = "default_user",
    retest_status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MistakeRecord).filter_by(user_id=user_id).order_by(MistakeRecord.created_at.desc())
    if retest_status and retest_status != "All":
        query = query.filter(MistakeRecord.retest_status == retest_status)
    if category and category != "All":
        query = query.filter(MistakeRecord.error_category == category)

    mistakes = query.all()
    results = []
    for m in mistakes:
        p = db.query(Problem).filter_by(id=m.problem_id).first()
        results.append(MistakeResponse(
            id=m.id,
            problem_id=m.problem_id,
            problem_title=p.title if p else "Unknown Problem",
            topic_id=p.topic_id if p else "general",
            error_category=m.error_category,
            submitted_code=m.submitted_code,
            failing_test_case=m.failing_test_case,
            what_went_wrong=m.what_went_wrong,
            why_it_went_wrong=m.why_it_went_wrong,
            how_to_avoid=m.how_to_avoid,
            retest_status=m.retest_status,
            created_at=m.created_at
        ))
    return results

@router.post("/{mistake_id}/retest", response_model=RetestMistakeResponse)
def retest_mistake(mistake_id: str, payload: RetestMistakeRequest, db: Session = Depends(get_db)):
    m = db.query(MistakeRecord).filter_by(id=mistake_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mistake record not found")

    p = db.query(Problem).filter_by(id=m.problem_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Associated problem not found")

    eval_res = run_problem_test_cases(payload.code, p.test_cases or [])
    is_resolved = (eval_res["status"] == "Passed")

    if is_resolved:
        m.retest_status = "resolved"
        db.commit()

    return RetestMistakeResponse(
        mistake_id=m.id,
        is_resolved=is_resolved,
        passes_count=eval_res["passes_count"],
        total_tests=eval_res["total_tests"],
        feedback="Mistake successfully resolved! Code passed all edge cases." if is_resolved else f"Retest failed: passed {eval_res['passes_count']}/{eval_res['total_tests']} tests."
    )
