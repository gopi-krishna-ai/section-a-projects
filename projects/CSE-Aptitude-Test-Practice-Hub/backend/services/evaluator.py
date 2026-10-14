import re
import math
from typing import Tuple, Dict, Any, Optional

def normalize_text(text: str) -> str:
    """Strip formatting, markdown, punctuation, and extra whitespace."""
    if not text:
        return ""
    # Strip markdown backticks, bold, italic
    cleaned = re.sub(r'[`*_~]', '', text)
    # Strip outer quotes
    cleaned = cleaned.strip("\"' \t\r\n")
    # Collapse multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def extract_numeric_value(text: str) -> Optional[float]:
    """Extract numeric value considering decimals, percentages, and currencies."""
    cleaned = text.strip()
    # Remove currency symbols and comma separators
    cleaned = re.sub(r'[$€£₹,]', '', cleaned)
    # Remove percentage signs
    cleaned = cleaned.replace('%', '')
    # Remove trailing unit words
    cleaned = re.sub(r'\s*(units?|m/s|km/h|km|m|cm|days?|hours?|hrs?|mins?|sec|seconds?|kg|g|dollars?|cents?)\.?$', '', cleaned, flags=re.IGNORECASE).strip()
    
    # Check fraction e.g. "1/2", "3/4"
    frac_match = re.match(r'^(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)$', cleaned)
    if frac_match:
        try:
            num = float(frac_match.group(1))
            den = float(frac_match.group(2))
            if den != 0:
                return num / den
        except ValueError:
            pass

    # Direct float conversion
    try:
        return float(cleaned)
    except ValueError:
        pass

    # Check if number appears embedded: e.g. "Answer: 100" or "= 100"
    num_match = re.search(r'[-+]?\d+(?:\.\d+)?', cleaned)
    if num_match:
        try:
            return float(num_match.group(0))
        except ValueError:
            pass

    return None

def normalize_ratio(text: str) -> Optional[Tuple[float, float]]:
    """Normalizes ratios like '9:10', '9 : 10', '9/10'."""
    cleaned = text.replace(' ', '')
    m = re.match(r'^(\d+(?:\.\d+)?)(?::|/)(\d+(?:\.\d+)?)$', cleaned)
    if m:
        try:
            a = float(m.group(1))
            b = float(m.group(2))
            if b != 0:
                return (a, b)
        except ValueError:
            pass
    return None

