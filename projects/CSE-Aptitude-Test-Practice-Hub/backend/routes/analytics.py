from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Dict, Any
from backend.database import get_db
from backend.models import (
    Question, Topic, QuestionAttempt, TopicMastery, MistakeRecord, RevisionSchedule
)
from backend.schemas import DashboardResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard_data(user_id: str = "default_user", db: Session = Depends(get_db)):
    total_repo_q = db.query(Question).count()

    # Unique questions attempted
    attempts = db.query(QuestionAttempt).filter_by(user_id=user_id).all()
    q_map: Dict[str, List[QuestionAttempt]] = {}
    for a in attempts:
        if a.question_id not in q_map:
            q_map[a.question_id] = []
        q_map[a.question_id].append(a)

    total_attempted_unique = len(q_map)
    total_solved_correct = sum(1 for qid, atts in q_map.items() if any(x.is_correct for x in atts))
    total_unassisted_correct = sum(1 for qid, atts in q_map.items() if any(x.is_correct and x.hints_used == 0 for x in atts))

    overall_accuracy = round((total_solved_correct / total_attempted_unique * 100.0), 1) if total_attempted_unique > 0 else 0.0
    unassisted_acc = round((total_unassisted_correct / total_attempted_unique * 100.0), 1) if total_attempted_unique > 0 else 0.0

    # Topics currently studying & needing improvement
    masteries = db.query(TopicMastery).filter_by(user_id=user_id).all()
    studying = []
    needing_imp = []

    for m in masteries:
        t = db.query(Topic).filter_by(id=m.topic_id).first()
        if not t:
            continue
        info = {
            "topic_id": t.id,
            "topic_name": t.name,
            "category": t.category,
            "mastery_score": m.mastery_score,
            "status": m.status,
            "total_attempted": m.total_attempted,
            "total_correct": m.total_correct
        }
        if m.total_attempted > 0:
            studying.append(info)
        if m.status in ["needs_practice", "needs_revision"] or (m.total_attempted >= 2 and m.mastery_score < 60.0):
            needing_imp.append(info)

    # Top repeated mistakes
    mistake_counts = (
        db.query(MistakeRecord.error_category, func.count(MistakeRecord.id))
        .filter(MistakeRecord.user_id == user_id)
        .group_by(MistakeRecord.error_category)
        .order_by(func.count(MistakeRecord.id).desc())
        .limit(5)
        .all()
    )
    repeated_mistakes = [
        {"error_category": row[0], "count": row[1]} for row in mistake_counts
    ]

    # Revisions due
    due_rev_count = (
        db.query(RevisionSchedule)
        .filter(RevisionSchedule.user_id == user_id, RevisionSchedule.review_status == "pending")
        .count()
    )

    # Recent attempts (last 10)
    recent_atts = (
        db.query(QuestionAttempt)
        .filter_by(user_id=user_id)
        .order_by(QuestionAttempt.attempted_at.desc())
        .limit(10)
        .all()
    )
    recent_activity = []
    for ra in recent_atts:
        q = db.query(Question).filter_by(id=ra.question_id).first()
        recent_activity.append({
            "attempt_id": ra.id,
            "question_id": ra.question_id,
            "question_text": q.question_text[:80] + "..." if q else "Question",
            "category": q.category if q else "General",
            "is_correct": ra.is_correct,
            "hints_used": ra.hints_used,
            "time_spent": ra.time_spent,
            "attempted_at": ra.attempted_at.isoformat()
        })

    # Recommended next lesson
    # Find first uncompleted topic whose prerequisites are met
    rec_topic = None
    all_topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    completed_topics = set(
        m.topic_id for m in masteries if m.mastery_score >= 70.0
    )

    for t in all_topics:
        prereqs = t.prerequisites or []
        # Check if prerequisites are satisfied
        if all(p in completed_topics for p in prereqs):
            # If not yet proficient
            m = next((m for m in masteries if m.topic_id == t.id), None)
            if not m or m.mastery_score < 75.0:
                rec_topic = {
                    "topic_id": t.id,
                    "topic_name": t.name,
                    "category": t.category,
                    "reason": "Prerequisites completed. Ready for guided concept mastery."
                }
                break

    if not rec_topic and all_topics:
        rec_topic = {
            "topic_id": all_topics[0].id,
            "topic_name": all_topics[0].name,
            "category": all_topics[0].category,
            "reason": "Recommended starting foundational topic."
        }

    return DashboardResponse(
        total_repository_questions=total_repo_q,
        total_attempted_unique=total_attempted_unique,
        total_solved_correct=total_solved_correct,
        overall_accuracy=overall_accuracy,
        unassisted_accuracy=unassisted_acc,
        current_studying_topics=studying[:6],
        topics_needing_improvement=needing_imp[:6],
        top_repeated_mistakes=repeated_mistakes,
        due_revisions_count=due_rev_count,
        recent_attempts=recent_activity,
        recommended_next_lesson=rec_topic
    )
