import os
import re
import glob
import json
from typing import List, Dict, Any, Optional

def clean_category_name(raw: str) -> str:
    # E.g. "01 Quantitative Aptitude (Numerical Ability)" -> "Quantitative Aptitude"
    cleaned = re.sub(r'^\d+\s*', '', raw)
    if '(' in cleaned:
        cleaned = cleaned.split('(')[0].strip()
    return cleaned

def clean_level_name(raw: str) -> str:
    # E.g. "01 Basic" -> "Basic", "02 Intermediate" -> "Intermediate", "03 Advance" -> "Advanced"
    cleaned = re.sub(r'^\d+\s*', '', raw).strip()
    if cleaned.lower() == 'advance':
        return 'Advanced'
    return cleaned

def clean_subtopic_name(raw: str) -> str:
    # Remove question numbers or suffixes like " (1-20)"
    cleaned = re.sub(r'\s*\(\d+[-–]\d+\)', '', raw).strip()
    return cleaned

def extract_mcq_options(q_text: str):
    """
    Extracts A) ... B) ... C) ... D) options if present.
    Returns (cleaned_stem, list_of_options) or (q_text, None)
    """
    # Check if there is an options pattern
    opt_pattern = r'([A-D]\))\s*([^A-D\n]+)'
    matches = list(re.finditer(opt_pattern, q_text))
    if len(matches) >= 3:
        first_opt_idx = matches[0].start()
        stem = q_text[:first_opt_idx].strip()
        options = []
        for m in matches:
            options.append(f"{m.group(1)} {m.group(2).strip()}")
        return stem, options
    return q_text, None

def detect_question_type(q_text: str, answer: str, options: Optional[List[str]]) -> str:
    if options and len(options) > 0:
        return "mcq"
    ans_clean = answer.strip()
    # Check if pure number or currency or percent
    if re.match(r'^[$\u20ac\u00a3]?\s*-?\d+(\.\d+)?%?\s*(units?|m/s|km/h|days?|hours?|mins?|sec)?$', ans_clean, re.IGNORECASE):
        return "numeric"
    if "Correct:" in q_text or "Correct the sentence:" in q_text:
        return "text_correction"
    return "short_answer"

def generate_progressive_hints(question: str, solution: str, answer: str) -> List[str]:
    """
    Derives educational progressive hints from the verified solution.
    Hint 1: Identifies key clue and objective
    Hint 2: Relevant formula or relation
    Hint 3: First computational or logical step
    """
    sol_lines = [l.strip() for l in solution.split('\n') if l.strip()]
    
    # Hint 1: What is given / clue
    hint1 = "Analyze what is given in the problem and identify what needs to be calculated."
    if "Let" in solution:
        hint1 = "Try defining an unknown variable for the required quantity (e.g. let the value be x)."
    elif "series" in solution.lower():
        hint1 = "Look closely at the differences, ratios, or operations between consecutive terms."
    elif "%" in question:
        hint1 = "Identify the base value and the percentage rate applied."

    # Hint 2: Formula or rule
    hint2 = "Recall the standard formula or definition that connects the given values."
    for line in sol_lines:
        if any(term in line.lower() for term in ["formula", "=", "ratio", "difference", "mean", "speed", "work", "profit"]):
            hint2 = f"Key relationship to apply: {line[:120]}"
            break

    # Hint 3: First calculation step
    hint3 = "Set up the initial equation or first operation."
    if len(sol_lines) > 1:
        hint3 = f"First step: {sol_lines[0][:150]}"
    elif len(sol_lines) == 1:
        hint3 = f"Consider: {sol_lines[0][:150]}"

    return [
        f"Clue: {hint1}",
        f"Concept & Formula: {hint2}",
        f"Method Step: {hint3}"
    ]

