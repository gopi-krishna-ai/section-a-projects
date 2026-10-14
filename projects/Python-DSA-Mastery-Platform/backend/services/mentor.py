import os
import json
from typing import Dict, Any, Optional, List
from backend.config import settings

def get_socratic_hint(
    problem: Any,
    hint_level: int,
    user_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns progressive hints from Level 1 to 6.
    Level 1: Clarify
    Level 2: Direct attention
    Level 3: Suggest pattern
    Level 4: Guide algorithm
    Level 5: Targeted debugging
    Level 6: Full explanation & reference solution
    """
    hints = problem.hints or []
    idx = max(0, min(hint_level - 1, 5))

    hint_titles = [
        "Clarification & Problem Understanding",
        "Key Observation & Constraint Focus",
        "Algorithmic Pattern Clue",
        "Algorithm Design & Pseudocode",
        "Targeted Debugging & Invariant Check",
        "Full Walkthrough & Complexity Proof"
    ]

    if idx < len(hints) and isinstance(hints[idx], dict):
        content = hints[idx].get("content") or hints[idx].get("text", "")
        title = hints[idx].get("title", hint_titles[idx])
    elif idx < len(hints) and isinstance(hints[idx], str):
        content = hints[idx]
        title = hint_titles[idx]
    else:
        # Fallback progressive hints based on problem metadata
        if idx == 0:
            content = f"Look at the inputs and outputs for '{problem.title}'. What is guaranteed about the input types? What are the edge boundaries?"
        elif idx == 1:
            constraints_str = ", ".join(problem.constraints or ["N <= 10^5"])
            content = f"Pay attention to the constraints: {constraints_str}. Notice that an O(N^2) brute-force might exceed the runtime limit. What value can be cached?"
        elif idx == 2:
            tags_str = ", ".join(problem.tags or ["hash_table"])
            content = f"Pattern clue: Consider using the '{tags_str}' pattern. How does storing seen elements in a hash structure reduce repetitive scans?"
        elif idx == 3:
            content = f"Algorithm step: 1. Initialize data structure. 2. Iterate through input once. 3. Check for complementary condition in O(1). 4. Return result immediately upon discovery."
        elif idx == 4:
            content = f"Debugging check: Have you checked the case where elements are duplicated or negative? Verify loop termination before indexing."
        else:
            content = f"Reference Solution:\\n```python\\n{problem.reference_solution}\\n```\\nTime Complexity: {problem.time_complexity}, Space Complexity: {problem.space_complexity}"
        title = hint_titles[idx]

    return {
        "level": idx + 1,
        "title": title,
        "content": content,
        "is_full_solution": (idx == 5)
    }

def ask_mentor(
    problem_title: str,
    user_code: str,
    query: str,
    error_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Socratic AI Coding Mentor with local rule fallback.
    """
    # Check if Gemini API is available
    if settings.GEMINI_API_KEY and settings.LLM_PROVIDER == "gemini":
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.LLM_MODEL)
            prompt = f"""You are a Socratic Computer Science & DSA Mentor.
Problem: {problem_title}
User Query: {query}
User Code:
{user_code}
Error / Stderr: {error_message or 'None'}

Rules:
1. Do NOT immediately provide the full code solution unless explicitly asked.
2. Guide the user by identifying assumptions, loop boundaries, or invariant violations.
3. Be concise, encouraging, and pedagogically rigorous.
"""
            resp = model.generate_content(prompt)
            return {
                "provider": "gemini",
                "response": resp.text
            }
        except Exception as e:
            pass # Fallback to local rule engine

    # Local Socratic rule engine
    advice = []
    if error_message:
        advice.append(f"Notice the runtime signal: `{error_message.strip()}`.")
        if "IndexError" in error_message:
            advice.append("Check if your loop index is running past `len - 1` or if pointers cross boundaries.")
        elif "KeyError" in error_message:
            advice.append("A dictionary lookup occurred before the key was populated. Consider checking `key in dict` or using `dict.get()`.")
        elif "TypeError" in error_message:
            advice.append("A function received an unexpected type. Inspect the return types and input arguments.")
    else:
        advice.append(f"Regarding '{problem_title}':")
        if "for " in user_code and "for " in user_code.split("for ")[-1]:
            advice.append("You have nested loops. Can you precompute values in a dictionary or frequency map to achieve O(N) linear time?")
        else:
            advice.append("Trace your variable state with a 3-element example on paper. What invariant must remain true at the end of every loop iteration?")

    advice.append("Try printing intermediate values or running a single test case through the dry-run table to locate the divergence.")

    return {
        "provider": "local_socratic_engine",
        "response": "\\n\\n".join(advice)
    }
