import re
from typing import Dict, Any, Optional, List

MISTAKE_TAXONOMY_22 = [
    "Misunderstood the problem",
    "Missed a constraint",
    "Chose the wrong algorithm",
    "Failed to identify a useful pattern",
    "Incorrect data-structure choice",
    "Incorrect mathematical reasoning",
    "Incorrect pseudocode",
    "Logical error",
    "Incorrect loop boundary",
    "Off-by-one error",
    "Incorrect variable update",
    "Incorrect recursion base case",
    "State or invariant error",
    "Edge-case failure",
    "Syntax error",
    "Type or data-conversion error",
    "Incorrect complexity analysis",
    "Inefficient solution",
    "Incorrect assumption",
    "Poor debugging approach",
    "Time-management problem",
    "Unknown or insufficient evidence"
]

def diagnose_code_failure(
    code: str,
    status: str,
    error_output: Optional[str] = None,
    failing_test_case: Optional[Dict[str, Any]] = None,
    time_limit_exceeded: bool = False
) -> Dict[str, Any]:
    """
    Analyzes submitted code, execution errors, and failing test cases against the 22 mistake taxonomies.
    """
    category = "Logical error"
    what_went_wrong = "The function produced an incorrect output for the given input."
    why_it_went_wrong = "The algorithmic steps did not transform the input into the expected invariant."
    how_to_avoid = "Trace the state variables step-by-step using a small manual example before coding."
    corrective_check = {
        "title": "State Invariant Trace",
        "prompt": "Dry-run with a 3-element input: verify the variable values after each iteration."
    }

    if time_limit_exceeded or status == "Timeout":
        category = "Inefficient solution"
        what_went_wrong = "Code execution exceeded the 4.0s CPU time limit."
        why_it_went_wrong = "Likely using an O(N^2) or exponential algorithm where an O(N) or O(N log N) approach is required by constraints, or caught in an infinite loop."
        how_to_avoid = "Check the input constraint N. If N <= 10^5, aim for O(N) or O(N log N) using hash maps or sorting instead of nested brute-force loops."
        corrective_check = {
            "title": "Complexity Filter Check",
            "prompt": "Identify any nested loops: can one loop be replaced with a dictionary lookup in O(1)?"
        }
        return {
            "error_category": category,
            "what_went_wrong": what_went_wrong,
            "why_it_went_wrong": why_it_went_wrong,
            "how_to_avoid": how_to_avoid,
            "corrective_exercise": corrective_check
        }

    err = (error_output or "").lower()

    if "recursionerror" in err or "maximum recursion depth" in err:
        category = "Incorrect recursion base case"
        what_went_wrong = "Recursion depth exceeded without hitting a terminating condition."
        why_it_went_wrong = "The base case is either missing, never satisfied, or the recursive call is not making progress toward the base case."
        how_to_avoid = "Always write and verify the base case first (e.g. if root is None or index == len(arr)) and ensure parameters decrease or advance."
        corrective_check = {
            "title": "Base Case Audit",
            "prompt": "Write down the smallest possible valid input and verify whether your function immediately returns without recurring."
        }
    elif "indexerror" in err or "string index out of range" in err or "list index out of range" in err:
        if "len(" in code and ("<=" in code or "+1" in code or "+ 1" in code or re.search(r"\+\s*1", code)):
            category = "Off-by-one error"
            what_went_wrong = "Accessed an array index equal to or exceeding the collection length."
            why_it_went_wrong = "Python 0-indexed sequences end at len(arr) - 1. A loop condition like i <= len(arr) attempts to read out-of-bounds memory."
            how_to_avoid = "Use 'range(len(arr))' or 'while i < len(arr)'. Never use '<=' with len(arr)."
        else:
            category = "Incorrect loop boundary"
            what_went_wrong = "Out of range index dereferenced during iteration."
            why_it_went_wrong = "Pointer movement (left/right) pushed an index beyond 0 or len(arr)."
            how_to_avoid = "Add boundary guards like 'while left < right:' or verify indices before subscripting."
    elif "typeerror" in err:
        category = "Type or data-conversion error"
        what_went_wrong = f"Type mismatch encountered: {error_output}"
        why_it_went_wrong = "Attempted operation between incompatible types (e.g. int and str, or unsubscriptable NoneType)."
        how_to_avoid = "Use Python type annotations and verify return types before accessing attributes."
    elif "keyerror" in err:
        category = "Incorrect data-structure choice"
        what_went_wrong = "Dictionary key lookup failed on non-existent key."
        why_it_went_wrong = "Accessed dict[k] directly without checking existence or using dict.get(k, default) / collections.defaultdict."
        how_to_avoid = "Use collections.defaultdict(int) for frequency counting to avoid explicit existence checks."
    elif "syntaxerror" in err or "indentationerror" in err:
        category = "Syntax error"
        what_went_wrong = "Invalid Python syntax or indentation structure."
        why_it_went_wrong = "Missing colon, unclosed bracket, or mismatched whitespace indentation."
        how_to_avoid = "Keep indentation strictly consistent at 4 spaces and check colon placement after def, for, if, while."
    elif failing_test_case:
        tc_in = str(failing_test_case.get("input", ""))
        tc_expected = str(failing_test_case.get("expected_output", ""))
        tc_actual = str(failing_test_case.get("actual_output", ""))

        # Check for empty or single element input edge case
        if tc_in in ["[]", "''", '""', "[0]", "0", "None"]:
            category = "Edge-case failure"
            what_went_wrong = f"Function failed on minimal boundary/edge-case input: {tc_in}"
            why_it_went_wrong = "Algorithm implicitly assumed non-empty or multi-element input without checking edge conditions."
            how_to_avoid = "Handle empty collections or boundary lengths (len == 0, len == 1) at the top of the function as early guard clauses."
        elif tc_expected.isdigit() and tc_actual.isdigit() and abs(int(tc_expected) - int(tc_actual)) == 1:
            category = "Off-by-one error"
            what_went_wrong = f"Output {tc_actual} is off by exactly 1 from expected {tc_expected}."
            why_it_went_wrong = "Loop range was either inclusive when it should be exclusive, or window length was calculated as (right - left) instead of (right - left + 1)."
            how_to_avoid = "Remember: length of inclusive subarray [left, right] is (right - left + 1)."
        elif ("{" in code or "dict" in code) and "set" not in code and "hash" not in code:
            category = "Failed to identify a useful pattern"
            what_went_wrong = "Expected optimal output not achieved with current approach."
            why_it_went_wrong = "Problem pattern may be Two Pointers, Sliding Window, or Prefix Sums rather than nested scanning."
            how_to_avoid = "Recognize problem archetypes: contiguous subarrays -> Sliding Window or Prefix Sum; sorted pairs -> Two Pointers."

    return {
        "error_category": category,
        "what_went_wrong": what_went_wrong,
        "why_it_went_wrong": why_it_went_wrong,
        "how_to_avoid": how_to_avoid,
        "corrective_exercise": corrective_check
    }