def parse_markdown_file(fpath: str, repo_root: str) -> List[Dict[str, Any]]:
    rel = os.path.relpath(fpath, repo_root)
    parts = rel.split(os.sep)
    raw_category = parts[0]
    raw_level = parts[1]
    
    category = clean_category_name(raw_category)
    level = clean_level_name(raw_level)
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.read().split('\n')
        
    questions = []
    current_subtopic = "General"
    current_context = ""
    
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        
        # Check subtopic heading
        if line.startswith('## '):
            current_subtopic = clean_subtopic_name(line.replace('## ', '').strip())
            current_context = ""
            i += 1
            continue
            
        # Check context block like **Table ...** or **Passage ...** or **Bar Graph ...**
        if (line.startswith('**Table') or line.startswith('**Passage') or 
            line.startswith('**Bar Graph') or line.startswith('**Chart') or 
            line.startswith('**Caselet') or line.startswith('**Line Graph')):
            ctx_lines = [line]
            i += 1
            while i < n and not re.match(r'^\s*\d+\.\s+\*\*Question\*\*', lines[i]) and not lines[i].startswith('## '):
                ctx_lines.append(lines[i])
                i += 1
            current_context = '\n'.join(ctx_lines).strip()
            continue
            
        # Question pattern
        m = re.match(r'^\s*(\d+)\.\s+\*\*Question\*\*:\s*(.*)', line)
        if m:
            q_num = int(m.group(1))
            q_text_first = m.group(2).strip()
            q_lines = [q_text_first] if q_text_first else []
            i += 1
            
            sol_lines = []
            ans_lines = []
            mode = 'question'
            
            while i < n:
                curr = lines[i]
                if re.match(r'^\s*\d+\.\s+\*\*Question\*\*', curr) or curr.startswith('## '):
                    break
                if curr.startswith('**Passage') or curr.startswith('**Table'):
                    break
                    
                if '**Solution**:' in curr:
                    mode = 'solution'
                    after = curr.split('**Solution**:', 1)[1].strip()
                    if after: sol_lines.append(after)
                elif '**Corrected**:' in curr:
                    mode = 'answer'
                    after = curr.split('**Corrected**:', 1)[1].strip()
                    if after: ans_lines.append(after)
                elif '**Answer**:' in curr:
                    # In Q100 of basic quant, **Answer**: appeared where **Solution**: was expected
                    if mode == 'question':
                        mode = 'solution'
                        after = curr.split('**Answer**:', 1)[1].strip()
                        if after: sol_lines.append(after)
                    else:
                        mode = 'answer'
                        after = curr.split('**Answer**:', 1)[1].strip()
                        if after: ans_lines.append(after)
                else:
                    if mode == 'question':
                        q_lines.append(curr)
                    elif mode == 'solution':
                        sol_lines.append(curr)
                    elif mode == 'answer':
                        if '</xaiArtifactEnd>' in curr or '```' in curr or '### How to Use' in curr:
                            pass
                        else:
                            ans_lines.append(curr)
                i += 1
                
            raw_q_text = '\n'.join(q_lines).strip()
            sol_text = '\n'.join(sol_lines).strip()
            ans_text = '\n'.join(ans_lines).strip()
            
            # Clean artifact leftovers from answer
            ans_text = re.sub(r'</xaiArtifactEnd>.*', '', ans_text, flags=re.DOTALL).strip()
            
            stem, options = extract_mcq_options(raw_q_text)
            q_type = detect_question_type(stem, ans_text, options)
            hints = generate_progressive_hints(stem, sol_text, ans_text)
            
            # Stable unique source ID
            cat_slug = re.sub(r'[^a-zA-Z0-9]+', '_', category.lower()).strip('_')
            level_slug = level.lower()
            source_id = f"{cat_slug}_{level_slug}_q{q_num}"
            
            questions.append({
                'source_id': source_id,
                'source_file': rel.replace('\\', '/'),
                'q_num': q_num,
                'category': category,
                'level': level,
                'subtopic': current_subtopic,
                'stimulus_context': current_context if current_context else None,
                'question_text': stem,
                'raw_question': raw_q_text,
                'options': options,
                'question_type': q_type,
                'correct_answer': ans_text,
                'reference_solution': sol_text,
                'hints': hints,
                'validation_status': 'verified' if (sol_text and ans_text) else 'flagged_review'
            })
            continue
        i += 1
        
    return questions

def parse_all_repository_questions(repo_root: str) -> List[Dict[str, Any]]:
    pattern = os.path.join(repo_root, '*', '*', 'README.md')
    files = glob.glob(pattern)
    all_questions = []
    
    for f in sorted(files):
        qs = parse_markdown_file(f, repo_root)
        all_questions.extend(qs)
        
    return all_questions

if __name__ == '__main__':
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    qs = parse_all_repository_questions(repo_path)
    print(f"Total parsed: {len(qs)}")
    categories = set(q['category'] for q in qs)
    print(f"Categories ({len(categories)}): {categories}")
    levels = set(q['level'] for q in qs)
    print(f"Levels: {levels}")
    q_types = {}
    for q in qs:
        t = q['question_type']
        q_types[t] = q_types.get(t, 0) + 1
    print(f"Question types: {q_types}")
