import pytest
import os
import sys
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal, Base, engine
from backend.services.executor import execute_python_code, run_problem_test_cases
from backend.services.diagnosis import diagnose_code_failure
from backend.services.seed_data import seed_database

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()
    yield

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_code_executor_basic():
    code = "print(2 + 2)"
    res = execute_python_code(code)
    assert res["exit_code"] == 0
    assert "4" in res["stdout"]
    assert res["error_type"] is None

def test_code_executor_timeout_protection():
    # Infinite loop must trigger Timeout error rather than hanging
    code = "while True: pass"
    res = execute_python_code(code)
    assert res["error_type"] == "Timeout"
    assert "Time Limit Exceeded" in res["stderr"]

def test_problem_test_case_runner():
    code = """
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        comp = target - n
        if comp in seen:
            return [seen[comp], i]
        seen[n] = i
    return []
"""
    test_cases = [
        {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected_output": [0, 1]},
        {"input": {"nums": [3, 2, 4], "target": 6}, "expected_output": [1, 2]}
    ]
    res = run_problem_test_cases(code, test_cases)
    assert res["status"] == "Passed"
    assert res["passes_count"] == 2
    assert res["total_tests"] == 2

def test_mistake_diagnosis_recursion():
    diag = diagnose_code_failure(
        code="def f(x): return f(x+1)",
        status="Runtime Error",
        error_output="RecursionError: maximum recursion depth exceeded"
    )
    assert diag["error_category"] == "Incorrect recursion base case"
    assert "terminating condition" in diag["what_went_wrong"]

def test_mistake_diagnosis_off_by_one():
    diag = diagnose_code_failure(
        code="for i in range(len(arr) + 1): pass",
        status="Runtime Error",
        error_output="IndexError: list index out of range"
    )
    assert diag["error_category"] == "Off-by-one error"

def test_auth_and_demo_users():
    res = client.get("/api/auth/demo_users")
    assert res.status_code == 200
    demos = res.json()
    assert len(demos) >= 4
    usernames = [d["username"] for d in demos]
    assert "py_ninja" in usernames
    assert "algo_master" in usernames

    # Switch demo
    switch_res = client.post("/api/auth/switch_demo", json={"username": "py_ninja"})
    assert switch_res.status_code == 200
    token_data = switch_res.json()
    assert "token" in token_data
    assert token_data["user"]["username"] == "py_ninja"

def test_curriculum_and_problems_endpoints():
    res = client.get("/api/curriculum/topics")
    assert res.status_code == 200
    topics = res.json()
    assert len(topics) >= 5

    prob_res = client.get("/api/problems")
    assert prob_res.status_code == 200
    problems = prob_res.json()
    assert len(problems) >= 3
