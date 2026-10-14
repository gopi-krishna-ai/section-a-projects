import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.evaluator import evaluate_answer
from backend.services.diagnosis import diagnose_mistake
from backend.database import SessionLocal
from backend.models import Question, Topic, User

client = TestClient(app)

def test_evaluator_cases():
    # Exact numeric
    res1 = evaluate_answer("100", "100", "numeric")
    assert res1["is_correct"] is True

    # Numeric tolerance & unit stripping
    res2 = evaluate_answer("187.5", "187.5 units", "numeric")
    assert res2["is_correct"] is True

    # Currency format
    res3 = evaluate_answer("$180", "180", "numeric")
    assert res3["is_correct"] is True

    # Percentage
    res4 = evaluate_answer("20%", "20%", "numeric")
    assert res4["is_correct"] is True

    # MCQ letter
    res5 = evaluate_answer("B", "B) Plentiful", "mcq", ["A) Scarce", "B) Plentiful", "C) Limited", "D) Rare"])
    assert res5["is_correct"] is True

    # MCQ content
    res6 = evaluate_answer("Plentiful", "B) Plentiful", "mcq", ["A) Scarce", "B) Plentiful", "C) Limited", "D) Rare"])
    assert res6["is_correct"] is True

    # Sentence correction
    res7 = evaluate_answer("She sings beautifully", "She sings beautifully.", "text_correction")
    assert res7["is_correct"] is True

    # Ratio
    res8 = evaluate_answer("9:10", "9 : 10", "short_answer")
    assert res8["is_correct"] is True

    # Incorrect
    res9 = evaluate_answer("40", "100", "numeric")
    assert res9["is_correct"] is False

def test_diagnosis_engine():
    diag1 = diagnose_mistake(
        question_text="What is 25% of 400?",
        submitted_answer="10",
        correct_answer="100",
        reference_solution="25% of 400 = (25/100) * 400 = 100",
        category="Quantitative Aptitude",
        time_spent=20.0
    )
    assert diag1["error_category"] in ["Unit conversion error", "Calculation or arithmetic error", "Incorrect setup"]

    diag_fast = diagnose_mistake(
        question_text="Sample Q",
        submitted_answer="X",
        correct_answer="Y",
        reference_solution="Step 1...",
        category="Quantitative Aptitude",
        time_spent=1.5
    )
    assert diag_fast["error_category"] == "Guessing or insufficient evidence"

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_api_topics():
    response = client.get("/api/topics")
    assert response.status_code == 200
    topics = response.json()
    assert len(topics) >= 40
    assert any(t["id"] == "percentages" for t in topics)

def test_api_questions_and_solving_flow():
    # 1. Fetch questions for percentages
    q_resp = client.get("/api/questions?topic_id=percentages&limit=5")
    assert q_resp.status_code == 200
    questions = q_resp.json()
    assert len(questions) > 0
    q1 = questions[0]
    q_id = q1["id"]

    # 2. Test Progressive Hints
    h_resp = client.post(f"/api/questions/{q_id}/hints", json={"hint_level": 1})
    assert h_resp.status_code == 200
    assert h_resp.json()["hint_level"] == 1

    # 3. Test Step Tutor
    step_resp = client.post(f"/api/questions/{q_id}/step_tutor", json={"step_name": "understand"})
    assert step_resp.status_code == 200
    assert step_resp.json()["step"] == "understand"

    # 4. Submit Answer
    sub_resp = client.post(f"/api/questions/{q_id}/submit", json={
        "user_id": "test_learner",
        "submitted_answer": "100",
        "time_spent": 15.0,
        "hints_used": 0
    })
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    assert "is_correct" in sub_data
    assert "reference_solution" in sub_data

def test_api_dashboard():
    response = client.get("/api/analytics/dashboard?user_id=default_user")
    assert response.status_code == 200
    data = response.json()
    assert data["total_repository_questions"] >= 1800
    assert "overall_accuracy" in data
    assert "recommended_next_lesson" in data

def test_api_mock_test_flow():
    # Start mock test
    start_resp = client.post("/api/mock_tests/start", json={
        "user_id": "test_learner",
        "profile_id": "tcs_nqt"
    })
    assert start_resp.status_code == 200
    test_data = start_resp.json()
    assert test_data["total_questions"] > 0
    assert "session_id" in test_data
    sess_id = test_data["session_id"]
    test_qs = test_data["questions"]

    # Submit mock test
    sub_items = [
        {
            "question_id": q["id"],
            "submitted_answer": "10",
            "time_spent": 30.0,
            "is_marked_for_review": False
        }
        for q in test_qs[:3]
    ]
    sub_resp = client.post("/api/mock_tests/submit", json={
        "user_id": "test_learner",
        "session_id": sess_id,
        "answers": sub_items
    })
    assert sub_resp.status_code == 200
    result = sub_resp.json()
    assert "score" in result
    assert "accuracy" in result
