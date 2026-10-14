from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Topic, Question, TopicMastery, ConceptLesson
from backend.schemas import TopicResponse, ConceptLessonResponse

router = APIRouter(prefix="/api/topics", tags=["Topics"])

@router.get("", response_model=List[TopicResponse])
def get_all_topics(user_id: str = "default_user", db: Session = Depends(get_db)):
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    results = []
    
    for t in topics:
        q_count = db.query(Question).filter_by(topic_id=t.id).count()
        mastery = db.query(TopicMastery).filter_by(user_id=user_id, topic_id=t.id).first()
        
        mastery_score = mastery.mastery_score if mastery else 0.0
        status = mastery.status if mastery else "not_started"
        unassisted = 0.0
        if mastery and mastery.total_attempted > 0:
            unassisted = round((mastery.unassisted_correct / mastery.total_attempted) * 100.0, 1)

        results.append(TopicResponse(
            id=t.id,
            name=t.name,
            category=t.category,
            parent_topic_id=t.parent_topic_id,
            description=t.description or "",
            prerequisites=t.prerequisites or [],
            icon=t.icon or "BookOpen",
            order_index=t.order_index or 0,
            total_questions=q_count,
            mastery_score=mastery_score,
            status=status,
            unassisted_accuracy=unassisted
        ))
        
    return results

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_detail(topic_id: str, user_id: str = "default_user", db: Session = Depends(get_db)):
    t = db.query(Topic).filter_by(id=topic_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Topic not found")
        
    q_count = db.query(Question).filter_by(topic_id=t.id).count()
    mastery = db.query(TopicMastery).filter_by(user_id=user_id, topic_id=t.id).first()
    
    mastery_score = mastery.mastery_score if mastery else 0.0
    status = mastery.status if mastery else "not_started"
    unassisted = 0.0
    if mastery and mastery.total_attempted > 0:
        unassisted = round((mastery.unassisted_correct / mastery.total_attempted) * 100.0, 1)

    return TopicResponse(
        id=t.id,
        name=t.name,
        category=t.category,
        parent_topic_id=t.parent_topic_id,
        description=t.description or "",
        prerequisites=t.prerequisites or [],
        icon=t.icon or "BookOpen",
        order_index=t.order_index or 0,
        total_questions=q_count,
        mastery_score=mastery_score,
        status=status,
        unassisted_accuracy=unassisted
    )

@router.get("/{topic_id}/lesson", response_model=ConceptLessonResponse)
def get_topic_lesson(topic_id: str, db: Session = Depends(get_db)):
    lesson = db.query(ConceptLesson).filter_by(topic_id=topic_id).first()
    if not lesson:
        # Generate on-the-fly default structured lesson using topic data
        topic = db.query(Topic).filter_by(id=topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        # Fetch representative question
        rep_q = db.query(Question).filter_by(topic_id=topic_id).first()
        sample_q = rep_q.question_text if rep_q else "Calculate the target value."
        sample_sol = rep_q.reference_solution if rep_q else "Step-by-step breakdown."

        return ConceptLessonResponse(
            id=topic_id,
            topic_id=topic_id,
            category=topic.category,
            title=f"{topic.name} Mastery",
            concept_summary=f"Foundational understanding of {topic.name} in {topic.category}.",
            why_needed=f"Crucial for high performance in aptitude exams and developing analytical precision.",
            simple_explanation=f"A systematic methodology to analyze and solve problems involving {topic.name}.",
            real_world_example=f"Applying {topic.name} in day-to-day data reasoning and engineering optimization.",
            intuition=f"Break the problem into primary components: Given data, Governing relations, and Unknowns.",
            important_terms=[
                {"term": "Base Quantity", "definition": "The starting baseline reference."},
                {"term": "Rate of Change", "definition": "Proportional delta between states."}
            ],
            formulas=[
                {
                    "name": f"{topic.name} Standard Form",
                    "formula": "Governing Rule = Input / Standard Reference",
                    "why_works": "Scales the quantity proportionally.",
                    "when_to_use": "Direct calculation under standard placement patterns."
                }
            ],
            step_by_step_example={
                "question": sample_q,
                "steps": ["Step 1: Parse given values.", "Step 2: Apply governing relation.", "Step 3: Compute final value."],
                "solution": sample_sol
            },
            placement_example={
                "question": f"Advanced {topic.name} problem under exam pressure.",
                "approach": "Avoid premature rounding and cancel common factors first.",
                "solution": sample_sol,
                "trap": "Misinterpreting the base value or skipping unit conversions."
            },
            common_traps=[
                "Skipping unit conversions.",
                "Rushing calculations without verifying bounds."
            ],
            key_takeaways=[
                "Understand the principle before memorizing shortcuts.",
                "Independent verification prevents negative marking."
            ]
        )
    return lesson
