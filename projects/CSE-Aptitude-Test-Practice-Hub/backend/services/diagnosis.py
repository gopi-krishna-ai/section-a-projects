import re
from typing import Dict, Any, Optional

ERROR_TAXONOMIES = [
    "Concept misunderstanding",
    "Formula selection error",
    "Question interpretation error",
    "Incorrect setup",
    "Calculation or arithmetic error",
    "Unit conversion error",
    "Logical reasoning error",
    "Incomplete solution",
    "Incorrect shortcut",
    "Time-management problem",
    "Guessing or insufficient evidence",
    "Unclassified error"
]

def diagnose_mistake(
    question_text: str,
    submitted_answer: str,
    correct_answer: str,
    reference_solution: str,
    category: str,
    time_spent: float = 0.0,
    hints_used: int = 0,
    scratchpad_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes an incorrect attempt to categorize the error and generate actionable remediation.
    """
    sub_raw = submitted_answer.strip()
    cor_raw = correct_answer.strip()
    
    # 1. Check for hasty attempt or guessing (< 4 seconds or empty/random)
    if time_spent > 0 and time_spent < 4.0 and hints_used == 0:
        return {
            "error_category": "Guessing or insufficient evidence",
            "what_went_wrong": "The answer was submitted very quickly (under 4 seconds) without working through the problem steps.",
            "why_it_went_wrong": "Impulsive guessing under placement time pressure often leads to avoidable errors on solvable questions.",
            "correct_reasoning": f"Take 20-30 seconds to break down the problem into given values and target variable. Reference solution: {reference_solution[:200]}...",
            "how_to_avoid": "Pause for at least 15 seconds to identify what is given and what formula connects them before selecting an answer.",
            "corrective_exercise": {
                "prompt": "Identify the primary given quantity and target in this question before calculating.",
                "hint": "Check the numbers and units provided."
            }
        }

    # 2. Check for time management problem (> 180 seconds on basic/intermediate question)
    if time_spent > 180.0:
        return {
            "error_category": "Time-management problem",
            "what_went_wrong": f"You spent over {int(time_spent // 60)} minutes wrestling with this single question.",
            "why_it_went_wrong": "Getting stuck in complicated arithmetic without switching to a faster formulation or structured method.",
            "correct_reasoning": f"Standard placement questions are designed to be solved within 60-90 seconds using clean shortcuts or unitary methods.",
            "how_to_avoid": "If no clear path emerges after 45 seconds, review the formula reference or request Progressive Hint 1.",
            "corrective_exercise": {
                "prompt": "Review the LCM or ratio shortcut in the reference solution.",
                "hint": "Notice how working with integer units avoids fractional slowdowns."
            }
        }

    # 3. Numeric ratio / off-by-factor / arithmetic errors
    try:
        from backend.services.evaluator import extract_numeric_value
        sub_num = extract_numeric_value(sub_raw)
        cor_num = extract_numeric_value(cor_raw)
        if sub_num is not None and cor_num is not None and cor_num != 0:
            ratio = sub_num / cor_num
            # Factor of 10 or 100 error -> Unit conversion or decimal point slip
            if abs(ratio - 10) < 0.05 or abs(ratio - 0.1) < 0.005 or abs(ratio - 100) < 0.1 or abs(ratio - 0.01) < 0.001:
                return {
                    "error_category": "Unit conversion error",
                    "what_went_wrong": f"Your calculated answer ({sub_num}) is off by a power of 10 from the correct value ({cor_num}).",
                    "why_it_went_wrong": "A decimal placement slip or missing unit conversion (e.g. m/s to km/h, percentage to decimal, or grams to kg).",
                    "correct_reasoning": f"Carefully track units at each step: {reference_solution[:180]}...",
                    "how_to_avoid": "Explicitly write the conversion factors (e.g. multiply by 5/18 for km/h to m/s, divide by 100 for percent) before performing operations.",
                    "corrective_exercise": {
                        "prompt": f"Verify whether your final step multiplied or divided by 10 or 100.",
                        "hint": "Double check percentage conversion."
                    }
                }
            # Off by 2x or 0.5x -> formula factor error (e.g. radius vs diameter, triangle 1/2 factor)
            if abs(ratio - 2.0) < 0.05 or abs(ratio - 0.5) < 0.005:
                return {
                    "error_category": "Formula selection error",
                    "what_went_wrong": f"Your answer ({sub_num}) is exactly double or half of the correct answer ({cor_num}).",
                    "why_it_went_wrong": "Likely missed a factor of 2 in the governing formula (e.g. diameter vs radius, or 1/2 base × height, or round-trip vs one-way distance).",
                    "correct_reasoning": f"The governing relation requires: {reference_solution[:180]}...",
                    "how_to_avoid": "State whether the problem asks for a single trip, round trip, radius, or diameter before plugging numbers into formulas.",
                    "corrective_exercise": {
                        "prompt": "Re-read the question's final clause to confirm the exact unit requested.",
                        "hint": "Check if one-way or two-way/round-trip was asked."
                    }
                }
            # Close value error -> Calculation or arithmetic error
            if abs(sub_num - cor_num) < max(5, abs(cor_num) * 0.15):
                return {
                    "error_category": "Calculation or arithmetic error",
                    "what_went_wrong": f"Your response ({sub_num}) was very close to the actual value ({cor_num}), but contained a computation slip.",
                    "why_it_went_wrong": "An intermediate addition, subtraction, or simplification mistake while the overall problem setup was likely correct.",
                    "correct_reasoning": f"Step-by-step arithmetic check: {reference_solution[:200]}...",
                    "how_to_avoid": "Use scratchpad breakdown (e.g. splitting 15% into 10% + 5%) rather than mental approximations.",
                    "corrective_exercise": {
                        "prompt": f"Recalculate the last multiplication or division: verify against {cor_num}.",
                        "hint": "Check simple multiplication tables."
                    }
                }
    except Exception:
        pass

    # 4. Verbal Ability & Sentence errors
    if category == "Verbal Ability":
        if "Correct" in question_text:
            return {
                "error_category": "Question interpretation error",
                "what_went_wrong": "The grammar or tense correction did not accurately resolve the underlying grammatical flaw.",
                "why_it_went_wrong": "Overlooking subject-verb agreement, plural irregularities, or tense consistency in the original clause.",
                "correct_reasoning": f"Solution: {reference_solution}",
                "how_to_avoid": "Isolate the subject noun and its main verb first to verify number agreement (singular vs plural).",
                "corrective_exercise": {
                    "prompt": "Identify the subject and verb in the original sentence.",
                    "hint": "Look for third-person singular markers."
                }
            }
        return {
            "error_category": "Concept misunderstanding",
            "what_went_wrong": f"Selected '{sub_raw}', whereas the intended context demands '{cor_raw}'.",
            "why_it_went_wrong": "Confusion between words with similar phonetic roots or misjudging subtle positive/negative connotations.",
            "correct_reasoning": f"Explanation: {reference_solution}",
            "how_to_avoid": "Substitute the chosen word back into the full context sentence to test if the tone and meaning remain coherent.",
            "corrective_exercise": {
                "prompt": f"Write down the precise definition of {cor_raw}.",
                "hint": "Notice whether the word has a positive or negative tone."
            }
        }

    # 5. Logical & Series errors
    if category in ["Logical Reasoning", "Abstract Reasoning"]:
        return {
            "error_category": "Logical reasoning error",
            "what_went_wrong": f"Your deduced progression yielded '{sub_raw}', while the governing pattern produces '{cor_raw}'.",
            "why_it_went_wrong": "Assuming a single linear difference without testing if differences are growing, alternating, or squaring.",
            "correct_reasoning": f"Pattern explanation: {reference_solution}",
            "how_to_avoid": "Always test your hypothesis against at least TWO consecutive pairs before predicting the next element.",
            "corrective_exercise": {
                "prompt": "Write down the differences between each pair of terms in the sequence.",
                "hint": "Check whether the differences themselves form an arithmetic or geometric sequence."
            }
        }

    # 6. Default Fallback
    return {
        "error_category": "Incorrect setup",
        "what_went_wrong": f"Your entered answer '{sub_raw}' does not match the verified result '{cor_raw}'.",
        "why_it_went_wrong": "The initial equation or translation from words into mathematical variables was set up incorrectly.",
        "correct_reasoning": f"Correct approach: {reference_solution}",
        "how_to_avoid": "Write down 'Given:' and 'To Find:' clearly before applying any formula.",
        "corrective_exercise": {
            "prompt": "Carefully read the reference solution and re-attempt the calculation on scratchpad.",
            "hint": "Follow each line of the reference solution."
        }
    }
