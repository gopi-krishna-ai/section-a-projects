from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List
from backend.database import get_db
from backend.models import (
    Problem, ProblemSubmission, MistakeRecord, TopicMastery,
    RevisionSchedule, Topic
)
from backend.schemas import DashboardResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Progress"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(user_id: str = "default_user", db: Session = Depends(get_db)):
    total_bank = db.query(Problem).count()

    # User Submissions
    subs = db.query(ProblemSubmission).filter_by(user_id=user_id).all()
    total_attempted = len({s.problem_id for s in subs})
    solved_submissions = [s for s in subs if s.status == "Passed"]
    solved_problem_ids = {s.problem_id for s in solved_submissions}
    total_solved = len(solved_problem_ids)

    independent_solved_ids = {s.problem_id for s in solved_submissions if s.is_independent}
    independent_solved = len(independent_solved_ids)

    overall_acc = round((total_solved / total_attempted * 100.0), 1) if total_attempted > 0 else 0.0
    indep_acc = round((independent_solved / total_attempted * 100.0), 1) if total_attempted > 0 else 0.0

    # Topic Masteries
    masteries = db.query(TopicMastery).filter_by(user_id=user_id).all()
    active_topics = []
    needing_focus = []
    for m in masteries:
        t = db.query(Topic).filter_by(id=m.topic_id).first()
        if t:
            item = {
                "topic_id": t.id,
                "title": t.title,
                "track": t.track,
                "mastery_score": m.mastery_score,
                "status": m.status,
                "total_attempted": m.total_attempted,
                "independent_solved": m.independent_solved
            }
            if m.total_attempted > 0:
                active_topics.append(item)
            if m.status in ["needs_revision", "developing_independence"] or m.mastery_score < 60.0:
                needing_focus.append(item)

    # Top Mistake Patterns
    mistakes = db.query(MistakeRecord).filter_by(user_id=user_id).all()
    pattern_map: Dict[str, int] = {}
    for m in mistakes:
        pattern_map[m.error_category] = pattern_map.get(m.error_category, 0) + 1
    top_patterns = [
        {"error_category": k, "count": v}
        for k, v in sorted(pattern_map.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Due revisions
    due_revs = (
        db.query(RevisionSchedule)
        .filter(RevisionSchedule.user_id == user_id, RevisionSchedule.review_status == "pending")
        .count()
    )

    # Recent submissions
    recent_subs = (
        db.query(ProblemSubmission)
        .filter_by(user_id=user_id)
        .order_by(ProblemSubmission.submitted_at.desc())
        .limit(6)
        .all()
    )
    recent_items = []
    for s in recent_subs:
        p = db.query(Problem).filter_by(id=s.problem_id).first()
        recent_items.append({
            "problem_id": s.problem_id,
            "problem_title": p.title if p else "Problem",
            "status": s.status,
            "is_independent": s.is_independent,
            "hints_used": s.hints_used,
            "execution_time_ms": s.execution_time_ms,
            "submitted_at": s.submitted_at.isoformat()
        })

    # Recommended next task
    rec = None
    first_unsolved = None
    for p in db.query(Problem).all():
        if p.id not in solved_problem_ids:
            first_unsolved = p
            break
    if first_unsolved:
        t = db.query(Topic).filter_by(id=first_unsolved.topic_id).first()
        rec = {
            "type": "problem",
            "id": first_unsolved.slug,
            "title": first_unsolved.title,
            "topic": t.title if t else "DSA",
            "difficulty": first_unsolved.difficulty,
            "reason": "Next step in structured learning path."
        }

    return DashboardResponse(
        total_problems_in_bank=total_bank,
        total_attempted=total_attempted,
        total_solved=total_solved,
        independent_solved=independent_solved,
        independent_accuracy=indep_acc,
        overall_accuracy=overall_acc,
        streak_days=3 if total_attempted > 0 else 0,
        active_topics=active_topics,
        topics_needing_focus=needing_focus,
        top_mistake_patterns=top_patterns,
        due_revisions_count=due_revs,
        recent_submissions=recent_items,
        recommended_next_task=rec
    )
