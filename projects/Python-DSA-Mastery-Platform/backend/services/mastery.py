from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models import TopicMastery, RevisionSchedule, ProblemSubmission

def update_topic_mastery(
    db: Session,
    user_id: str,
    topic_id: str,
    is_correct: bool,
    is_independent: bool
) -> Dict[str, Any]:
    mastery = db.query(TopicMastery).filter_by(user_id=user_id, topic_id=topic_id).first()
    if not mastery:
        mastery = TopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            mastery_score=0.0,
            status="not_started",
            total_attempted=0,
            independent_solved=0,
            assisted_solved=0
        )
        db.add(mastery)

    mastery.total_attempted += 1
    if is_correct:
        if is_independent:
            mastery.independent_solved += 1
        else:
            mastery.assisted_solved += 1

    total_solved = mastery.independent_solved + mastery.assisted_solved
    
    # Independent solving is weighted 1.5x higher than assisted solving
    weighted_score = (mastery.independent_solved * 1.0 + mastery.assisted_solved * 0.4)
    target_benchmark = max(mastery.total_attempted, 5)
    raw_pct = min(100.0, round((weighted_score / target_benchmark) * 100.0, 1))

    mastery.mastery_score = raw_pct
    mastery.last_practiced_at = datetime.now(timezone.utc)

    # Determine status
    if mastery.total_attempted == 0:
        mastery.status = "not_started"
    elif raw_pct >= 90.0 and mastery.independent_solved >= 4:
        mastery.status = "mastered"
    elif raw_pct >= 75.0 and mastery.independent_solved >= 2:
        mastery.status = "proficient"
    elif mastery.assisted_solved > mastery.independent_solved and mastery.total_attempted >= 3:
        mastery.status = "developing_independence"
    elif raw_pct < 50.0 and mastery.total_attempted >= 2:
        mastery.status = "needs_revision"
    else:
        mastery.status = "practising"

    db.commit()
    db.refresh(mastery)

    return {
        "topic_id": mastery.topic_id,
        "mastery_score": mastery.mastery_score,
        "status": mastery.status,
        "independent_solved": mastery.independent_solved,
        "assisted_solved": mastery.assisted_solved,
        "total_attempted": mastery.total_attempted
    }

def schedule_spaced_revision(
    db: Session,
    user_id: str,
    problem_id: str,
    is_correct: bool,
    is_independent: bool
):
    rev = db.query(RevisionSchedule).filter_by(user_id=user_id, problem_id=problem_id).first()
    now = datetime.now(timezone.utc)

    if not rev:
        rev = RevisionSchedule(
            user_id=user_id,
            problem_id=problem_id,
            interval_days=1,
            repetition_number=1,
            ease_factor=2.5,
            due_at=now + timedelta(days=1),
            review_status="pending"
        )
        db.add(rev)
    else:
        if is_correct and is_independent:
            new_rep = rev.repetition_number + 1
            if new_rep == 1:
                interval = 1
            elif new_rep == 2:
                interval = 3
            elif new_rep == 3:
                interval = 7
            else:
                interval = int(round(rev.interval_days * rev.ease_factor))
            
            rev.repetition_number = new_rep
            rev.interval_days = interval
            rev.due_at = now + timedelta(days=interval)
            rev.review_status = "pending"
            rev.last_reviewed_at = now
        else:
            # Mistake or heavily assisted: Reset back to day 1 interval
            rev.repetition_number = 1
            rev.interval_days = 1
            rev.due_at = now + timedelta(days=1)
            rev.review_status = "pending"
            rev.last_reviewed_at = now

    db.commit()
