from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from backend.database import get_db
from backend.models import Problem, ProblemSubmission, MistakeRecord
from backend.schemas import (
    ProblemSummary, ProblemDetail, SubmitSolutionRequest,
    SubmitSolutionResponse, TestResultItem
)
from backend.services.executor import run_problem_test_cases
from backend.services.diagnosis import diagnose_code_failure
from backend.services.mastery import update_topic_mastery, schedule_spaced_revision
from backend.services.mentor import get_socratic_hint, ask_mentor

router = APIRouter(prefix="/api/problems", tags=["Problems"])

@router.get("", response_model=List[ProblemSummary])
def list_problems(
    topic_id: Optional[str] = None,
    difficulty: Optional[str] = None,
    track: Optional[str] = None,
    search: Optional[str] = None,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    query = db.query(Problem)
    if topic_id:
        query = query.filter(Problem.topic_id == topic_id)
    if difficulty and difficulty != "All":
        query = query.filter(Problem.difficulty == difficulty)
    if track and track != "All":
        query = query.filter(Problem.track == track)
    if search:
        query = query.filter(Problem.title.ilike(f"%{search}%"))

    problems = query.all()
    user_subs = db.query(ProblemSubmission).filter_by(user_id=user_id).all()
    solved_set = {s.problem_id for s in user_subs if s.status == "Passed"}
    attempted_set = {s.problem_id for s in user_subs}

    return [
        ProblemSummary(
            id=p.id,
            slug=p.slug,
            title=p.title,
            topic_id=p.topic_id,
            track=p.track,
            difficulty=p.difficulty,
            time_complexity=p.time_complexity,
            space_complexity=p.space_complexity,
            tags=p.tags or [],
            has_attempted=(p.id in attempted_set),
            is_solved=(p.id in solved_set)
        )
        for p in problems
    ]

@router.get("/{problem_id}", response_model=ProblemDetail)
def get_problem_detail(problem_id: str, db: Session = Depends(get_db)):
    p = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    visible_tests = [tc for tc in (p.test_cases or []) if not tc.get("is_hidden")]

    return ProblemDetail(
        id=p.id,
        slug=p.slug,
        title=p.title,
        topic_id=p.topic_id,
        track=p.track,
        difficulty=p.difficulty,
        description=p.description,
        constraints=p.constraints or [],
        examples=p.examples or [],
        starter_code=p.starter_code,
        time_complexity=p.time_complexity,
        space_complexity=p.space_complexity,
        hints=p.hints or [],
        visible_tests=visible_tests,
        tags=p.tags or [],
        dry_run_steps=p.dry_run_steps or []
    )

@router.post("/{problem_id}/hints")
def fetch_hint(problem_id: str, hint_level: int = Query(1, ge=1, le=6), db: Session = Depends(get_db)):
    p = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    return get_socratic_hint(p, hint_level)

@router.post("/{problem_id}/ask_mentor")
def mentor_query(problem_id: str, payload: dict, db: Session = Depends(get_db)):
    p = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    user_code = payload.get("code", "")
    query = payload.get("query", "How do I approach this?")
    err = payload.get("error_message")

    return ask_mentor(p.title, user_code, query, err)

@router.post("/{problem_id}/submit", response_model=SubmitSolutionResponse)
def submit_solution(
    problem_id: str,
    payload: SubmitSolutionRequest,
    db: Session = Depends(get_db)
):
    p = db.query(Problem).filter((Problem.id == problem_id) | (Problem.slug == problem_id)).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")

    user_id = payload.user_id or "default_user"
    test_cases = p.test_cases or []

    # Run tests in isolated subprocess
    eval_result = run_problem_test_cases(payload.code, test_cases)

    status = eval_result["status"]
    passes = eval_result["passes_count"]
    total = eval_result["total_tests"]
    is_correct = (status == "Passed")
    is_independent = (is_correct and payload.hints_used == 0 and not payload.solution_viewed)

    # Save submission
    sub = ProblemSubmission(
        user_id=user_id,
        problem_id=p.id,
        code=payload.code,
        status=status,
        passes_count=passes,
        total_tests=total,
        execution_time_ms=eval_result["execution_time_ms"],
        is_independent=is_independent,
        hints_used=payload.hints_used,
        solution_viewed=payload.solution_viewed,
        error_output=eval_result.get("error_output"),
        submitted_at=datetime.now(timezone.utc)
    )
    db.add(sub)
    db.flush()

    mistake_info = None
    if not is_correct:
        # Find first failing test case
        failing_tc = None
        for r in eval_result.get("test_results", []):
            if not r.get("passed"):
                failing_tc = {
                    "input": r.get("input_str"),
                    "expected_output": r.get("expected_output_str"),
                    "actual_output": r.get("actual_output_str")
                }
                break

        diag = diagnose_code_failure(
            code=payload.code,
            status=status,
            error_output=eval_result.get("error_output"),
            failing_test_case=failing_tc,
            time_limit_exceeded=(status == "Timeout")
        )

        mistake = MistakeRecord(
            user_id=user_id,
            problem_id=p.id,
            submission_id=sub.id,
            error_category=diag["error_category"],
            submitted_code=payload.code,
            failing_test_case=failing_tc,
            what_went_wrong=diag["what_went_wrong"],
            why_it_went_wrong=diag["why_it_went_wrong"],
            how_to_avoid=diag["how_to_avoid"],
            corrective_exercise=diag.get("corrective_exercise"),
            retest_status="pending",
            created_at=datetime.now(timezone.utc)
        )
        db.add(mistake)
        mistake_info = diag

    # Update Topic Mastery
    mastery_data = update_topic_mastery(
        db=db,
        user_id=user_id,
        topic_id=p.topic_id,
        is_correct=is_correct,
        is_independent=is_independent
    )

    # Schedule SM-2 Spaced Revision
    schedule_spaced_revision(
        db=db,
        user_id=user_id,
        problem_id=p.id,
        is_correct=is_correct,
        is_independent=is_independent
    )

    db.commit()

    return SubmitSolutionResponse(
        status=status,
        passes_count=passes,
        total_tests=total,
        execution_time_ms=eval_result["execution_time_ms"],
        is_independent=is_independent,
        test_results=eval_result.get("test_results", []),
        mistake_diagnosis=mistake_info,
        mastery_update=mastery_data
    )
