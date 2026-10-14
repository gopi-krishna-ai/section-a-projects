import os
import json
import httpx
from typing import Dict, Any, List, Optional
from backend.config import settings

class TutorService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.gemini_key = settings.GEMINI_API_KEY
        self.openai_key = settings.OPENAI_API_KEY
        self.model = settings.LLM_MODEL

    def get_progressive_hint(
        self,
        question_text: str,
        reference_solution: str,
        correct_answer: str,
        hint_level: int, # 1, 2, 3, or 4
        current_attempt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Returns progressive hint 1, 2, 3 or full solution.
        1: Clue & Objective
        2: Relevant Formula or Principle
        3: First computational or logical step
        4: Full verified solution
        """
        sol_lines = [l.strip() for l in reference_solution.split('\n') if l.strip()]

        if hint_level == 1:
            clue = "Carefully identify the given variables and what is being asked."
            if "%" in question_text:
                clue = "Identify the baseline (100% reference amount) before calculating changes."
            elif "series" in question_text.lower() or "next number" in question_text.lower():
                clue = "Look at the differences between consecutive elements. Are they increasing steadily or multiplying?"
            elif "speed" in question_text.lower() or "distance" in question_text.lower():
                clue = "Check if units match (km/h vs m/s). Speed = Distance / Time."
            return {
                "hint_level": 1,
                "title": "Hint 1: Spot the Key Clue",
                "content": clue,
                "educational_takeaway": "Always write down 'Given' and 'To Find' before writing any calculations."
            }

        elif hint_level == 2:
            formula = "Recall the standard relation connecting your given parameters."
            for line in sol_lines:
                if any(k in line.lower() for k in ["formula", "=", "ratio", "let", "profit", "work", "difference"]):
                    formula = f"Governing equation/relation: {line}"
                    break
            return {
                "hint_level": 2,
                "title": "Hint 2: Core Formula & Relationship",
                "content": formula,
                "educational_takeaway": "Understanding why the formula works avoids memorization mistakes."
            }

        elif hint_level == 3:
            first_step = sol_lines[0] if sol_lines else "Set up the initial equation with your variables."
            return {
                "hint_level": 3,
                "title": "Hint 3: First Step Calculation",
                "content": f"Begin with this step: {first_step}",
                "educational_takeaway": "Now complete the remaining arithmetic to solve for the target value."
            }

        else: # Hint level 4 or Full
            return {
                "hint_level": 4,
                "title": "Full Verified Solution",
                "content": reference_solution,
                "correct_answer": correct_answer,
                "educational_takeaway": "Review each step of this solution to understand the pattern for future questions."
            }

    def generate_step_by_step_guidance(
        self,
        question_text: str,
        stimulus_context: Optional[str],
        reference_solution: str,
        correct_answer: str,
        step_name: str # understand, identify, plan, solve, verify, generalize, transfer
    ) -> Dict[str, Any]:
        """
        Pedagogical step-by-step tutor:
        - understand: Deconstructs question phrasing
        - identify: Distinguishes given values vs requested result
        - plan: Proposes solving strategy (LCM method, algebra, substitution)
        - solve: Guided step-by-step walk
        - verify: Sanity checks and bounds
        - generalize: Pattern cues for future placement tests
        - transfer: Generates a similar practice problem testing the same skill
        """
        sol_lines = [l.strip() for l in reference_solution.split('\n') if l.strip()]

        if step_name == "understand":
            return {
                "step": "understand",
                "title": "Step A: Understand the Question",
                "content": f"The question states: '{question_text}'. What is the exact goal? Are there any subtle conditions or constraints?",
                "guiding_question": "Can you summarize in your own words what quantity we need to find?"
            }

        elif step_name == "identify":
            return {
                "step": "identify",
                "title": "Step B: Identify Given vs Required",
                "content": "List all numbers, percentages, or terms provided in the question. Ensure all units (time, distance, currency) are converted to a common unit system.",
                "guiding_question": "What information is given, and what are the units?"
            }

        elif step_name == "plan":
            return {
                "step": "plan",
                "title": "Step C: Choose the Best Approach",
                "content": "For this category, consider whether a direct formula, the unitary method, an LCM shortcut, or algebra is the cleanest and fastest method.",
                "guiding_question": "Which method will minimize calculation errors under exam time pressure?"
            }

        elif step_name == "solve":
            return {
                "step": "solve",
                "title": "Step D: Step-by-Step Solution",
                "content": reference_solution,
                "guiding_question": "Do each step one at a time on your scratchpad."
            }

        elif step_name == "verify":
            return {
                "step": "verify",
                "title": "Step E: Verify & Sanity Check",
                "content": f"Does the result ({correct_answer}) make intuitive sense? For instance, if finding speed, is it positive and realistic? If finding a discount, is SP < CP?",
                "guiding_question": "Plug the answer back into the original condition to confirm both sides balance."
            }

        elif step_name == "generalize":
            return {
                "step": "generalize",
                "title": "Step F: How to Spot This in Placement Tests",
                "content": "Whenever you encounter similar keywords, remember the governing pattern. Placement exams often change only the numbers while keeping this exact problem structure.",
                "guiding_question": "What clue in the wording will immediately trigger this approach in your next test?"
            }

        elif step_name == "transfer":
            # Deterministic variation of question
            transfer_q = f"Transfer Exercise: If the numbers in this problem were scaled by 2 (e.g., values doubled), how would you set up the equation to solve it?"
            return {
                "step": "transfer",
                "title": "Step G: Transfer Challenge",
                "content": transfer_q,
                "guiding_question": "Apply the exact same concept to test your independent retention."
            }

        return {
            "step": "general",
            "title": "Tutor Guidance",
            "content": reference_solution,
            "guiding_question": "What part of this problem feels most challenging?"
        }

    async def get_ai_explanation(
        self,
        question_text: str,
        reference_solution: str,
        correct_answer: str,
        learner_query: str
    ) -> Dict[str, Any]:
        """
        Calls configured AI Provider (Gemini or OpenAI) with fallback to verified local teaching.
        """
        # If Gemini API key is configured
        if self.gemini_key and (self.provider == "gemini" or not self.openai_key):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.gemini_key}"
                prompt = (
                    f"You are a patient, rigorous Aptitude Coach for college placements.\n"
                    f"Verified Question: {question_text}\n"
                    f"Verified Solution: {reference_solution}\n"
                    f"Verified Answer: {correct_answer}\n\n"
                    f"Student Query: '{learner_query}'\n\n"
                    f"Provide a concise, educational explanation. Help the student understand WHY the method works "
                    f"and how to avoid traps. Do not contradict the verified reference solution."
                )
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        url,
                        json={"contents": [{"parts": [{"text": prompt}]}]},
                        headers={"Content-Type": "application/json"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return {
                            "provider": "gemini",
                            "explanation": text,
                            "source": "AI-Assisted Educational Tutor"
                        }
            except Exception as e:
                # Graceful fallback to verified solution
                pass

        # Deterministic High-Quality Fallback
        return {
            "provider": "local_pedagogical_engine",
            "explanation": (
                f"### Core Pedagogical Breakdown\n\n"
                f"**Question Analysis**: {question_text}\n\n"
                f"**Step-by-Step Approach**:\n{reference_solution}\n\n"
                f"**Key Takeaway**: The correct result is **{correct_answer}**. "
                f"Remember to always verify the given base and units before executing the final arithmetic."
            ),
            "source": "Verified Repository Reference Engine"
        }

tutor_service = TutorService()
