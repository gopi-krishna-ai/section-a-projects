from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.models import TopicMastery, QuestionAttempt, RevisionSchedule, Question

# Spaced repetition intervals (in days)
SPACED_INTERVALS = [1, 3, 7, 14, 30]

def calculate_topic_mastery(
    db: Session,
    user_id: str,
    topic_id: str
) -> TopicMastery:
    """
    Computes rigorous topic mastery estimate based on attempts,
    difficulty weighting, unassisted accuracy, and recency.
    """
    mastery = db.query(TopicMastery).filter_by(user_id=user_id, topic_id=topic_id).first()
    if not mastery:
        mastery = TopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            mastery_score=0.0,
            status="not_started",
            total_attempted=0,
            total_correct=0,
            unassisted_correct=0
        )
        db.add(mastery)

    # Get all attempts for this topic
    attempts = (
        db.query(QuestionAttempt)
        .join(Question, QuestionAttempt.question_id == Question.id)
        .filter(QuestionAttempt.user_id == user_id, Question.topic_id == topic_id)
        .order_by(QuestionAttempt.attempted_at.asc())
        .all()
    )

    if not attempts:
        mastery.mastery_score = 0.0
        mastery.status = "not_started"
        mastery.total_attempted = 0
        mastery.total_correct = 0
        mastery.unassisted_correct = 0
        db.commit()
        return mastery

    # Count unique questions attempted
    question_attempts_map: Dict[str, List[QuestionAttempt]] = {}
    for att in attempts:
        if att.question_id not in question_attempts_map:
            question_attempts_map[att.question_id] = []
        question_attempts_map[att.question_id].append(att)

    total_attempted = len(question_attempts_map)
    total_correct = 0
    unassisted_correct = 0
    weighted_score = 0.0
    total_weight = 0.0

    for q_id, q_atts in question_attempts_map.items():
        # First attempt is most indicative of spontaneous recall
        first_att = q_atts[0]
        # Latest attempt indicates current retention
        last_att = q_atts[-1]

        q = db.query(Question).filter_by(id=q_id).first()
        diff = q.difficulty if q else 1.0

        if last_att.is_correct:
            total_correct += 1
            if last_att.hints_used == 0:
                unassisted_correct += 1
                # Full weight for unassisted correct
                weighted_score += 100.0 * diff
            else:
                # Scaled penalty for hints: 75% for 1 hint, 50% for 2, 25% for 3+
                penalty_factor = max(0.25, 1.0 - (last_att.hints_used * 0.25))
                weighted_score += 100.0 * diff * penalty_factor
        else:
            weighted_score += 0.0

        total_weight += 100.0 * diff

    raw_score = (weighted_score / total_weight) if total_weight > 0 else 0.0

    # Apply volume and confidence factor:
    # Need at least 5 questions to reach high mastery
    volume_factor = min(1.0, total_attempted / 5.0)
    mastery_score = round(raw_score * volume_factor, 1)

    # Determine status
    if total_attempted == 0:
        status = "not_started"
    elif total_attempted < 3:
        status = "learning"
    elif mastery_score < 50.0:
        status = "needs_practice"
    elif mastery_score < 75.0:
        status = "improving"
    elif mastery_score >= 75.0:
        # Check recency (if not practiced in > 14 days, flag needs_revision)
        last_attempt_time = attempts[-1].attempted_at
        if (datetime.utcnow() - last_attempt_time).days > 14:
            status = "needs_revision"
        else:
            status = "proficient"
    else:
        status = "improving"

    mastery.mastery_score = mastery_score
    mastery.status = status
    mastery.total_attempted = total_attempted
    mastery.total_correct = total_correct
    mastery.unassisted_correct = unassisted_correct
    mastery.last_practiced_at = attempts[-1].attempted_at
    mastery.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(mastery)
    return mastery

def schedule_spaced_revision(
    db: Session,
    user_id: str,
    question_id: str,
    topic_id: str,
    is_correct: bool
) -> RevisionSchedule:
    """
    Schedules spaced repetition based on an SM-2 inspired interval.
    If correct, increases interval: 1d -> 3d -> 7d -> 14d -> 30d.
    If incorrect, resets interval to 1d.
    """
    existing = db.query(RevisionSchedule).filter_by(
        user_id=user_id,
        question_id=question_id
    ).first()

    now = datetime.utcnow()

    if not existing:
        interval = 1 if is_correct else 1
        rep_num = 1 if is_correct else 0
        due_at = now + timedelta(days=interval)
        rev = RevisionSchedule(
            user_id=user_id,
            topic_id=topic_id,
            question_id=question_id,
            interval_days=interval,
            repetition_number=rep_num,
            ease_factor=2.5,
            due_at=due_at,
            review_status="pending",
            last_reviewed_at=now
        )
        db.add(rev)
        db.commit()
        db.refresh(rev)
        return rev

    if is_correct:
        next_rep = existing.repetition_number + 1
        idx = min(next_rep, len(SPACED_INTERVALS) - 1)
        next_interval = SPACED_INTERVALS[idx]
        existing.repetition_number = next_rep
        existing.interval_days = next_interval
        existing.due_at = now + timedelta(days=next_interval)
        existing.review_status = "pending"
        existing.last_reviewed_at = now
    else:
        # Reset on lapse
        existing.repetition_number = 0
        existing.interval_days = 1
        existing.due_at = now + timedelta(days=1)
        existing.review_status = "pending"
        existing.last_reviewed_at = now

    db.commit()
    db.refresh(existing)
    return existing
