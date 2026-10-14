from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models import LearningSession, Question, QuestionAttempt, MistakeRecord, RevisionSchedule, Bookmark
from backend.schemas import StartSessionRequest, SessionResponse, QuestionResponse

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.post("/start", response_model=SessionResponse)
def start_session(payload: StartSessionRequest, db: Session = Depends(get_db)):
    mode = payload.mode
    limit = max(1, min(payload.num_questions, 50))
    user_id = payload.user_id

    # Create new session record
    session = LearningSession(
        user_id=user_id,
        topic_id=payload.topic_id,
        mode=mode,
        started_at=datetime.utcnow(),
        total_questions=limit,
        meta_info=payload.meta_info or {}
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Question selection based on mode
    q_query = db.query(Question)

    if mode == "topic" and payload.topic_id:
        q_query = q_query.filter(Question.topic_id == payload.topic_id)
        if payload.level:
            q_query = q_query.filter(Question.level == payload.level)

    elif mode == "challenge":
        q_query = q_query.filter(Question.level.in_(["Intermediate", "Advanced"]))
        if payload.topic_id:
            q_query = q_query.filter(Question.topic_id == payload.topic_id)

    elif mode == "weakness":
        # Find topics with pending mistakes or low mastery
        mistake_topics = [
            m.topic_id for m in db.query(MistakeRecord.topic_id)
            .filter_by(user_id=user_id, retest_status="pending").distinct().all()
        ]
        if mistake_topics:
            q_query = q_query.filter(Question.topic_id.in_(mistake_topics))
        elif payload.topic_id:
            q_query = q_query.filter(Question.topic_id == payload.topic_id)

    elif mode == "revision":
        due_qids = [
            r.question_id for r in db.query(RevisionSchedule.question_id)
            .filter(RevisionSchedule.user_id == user_id, RevisionSchedule.review_status == "pending")
            .all()
        ]
        if due_qids:
            q_query = q_query.filter(Question.id.in_(due_qids))

    elif mode == "exam":
        # Exam mode: balanced cross-section
        if payload.level:
            q_query = q_query.filter(Question.level == payload.level)

    # Shuffle to avoid repeats in same order
    questions = q_query.order_by(func.random()).limit(limit).all()

    # Fallback if no questions matched specific filter
    if not questions:
        questions = db.query(Question).order_by(func.random()).limit(limit).all()

    # Check bookmarks
    bm_qids = set(
        b.question_id for b in db.query(Bookmark.question_id).filter_by(user_id=user_id).all()
    )

    q_responses = [
        QuestionResponse(
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
        )
        for q in questions
    ]

    return SessionResponse(
        session_id=session.id,
        mode=session.mode,
        topic_id=session.topic_id,
        total_questions=len(q_responses),
        questions=q_responses
    )

@router.post("/{session_id}/complete")
def complete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(LearningSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.completed_at = datetime.utcnow()
    # Compute score
    attempts = db.query(QuestionAttempt).filter_by(session_id=session_id).all()
    score = sum(1 for a in attempts if a.is_correct)
    session.score = score
    db.commit()

    return {
        "session_id": session.id,
        "mode": session.mode,
        "completed_at": session.completed_at,
        "total_attempted": len(attempts),
        "score": score
    }
