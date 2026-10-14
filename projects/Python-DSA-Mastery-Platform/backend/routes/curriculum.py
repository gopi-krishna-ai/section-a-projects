from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database import get_db
from backend.models import Topic, Lesson, Problem, TopicMastery
from backend.schemas import TopicSummary, LessonResponse

router = APIRouter(prefix="/api/curriculum", tags=["Curriculum"])

@router.get("/topics", response_model=List[TopicSummary])
def get_topics(
    track: Optional[str] = None,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
):
    query = db.query(Topic).order_by(Topic.order_index.asc())
    if track:
        query = query.filter(Topic.track == track)
    topics = query.all()

    results = []
    for t in topics:
        prob_count = db.query(Problem).filter_by(topic_id=t.id).count()
        mastery = db.query(TopicMastery).filter_by(user_id=user_id, topic_id=t.id).first()
        m_score = mastery.mastery_score if mastery else 0.0
        m_status = mastery.status if mastery else "not_started"

        results.append(TopicSummary(
            id=t.id,
            track=t.track,
            level=t.level,
            title=t.title,
            description=t.description,
            order_index=t.order_index,
            icon=t.icon,
            total_problems=prob_count,
            mastery_score=m_score,
            status=m_status
        ))
    return results

@router.get("/topics/{topic_id}/lessons", response_model=List[LessonResponse])
def get_topic_lessons(topic_id: str, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter_by(topic_id=topic_id).order_by(Lesson.order_index.asc()).all()
    return [
        LessonResponse(
            id=l.id,
            topic_id=l.topic_id,
            title=l.title,
            content=l.content,
            runnable_snippets=l.runnable_snippets or [],
            key_takeaways=l.key_takeaways or []
        )
        for l in lessons
    ]
