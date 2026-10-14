from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models import Question, QuestionAttempt, Bookmark, MistakeRecord
from backend.schemas import (
    QuestionResponse, QuestionDetailResponse,
    SubmitAnswerRequest, SubmitAnswerResponse,
    ProgressiveHintRequest, ProgressiveHintResponse,
    StepGuidanceRequest, StepGuidanceResponse,
    AskTutorRequest, AskTutorResponse,
    BookmarkToggleRequest, BookmarkResponse
)
from backend.services.evaluator import evaluate_answer
from backend.services.diagnosis import diagnose_mistake
from backend.services.mastery import calculate_topic_mastery, schedule_spaced_revision
from backend.services.tutor import tutor_service

router = APIRouter(prefix="/api/questions", tags=["Questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(
    topic_id: Optional[str] = None,
    category: Optional[str] = None,
    level: Optional[str] = None,
    question_type: Optional[str] = None,
    search: Optional[str] = None,
    user_id: str = "default_user",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if topic_id:
        query = query.filter(Question.topic_id == topic_id)
    if category:
        query = query.filter(Question.category == category)
    if level:
        query = query.filter(Question.level == level)
    if question_type:
        query = query.filter(Question.question_type == question_type)
    if search:
        query = query.filter(Question.question_text.ilike(f"%{search}%"))

    questions = query.offset(skip).limit(limit).all()

    # Check bookmarks for user
    bm_qids = set(
        b.question_id for b in db.query(Bookmark.question_id).filter_by(user_id=user_id).all()
    )

    results = []
    for q in questions:
        results.append(QuestionResponse(
            id=q.id,
            source_id=q.source_id,
            source_file=q.source_file,
            category=q.category,
            topic_id=q.topic_id,
            subtopic_name=q.subtopic_name,
            level=q.level,
            stimulus_context=q.stimulus_context,
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options,
            difficulty=q.difficulty,
            hints=q.hints or [],
            formula_reference=q.formula_reference,
            is_bookmarked=(q.id in bm_qids)
        ))

    return results

@router.get("/{question_id}", response_model=QuestionDetailResponse)
def get_question(question_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    q = db.query(Question).filter_by(id=question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    is_bm = db.query(Bookmark).filter_by(user_id=user_id, question_id=question_id).first() is not None

    return QuestionDetailResponse(
        id=q.id,
        source_id=q.source_id,
        source_file=q.source_file,
        category=q.category,
        topic_id=q.topic_id,
        subtopic_name=q.subtopic_name,
        level=q.level,
        stimulus_context=q.stimulus_context,
        question_text=q.question_text,
        question_type=q.question_type,
        options=q.options,
        difficulty=q.difficulty,
        hints=q.hints or [],
        formula_reference=q.formula_reference,
        is_bookmarked=is_bm,
        correct_answer=q.correct_answer,
        reference_solution=q.reference_solution
    )

@router.post("/{question_id}/submit", response_model=SubmitAnswerResponse)
def submit_answer(
    question_id: str,
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter_by(id=question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    # 1. Deterministic evaluation
    eval_result = evaluate_answer(
        submitted=payload.submitted_answer,
        correct=q.correct_answer,
        question_type=q.question_type,
        options=q.options
    )

    is_correct = eval_result["is_correct"]
    error_diag = None
    error_cat = None

    # 2. Mistake diagnosis if incorrect
    if not is_correct:
        error_diag = diagnose_mistake(
            question_text=q.question_text,
            submitted_answer=payload.submitted_answer,
            correct_answer=q.correct_answer,
            reference_solution=q.reference_solution,
            category=q.category,
            time_spent=payload.time_spent,
            hints_used=payload.hints_used,
            scratchpad_notes=payload.scratchpad_notes
        )
        error_cat = error_diag["error_category"]

    # 3. Record QuestionAttempt
    attempt = QuestionAttempt(
        user_id=payload.user_id,
        question_id=q.id,
        session_id=payload.session_id,
        submitted_answer=payload.submitted_answer,
        is_correct=is_correct,
        hints_used=payload.hints_used,
        time_spent=payload.time_spent,
        error_category=error_cat,
        scratchpad_notes=payload.scratchpad_notes,
        attempted_at=datetime.utcnow()
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # 4. If incorrect, store MistakeRecord in Notebook
    if not is_correct and error_diag:
        mistake = MistakeRecord(
            attempt_id=attempt.id,
            user_id=payload.user_id,
            question_id=q.id,
            topic_id=q.topic_id,
            error_category=error_cat,
            what_went_wrong=error_diag["what_went_wrong"],
            why_it_went_wrong=error_diag["why_it_went_wrong"],
            correct_reasoning=error_diag["correct_reasoning"],
            how_to_avoid=error_diag["how_to_avoid"],
            corrective_exercise=error_diag.get("corrective_exercise"),
            retest_status="pending"
        )
        db.add(mistake)
        db.commit()

    # 5. Update Topic Mastery
    updated_mastery = calculate_topic_mastery(db, payload.user_id, q.topic_id)

    # 6. Schedule Spaced Repetition Revision
    schedule_spaced_revision(db, payload.user_id, q.id, q.topic_id, is_correct)

    mastery_info = {
        "topic_id": q.topic_id,
        "mastery_score": updated_mastery.mastery_score,
        "status": updated_mastery.status,
        "total_attempted": updated_mastery.total_attempted,
        "total_correct": updated_mastery.total_correct
    }

    return SubmitAnswerResponse(
        is_correct=is_correct,
        submitted_answer=payload.submitted_answer,
        correct_answer=q.correct_answer,
        reference_solution=q.reference_solution,
        match_type=eval_result["match_type"],
        feedback=eval_result["feedback"],
        attempt_id=attempt.id,
        hints_used=payload.hints_used,
        error_diagnosis=error_diag,
        mastery_update=mastery_info
    )

@router.post("/{question_id}/hints", response_model=ProgressiveHintResponse)
def get_hint(
    question_id: str,
    payload: ProgressiveHintRequest,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter_by(id=question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    hint_data = tutor_service.get_progressive_hint(
        question_text=q.question_text,
        reference_solution=q.reference_solution,
        correct_answer=q.correct_answer,
        hint_level=payload.hint_level,
        current_attempt=payload.current_attempt
    )

    return ProgressiveHintResponse(
        hint_level=hint_data["hint_level"],
        title=hint_data["title"],
        content=hint_data["content"],
        educational_takeaway=hint_data.get("educational_takeaway"),
        correct_answer=hint_data.get("correct_answer")
    )

@router.post("/{question_id}/step_tutor", response_model=StepGuidanceResponse)
def get_step_guidance(
    question_id: str,
    payload: StepGuidanceRequest,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter_by(id=question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    step_data = tutor_service.generate_step_by_step_guidance(
        question_text=q.question_text,
        stimulus_context=q.stimulus_context,
        reference_solution=q.reference_solution,
        correct_answer=q.correct_answer,
        step_name=payload.step_name
    )

    return StepGuidanceResponse(
        step=step_data["step"],
        title=step_data["title"],
        content=step_data["content"],
        guiding_question=step_data.get("guiding_question")
    )

@router.post("/{question_id}/ask_ai", response_model=AskTutorResponse)
async def ask_ai_tutor(
    question_id: str,
    payload: AskTutorRequest,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter_by(id=question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    res = await tutor_service.get_ai_explanation(
        question_text=q.question_text,
        reference_solution=q.reference_solution,
        correct_answer=q.correct_answer,
        learner_query=payload.query
    )

    return AskTutorResponse(
        provider=res["provider"],
        explanation=res["explanation"],
        source=res["source"]
    )

@router.post("/{question_id}/bookmark", response_model=BookmarkResponse)
def toggle_bookmark(
    question_id: str,
    payload: BookmarkToggleRequest,
    db: Session = Depends(get_db)
):
    bm = db.query(Bookmark).filter_by(user_id=payload.user_id, question_id=question_id).first()
    if bm:
        db.delete(bm)
        db.commit()
        return BookmarkResponse(is_bookmarked=False, notes=None)
    else:
        new_bm = Bookmark(user_id=payload.user_id, question_id=question_id, notes=payload.notes)
        db.add(new_bm)
        db.commit()
        return BookmarkResponse(is_bookmarked=True, notes=payload.notes)