def evaluate_answer(
    submitted: str,
    correct: str,
    question_type: str = "short_answer",
    options: Optional[list] = None
) -> Dict[str, Any]:
    """
    Deterministically evaluates submitted answer against verified correct answer.
    Returns:
    {
        "is_correct": bool,
        "normalized_submitted": str,
        "normalized_correct": str,
        "match_type": str,
        "feedback": str
    }
    """
    sub_raw = submitted.strip() if submitted else ""
    cor_raw = correct.strip() if correct else ""

    if not sub_raw:
        return {
            "is_correct": False,
            "normalized_submitted": "",
            "normalized_correct": cor_raw,
            "match_type": "empty",
            "feedback": "No answer was provided."
        }

    sub_norm = normalize_text(sub_raw)
    cor_norm = normalize_text(cor_raw)

    # 1. Exact string match (case-insensitive)
    if sub_norm.lower() == cor_norm.lower():
        return {
            "is_correct": True,
            "normalized_submitted": sub_norm,
            "normalized_correct": cor_norm,
            "match_type": "exact",
            "feedback": "Correct! Perfect match."
        }

    # 2. MCQ Option matching (e.g. "B" vs "B) Plentiful")
    if question_type == "mcq" or (options and len(options) > 0):
        # Extract letter from submitted: e.g. "B", "b", "B)", "(B)"
        sub_letter_m = re.match(r'^\(?([A-Da-d])\)?(?:\s|$|\.|\))', sub_norm)
        cor_letter_m = re.match(r'^\(?([A-Da-d])\)?(?:\s|$|\.|\))', cor_norm)

        sub_letter = sub_letter_m.group(1).upper() if sub_letter_m else None
        cor_letter = cor_letter_m.group(1).upper() if cor_letter_m else None

        if sub_letter and cor_letter and sub_letter == cor_letter:
            return {
                "is_correct": True,
                "normalized_submitted": sub_letter,
                "normalized_correct": cor_norm,
                "match_type": "mcq_letter",
                "feedback": f"Correct! Option {sub_letter} is the right choice."
            }

        # Check if submitted text matches option text directly
        if cor_letter and options:
            for opt in options:
                opt_norm = normalize_text(opt)
                if opt_norm.startswith(f"{cor_letter})"):
                    opt_content = re.sub(r'^[A-D]\)\s*', '', opt_norm).strip().lower()
                    if sub_norm.lower() == opt_content:
                        return {
                            "is_correct": True,
                            "normalized_submitted": sub_norm,
                            "normalized_correct": cor_norm,
                            "match_type": "mcq_content",
                            "feedback": f"Correct! '{sub_norm}' corresponds to option {cor_letter}."
                        }

    # 3. Numeric & Metric comparison
    sub_num = extract_numeric_value(sub_norm)
    cor_num = extract_numeric_value(cor_norm)

    if sub_num is not None and cor_num is not None:
        # Check relative and absolute tolerance (1e-3 or 0.1%)
        abs_diff = abs(sub_num - cor_num)
        rel_diff = abs_diff / (abs(cor_num) + 1e-9)
        if abs_diff < 0.01 or rel_diff < 0.005:
            return {
                "is_correct": True,
                "normalized_submitted": str(sub_num),
                "normalized_correct": str(cor_num),
                "match_type": "numeric_tolerance",
                "feedback": f"Correct! Numerically matches the verified answer ({cor_num})."
            }

    # 4. Ratio equivalence: e.g. 9:10 == 9/10 == 18:20
    sub_ratio = normalize_ratio(sub_norm)
    cor_ratio = normalize_ratio(cor_norm)
    if sub_ratio and cor_ratio:
        r1 = sub_ratio[0] / sub_ratio[1]
        r2 = cor_ratio[0] / cor_ratio[1]
        if abs(r1 - r2) < 1e-4:
            return {
                "is_correct": True,
                "normalized_submitted": f"{sub_ratio[0]}:{sub_ratio[1]}",
                "normalized_correct": cor_norm,
                "match_type": "ratio_equivalent",
                "feedback": "Correct! The ratio is mathematically equivalent."
            }

    # 5. Sentence Correction & Punctuation invariant text
    # Strip all non-alphanumeric characters and lowercase
    sub_alpha = re.sub(r'[^a-zA-Z0-9]', '', sub_norm).lower()
    cor_alpha = re.sub(r'[^a-zA-Z0-9]', '', cor_norm).lower()
    if sub_alpha and sub_alpha == cor_alpha:
        return {
            "is_correct": True,
            "normalized_submitted": sub_norm,
            "normalized_correct": cor_norm,
            "match_type": "alphanumeric_match",
            "feedback": "Correct! Grammatical text matches perfectly."
        }

    # 6. Containment check for short answer / key terms
    if len(cor_norm) > 1 and cor_norm.lower() in sub_norm.lower():
        # Only accept if submitted is not overly broad
        if len(sub_norm) <= len(cor_norm) * 2.5:
            return {
                "is_correct": True,
                "normalized_submitted": sub_norm,
                "normalized_correct": cor_norm,
                "match_type": "containment",
                "feedback": "Correct! Key solution identified."
            }

    return {
        "is_correct": False,
        "normalized_submitted": sub_norm,
        "normalized_correct": cor_norm,
        "match_type": "mismatch",
        "feedback": f"Incorrect. Your answer: '{sub_norm}'. Expected: '{cor_norm}'."
    }
