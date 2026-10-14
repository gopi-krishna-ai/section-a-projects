from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.models import (
    Topic, Lesson, Problem, DebugExercise, LogicPuzzle, User,
    ProblemSubmission, MistakeRecord, TopicMastery, RevisionSchedule
)
from backend.services.curriculum import (
    TOPICS_DATA, LESSONS_DATA, PROBLEMS_DATA, DEBUG_EXERCISES_DATA, LOGIC_PUZZLES_DATA
)
from backend.services.auth import seed_demo_users

def seed_database(db: Session):
    # 1. Seed Topics
    if db.query(Topic).count() == 0:
        for t_data in TOPICS_DATA:
            t = Topic(
                id=t_data["id"],
                track=t_data["track"],
                level=t_data["level"],
                title=t_data["title"],
                description=t_data["description"],
                order_index=t_data["order_index"],
                icon=t_data.get("icon", "Code"),
                prerequisites=t_data.get("prerequisites", [])
            )
            db.add(t)
        db.commit()

    # 2. Seed Lessons
    if db.query(Lesson).count() == 0:
        for l_data in LESSONS_DATA:
            l = Lesson(
                topic_id=l_data["topic_id"],
                title=l_data["title"],
                content=l_data["content"],
                runnable_snippets=l_data.get("runnable_snippets", []),
                key_takeaways=l_data.get("key_takeaways", []),
                order_index=l_data.get("order_index", 0)
            )
            db.add(l)
        db.commit()

    # 3. Seed Problems
    if db.query(Problem).count() == 0:
        for p_data in PROBLEMS_DATA:
            p = Problem(
                slug=p_data["slug"],
                title=p_data["title"],
                topic_id=p_data["topic_id"],
                track=p_data.get("track", "dsa"),
                difficulty=p_data["difficulty"],
                description=p_data["description"],
                constraints=p_data.get("constraints", []),
                examples=p_data.get("examples", []),
                starter_code=p_data["starter_code"],
                reference_solution=p_data["reference_solution"],
                brute_force_solution=p_data.get("brute_force_solution"),
                time_complexity=p_data.get("time_complexity", "O(N)"),
                space_complexity=p_data.get("space_complexity", "O(1)"),
                hints=p_data.get("hints", []),
                test_cases=p_data.get("test_cases", []),
                tags=p_data.get("tags", []),
                dry_run_steps=p_data.get("dry_run_steps", [])
            )
            db.add(p)
        db.commit()

    # 4. Seed Debug Exercises
    if db.query(DebugExercise).count() == 0:
        for d_data in DEBUG_EXERCISES_DATA:
            d = DebugExercise(
                title=d_data["title"],
                topic=d_data["topic"],
                difficulty=d_data["difficulty"],
                buggy_code=d_data["buggy_code"],
                bug_category=d_data["bug_category"],
                description=d_data["description"],
                test_cases=d_data.get("test_cases", []),
                hint=d_data["hint"],
                fixed_code=d_data["fixed_code"],
                explanation=d_data["explanation"]
            )
            db.add(d)
        db.commit()

    # 5. Seed Logic Puzzles
    if db.query(LogicPuzzle).count() == 0:
        for puz in LOGIC_PUZZLES_DATA:
            lp = LogicPuzzle(
                title=puz["title"],
                category=puz["category"],
                statement=puz["statement"],
                code_snippet=puz.get("code_snippet"),
                options=puz.get("options"),
                correct_answer=puz["correct_answer"],
                explanation=puz["explanation"],
                reasoning_pattern=puz["reasoning_pattern"]
            )
            db.add(lp)
        db.commit()

    # 6. Seed Demo Users
    seed_demo_users(db)

    # 7. Seed Sample Progress for py_ninja & algo_master
    now = datetime.now(timezone.utc)
    two_sum_p = db.query(Problem).filter_by(slug="two-sum").first()
    kadane_p = db.query(Problem).filter_by(slug="maximum-subarray").first()
    substr_p = db.query(Problem).filter_by(slug="longest-substring-without-repeating-characters").first()

    ninja_user = db.query(User).filter_by(id="user_pyninja").first()
    if ninja_user and db.query(ProblemSubmission).filter_by(user_id=ninja_user.id).count() == 0 and two_sum_p:
        # Submissions
        sub1 = ProblemSubmission(
            user_id=ninja_user.id,
            problem_id=two_sum_p.id,
            code=two_sum_p.reference_solution,
            status="Passed",
            passes_count=len(two_sum_p.test_cases),
            total_tests=len(two_sum_p.test_cases),
            execution_time_ms=28.4,
            is_independent=True,
            hints_used=0,
            submitted_at=now - timedelta(days=2)
        )
        db.add(sub1)

        if kadane_p:
            sub2 = ProblemSubmission(
                user_id=ninja_user.id,
                problem_id=kadane_p.id,
                code=kadane_p.reference_solution,
                status="Passed",
                passes_count=len(kadane_p.test_cases),
                total_tests=len(kadane_p.test_cases),
                execution_time_ms=35.1,
                is_independent=True,
                hints_used=1,
                submitted_at=now - timedelta(days=1)
            )
            db.add(sub2)

        if substr_p:
            # Add a mistake record for longest substring
            sub3 = ProblemSubmission(
                user_id=ninja_user.id,
                problem_id=substr_p.id,
                code="# Attempt with off-by-one window length\\ndef length_of_longest_substring(s): return len(set(s))",
                status="Failed",
                passes_count=2,
                total_tests=len(substr_p.test_cases),
                execution_time_ms=22.0,
                is_independent=False,
                hints_used=2,
                submitted_at=now - timedelta(hours=4)
            )
            db.add(sub3)
            db.flush()

            mistake = MistakeRecord(
                user_id=ninja_user.id,
                problem_id=substr_p.id,
                submission_id=sub3.id,
                error_category="Failed to identify a useful pattern",
                submitted_code=sub3.code,
                what_went_wrong="Used set(s) directly, destroying contiguous substring property.",
                why_it_went_wrong="Substrings must be contiguous; a global set counts all unique characters regardless of adjacency.",
                how_to_avoid="Use two-pointer sliding window to track contiguous substrings.",
                corrective_exercise={"title": "Sliding Window Check", "prompt": "Trace s='pwwkew': why is 'wke' valid but 'pwk' invalid?"},
                retest_status="pending",
                created_at=now - timedelta(hours=4)
            )
            db.add(mistake)

            rev = RevisionSchedule(
                user_id=ninja_user.id,
                problem_id=two_sum_p.id,
                interval_days=3,
                repetition_number=2,
                ease_factor=2.6,
                due_at=now - timedelta(hours=1),
                review_status="pending"
            )
            db.add(rev)

        # Topic Mastery
        tm1 = TopicMastery(
            user_id=ninja_user.id,
            topic_id="dsa_hashing",
            mastery_score=92.0,
            status="proficient",
            total_attempted=3,
            independent_solved=3,
            assisted_solved=0,
            last_practiced_at=now - timedelta(days=2)
        )
        db.add(tm1)

        tm2 = TopicMastery(
            user_id=ninja_user.id,
            topic_id="dsa_arrays_strings",
            mastery_score=68.5,
            status="developing_independence",
            total_attempted=4,
            independent_solved=2,
            assisted_solved=2,
            last_practiced_at=now - timedelta(hours=4)
        )
        db.add(tm2)

        db.commit()
