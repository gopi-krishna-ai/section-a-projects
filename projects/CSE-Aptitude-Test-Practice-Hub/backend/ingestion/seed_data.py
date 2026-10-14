import os
import re
import sys
from datetime import datetime
from backend.database import engine, SessionLocal, Base
from backend.models import User, Topic, Question, ConceptLesson, TopicMastery
from backend.ingestion.parser import parse_all_repository_questions
from backend.ingestion.lessons_data import LESSONS

# Master Topic Syllabus Definition
TOPIC_DEFINITIONS = [
    # Quantitative Aptitude
    {
        "id": "percentages",
        "name": "Percentages",
        "category": "Quantitative Aptitude",
        "parent_topic_id": None,
        "description": "Master basic percentages, fractional equivalents, successive changes, and base shifts.",
        "prerequisites": [],
        "icon": "Percent",
        "order_index": 1
    },
    {
        "id": "profit_and_loss",
        "name": "Profit and Loss",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "percentages",
        "description": "Cost price, selling price, markups, discounts, margins, and dishonest dealer problems.",
        "prerequisites": ["percentages"],
        "icon": "TrendingUp",
        "order_index": 2
    },
    {
        "id": "simple_and_compound_interest",
        "name": "Simple & Compound Interest",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "percentages",
        "description": "Principal, rate, time, simple interest accumulation, compounding frequency, and annual effective yields.",
        "prerequisites": ["percentages"],
        "icon": "DollarSign",
        "order_index": 3
    },
    {
        "id": "ratios_and_proportions",
        "name": "Ratios and Proportions",
        "category": "Quantitative Aptitude",
        "parent_topic_id": None,
        "description": "Direct and inverse proportions, compound ratios, partnership shares, and mixtures.",
        "prerequisites": [],
        "icon": "Scale",
        "order_index": 4
    },
    {
        "id": "averages",
        "name": "Averages",
        "category": "Quantitative Aptitude",
        "parent_topic_id": None,
        "description": "Arithmetic mean, weighted averages, age replacement problems, and running averages.",
        "prerequisites": [],
        "icon": "BarChart2",
        "order_index": 5
    },
    {
        "id": "time_and_work",
        "name": "Time and Work",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "ratios_and_proportions",
        "description": "Efficiency rates, LCM unitary method, pipes & cisterns, and alternating work schedules.",
        "prerequisites": ["ratios_and_proportions"],
        "icon": "Clock",
        "order_index": 6
    },
    {
        "id": "time_and_distance",
        "name": "Time and Distance",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "ratios_and_proportions",
        "description": "Speed-time-distance relations, relative speed, trains crossing platforms, boats and streams.",
        "prerequisites": ["ratios_and_proportions"],
        "icon": "Navigation",
        "order_index": 7
    },
    {
        "id": "number_systems",
        "name": "Number Systems",
        "category": "Quantitative Aptitude",
        "parent_topic_id": None,
        "description": "Divisibility rules, unit digits, LCM & HCF, remainders, factorials, and prime factorization.",
        "prerequisites": [],
        "icon": "Hash",
        "order_index": 8
    },
    {
        "id": "permutations_and_combinations",
        "name": "Permutations and Combinations",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "number_systems",
        "description": "Fundamental counting principle, arrangements, selections, circular permutations, and grouping.",
        "prerequisites": ["number_systems"],
        "icon": "Shuffle",
        "order_index": 9
    },
    {
        "id": "probability",
        "name": "Probability",
        "category": "Quantitative Aptitude",
        "parent_topic_id": "permutations_and_combinations",
        "description": "Sample space, independent events, conditional probability, Bayes theorem, and card/dice problems.",
        "prerequisites": ["permutations_and_combinations"],
        "icon": "HelpCircle",
        "order_index": 10
    },

    # Logical Reasoning
    {
        "id": "series",
        "name": "Series",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Arithmetic, geometric, quadratic differences, alphanumeric, and alternating sequences.",
        "prerequisites": [],
        "icon": "Activity",
        "order_index": 11
    },
    {
        "id": "analogies",
        "name": "Analogies",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Semantic relationships, functional pairs, categorical mapping, and symbolic analogies.",
        "prerequisites": [],
        "icon": "Repeat",
        "order_index": 12
    },
    {
        "id": "coding_decoding",
        "name": "Coding-Decoding",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Letter shifts, reversal ciphers, numerical substitution, and matrix cipher decoding.",
        "prerequisites": [],
        "icon": "Code",
        "order_index": 13
    },
    {
        "id": "blood_relations",
        "name": "Blood Relations",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Family tree modeling, coded relations, generational gaps, and maternal/paternal deductions.",
        "prerequisites": [],
        "icon": "Users",
        "order_index": 14
    },
    {
        "id": "directions",
        "name": "Directions",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Compass navigation, angular turns, shadow cues, and Euclidean shortest-path displacement.",
        "prerequisites": [],
        "icon": "Compass",
        "order_index": 15
    },
    {
        "id": "syllogisms",
        "name": "Syllogisms",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Deductive logic, Venn diagrams, universal/particular premises, and possibility conclusions.",
        "prerequisites": [],
        "icon": "Circle",
        "order_index": 16
    },
    {
        "id": "puzzles",
        "name": "Puzzles",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Floor arrangements, linear and circular seating arrangements, matching grids, and scheduling.",
        "prerequisites": [],
        "icon": "Grid",
        "order_index": 17
    },
    {
        "id": "data_sufficiency",
        "name": "Data Sufficiency",
        "category": "Logical Reasoning",
        "parent_topic_id": "series",
        "description": "Evaluating if statement (1), (2), or both combined suffice to answer without computing final values.",
        "prerequisites": ["series"],
        "icon": "CheckSquare",
        "order_index": 18
    },
    {
        "id": "critical_reasoning",
        "name": "Critical Reasoning",
        "category": "Logical Reasoning",
        "parent_topic_id": "syllogisms",
        "description": "Strengthening/weakening arguments, identifying implicit assumptions, and drawing valid inferences.",
        "prerequisites": ["syllogisms"],
        "icon": "Eye",
        "order_index": 19
    },
    {
        "id": "non_verbal_reasoning",
        "name": "Non-Verbal Reasoning",
        "category": "Logical Reasoning",
        "parent_topic_id": None,
        "description": "Mirror images, water reflections, paper folding, and spatial rotations.",
        "prerequisites": [],
        "icon": "Layers",
        "order_index": 20
    },

    # Verbal Ability
    {
        "id": "synonyms",
        "name": "Synonyms",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Vocabulary retention, context-based lexical connotations, and nuance distinction.",
        "prerequisites": [],
        "icon": "Book",
        "order_index": 21
    },
    {
        "id": "antonyms",
        "name": "Antonyms",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Direct polar opposites, contrasting tones, and contextual antonyms.",
        "prerequisites": [],
        "icon": "Minimize2",
        "order_index": 22
    },
    {
        "id": "sentence_completion",
        "name": "Sentence Completion",
        "category": "Verbal Ability",
        "parent_topic_id": "synonyms",
        "description": "Single and double blank fillers using grammatical agreement and transition signals.",
        "prerequisites": ["synonyms"],
        "icon": "Edit3",
        "order_index": 23
    },
    {
        "id": "spotting_errors",
        "name": "Spotting Errors",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Subject-verb agreement, tense inconsistencies, preposition misuse, and modifier placement.",
        "prerequisites": [],
        "icon": "AlertCircle",
        "order_index": 24
    },
    {
        "id": "sentence_correction",
        "name": "Sentence Correction",
        "category": "Verbal Ability",
        "parent_topic_id": "spotting_errors",
        "description": "Replacing flawed sentence clauses with grammatically sound and concise alternatives.",
        "prerequisites": ["spotting_errors"],
        "icon": "CheckCircle2",
        "order_index": 25
    },
    {
        "id": "reading_comprehension",
        "name": "Reading Comprehension",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Passage skimming, central theme extraction, tone analysis, and detail retrieval.",
        "prerequisites": [],
        "icon": "FileText",
        "order_index": 26
    },
    {
        "id": "jumbled_sentences",
        "name": "Jumbled Sentences (Para Jumbles)",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Ordering scrambled sentences into coherent paragraphs via mandatory pairs and pronoun links.",
        "prerequisites": [],
        "icon": "ListOrdered",
        "order_index": 27
    },
    {
        "id": "cloze_test",
        "name": "Cloze Test",
        "category": "Verbal Ability",
        "parent_topic_id": "sentence_completion",
        "description": "Paragraph fill-in-the-blanks requiring comprehensive narrative comprehension and vocabulary.",
        "prerequisites": ["sentence_completion"],
        "icon": "FileQuestion",
        "order_index": 28
    },
    {
        "id": "idioms_phrases",
        "name": "Idioms and Phrases",
        "category": "Verbal Ability",
        "parent_topic_id": None,
        "description": "Figurative expressions, phrasal verbs, colloquial terminology, and proverb meanings.",
        "prerequisites": [],
        "icon": "MessageSquare",
        "order_index": 29
    },
    {
        "id": "verbal_analogies",
        "name": "Verbal Analogies",
        "category": "Verbal Ability",
        "parent_topic_id": "synonyms",
        "description": "Relationship abstraction between pairs of words across degrees, tools, and actions.",
        "prerequisites": ["synonyms"],
        "icon": "GitCommit",
        "order_index": 30
    },

    # Data Interpretation
    {
        "id": "table_based_questions",
        "name": "Tables & Data Matrices",
        "category": "Data Interpretation and Analysis",
        "parent_topic_id": None,
        "description": "Reading tabular matrices, computing row/column totals, percentages, and growth rates.",
        "prerequisites": ["percentages", "averages"],
        "icon": "Table",
        "order_index": 31
    },
    {
        "id": "bar_graph_based_questions",
        "name": "Bar Graphs & Histograms",
        "category": "Data Interpretation and Analysis",
        "parent_topic_id": "table_based_questions",
        "description": "Single, grouped, and stacked bar graphs, comparing values across discrete categories.",
        "prerequisites": ["table_based_questions"],
        "icon": "BarChart",
        "order_index": 32
    },
    {
        "id": "pie_chart_based_questions",
        "name": "Pie Charts",
        "category": "Data Interpretation and Analysis",
        "parent_topic_id": "table_based_questions",
        "description": "Sector angle conversions (360 degrees = 100%), proportional breakdowns, and multiple pie comparisons.",
        "prerequisites": ["percentages", "ratios_and_proportions"],
        "icon": "PieChart",
        "order_index": 33
    },
    {
        "id": "line_graph_based_questions",
        "name": "Line Graphs",
        "category": "Data Interpretation and Analysis",
        "parent_topic_id": "table_based_questions",
        "description": "Continuous trend tracking, slopes, peak detection, and time-series comparisons.",
        "prerequisites": ["table_based_questions"],
        "icon": "TrendingUp",
        "order_index": 34
    },
    {
        "id": "caselet_based_questions",
        "name": "Caselets & Paragraph Data",
        "category": "Data Interpretation and Analysis",
        "parent_topic_id": "table_based_questions",
        "description": "Transforming unstructured descriptive paragraphs into structured tables or Venn sets.",
        "prerequisites": ["table_based_questions"],
        "icon": "FileSpreadsheet",
        "order_index": 35
    },

    # Abstract Reasoning
    {
        "id": "number_sequence_questions",
        "name": "Abstract Number Sequences",
        "category": "Abstract Reasoning",
        "parent_topic_id": None,
        "description": "Abstract and non-standard number progressions, transformations, and missing elements.",
        "prerequisites": [],
        "icon": "Binary",
        "order_index": 36
    },
    {
        "id": "shape_pattern_questions",
        "name": "Shape Patterns & Geometric Sequences",
        "category": "Abstract Reasoning",
        "parent_topic_id": None,
        "description": "Tracking clockwise/counter-clockwise rotations, side increments, shading shifts, and symmetries.",
        "prerequisites": [],
        "icon": "Square",
        "order_index": 37
    },
    {
        "id": "analogy_questions",
        "name": "Abstract Analogies",
        "category": "Abstract Reasoning",
        "parent_topic_id": None,
        "description": "Determining structural geometric rules relating figure A to B, then applying to figure C.",
        "prerequisites": [],
        "icon": "GitPullRequest",
        "order_index": 38
    },
    {
        "id": "matrix_pattern_questions",
        "name": "Matrix Patterns (3x3 Grids)",
        "category": "Abstract Reasoning",
        "parent_topic_id": "shape_pattern_questions",
        "description": "Discovering row-wise and column-wise visual logic within 2x2 and 3x3 pattern matrices.",
        "prerequisites": ["shape_pattern_questions"],
        "icon": "Grid",
        "order_index": 39
    },
    {
        "id": "odd_one_out_questions",
        "name": "Odd One Out",
        "category": "Abstract Reasoning",
        "parent_topic_id": None,
        "description": "Isolating visual or numerical figures that violate the common rule obeyed by the rest.",
        "prerequisites": [],
        "icon": "XCircle",
        "order_index": 40
    },

    # Technical Aptitude
    {
        "id": "programming_fundamentals",
        "name": "Programming Fundamentals",
        "category": "Technical Aptitude",
        "parent_topic_id": None,
        "description": "Language syntax, operator precedence, bitwise logic, loops, and variable scopes in C, C++, Java, Python.",
        "prerequisites": [],
        "icon": "Code",
        "order_index": 41
    },
    {
        "id": "data_structures",
        "name": "Data Structures",
        "category": "Technical Aptitude",
        "parent_topic_id": "programming_fundamentals",
        "description": "Arrays, linked lists, stacks, queues, binary trees, heaps, and hash table complexities.",
        "prerequisites": ["programming_fundamentals"],
        "icon": "Database",
        "order_index": 42
    },
    {
        "id": "algorithms",
        "name": "Algorithms",
        "category": "Technical Aptitude",
        "parent_topic_id": "data_structures",
        "description": "Asymptotic Big-O notation, binary search, sorting algorithms, recursion, and greedy paradigms.",
        "prerequisites": ["data_structures"],
        "icon": "Cpu",
        "order_index": 43
    },
    {
        "id": "database_basics",
        "name": "Database Basics (SQL)",
        "category": "Technical Aptitude",
        "parent_topic_id": None,
        "description": "Relational algebra, SQL queries (JOINs, GROUP BY, HAVING), keys, normalization, and ACID properties.",
        "prerequisites": [],
        "icon": "HardDrive",
        "order_index": 44
    },
    {
        "id": "computer_networks",
        "name": "Computer Networks",
        "category": "Technical Aptitude",
        "parent_topic_id": None,
        "description": "OSI & TCP/IP layers, IP addressing, subnetting, DNS, HTTP/HTTPS, and routing protocols.",
        "prerequisites": [],
        "icon": "Globe",
        "order_index": 45
    },
    {
        "id": "operating_systems",
        "name": "Operating Systems",
        "category": "Technical Aptitude",
        "parent_topic_id": None,
        "description": "Process management, threads, CPU scheduling, deadlocks, virtual memory, and paging.",
        "prerequisites": [],
        "icon": "Terminal",
        "order_index": 46
    },
    {
        "id": "ai_ml_foundations",
        "name": "AI & ML Foundations",
        "category": "Technical Aptitude",
        "parent_topic_id": "programming_fundamentals",
        "description": "Supervised vs unsupervised learning, regression, classification, overfitting/underfitting, neural nets.",
        "prerequisites": ["programming_fundamentals", "probability"],
        "icon": "Cpu",
        "order_index": 47
    }
]

def map_subtopic_to_topic_id(category: str, raw_subtopic: str) -> str:
    sub = raw_subtopic.lower()
    sub = re.sub(r'\s*\(\d+[-–]\d+\)', '', sub).strip()
    
    # Quantitative
    if "percentage" in sub: return "percentages"
    if "profit" in sub or "loss" in sub: return "profit_and_loss"
    if "simple interest" in sub or "compound interest" in sub: return "simple_and_compound_interest"
    if "ratio" in sub or "proportion" in sub: return "ratios_and_proportions"
    if "average" in sub: return "averages"
    if "work" in sub or "pipe" in sub: return "time_and_work"
    if "distance" in sub or "train" in sub or "speed" in sub: return "time_and_distance"
    if "number system" in sub: return "number_systems"
    if "permutation" in sub or "combination" in sub: return "permutations_and_combinations"
    if "probability" in sub: return "probability"
    
    # Logical
    if "series" in sub: return "series"
    if "analogy" in sub or "analogies" in sub:
        return "analogies" if category == "Logical Reasoning" else "analogy_questions"
    if "coding" in sub: return "coding_decoding"
    if "blood" in sub: return "blood_relations"
    if "direction" in sub: return "directions"
    if "syllogism" in sub: return "syllogisms"
    if "puzzle" in sub or "seating" in sub: return "puzzles"
    if "data sufficiency" in sub: return "data_sufficiency"
    if "critical" in sub: return "critical_reasoning"
    if "non-verbal" in sub or "non verbal" in sub: return "non_verbal_reasoning"
    
    # Verbal
    if "synonym" in sub: return "synonyms"
    if "antonym" in sub: return "antonyms"
    if "sentence completion" in sub: return "sentence_completion"
    if "spotting" in sub or "error" in sub: return "spotting_errors"
    if "sentence correction" in sub: return "sentence_correction"
    if "reading" in sub or "comprehension" in sub: return "reading_comprehension"
    if "jumbled" in sub or "para" in sub: return "jumbled_sentences"
    if "cloze" in sub: return "cloze_test"
    if "idiom" in sub or "phrase" in sub: return "idioms_phrases"
    if "verbal analog" in sub: return "verbal_analogies"
    
    # Data Interpretation
    if "table" in sub: return "table_based_questions"
    if "bar graph" in sub or "stacked bar" in sub: return "bar_graph_based_questions"
    if "pie" in sub: return "pie_chart_based_questions"
    if "line graph" in sub or "combination chart" in sub: return "line_graph_based_questions"
    if "caselet" in sub: return "caselet_based_questions"
    
    # Abstract Reasoning
    if "number sequence" in sub: return "number_sequence_questions"
    if "shape pattern" in sub: return "shape_pattern_questions"
    if "matrix" in sub: return "matrix_pattern_questions"
    if "odd one" in sub: return "odd_one_out_questions"
    
    # Technical
    if "programming" in sub: return "programming_fundamentals"
    if "data structure" in sub: return "data_structures"
    if "algorithm" in sub: return "algorithms"
    if "database" in sub or "sql" in sub: return "database_basics"
    if "network" in sub: return "computer_networks"
    if "operating" in sub or "os" in sub: return "operating_systems"
    if "ai" in sub or "ml" in sub: return "ai_ml_foundations"
    
    # Default fallbacks per category
    cat_fallbacks = {
        "Quantitative Aptitude": "percentages",
        "Logical Reasoning": "series",
        "Verbal Ability": "synonyms",
        "Data Interpretation and Analysis": "table_based_questions",
        "Abstract Reasoning": "shape_pattern_questions",
        "Technical Aptitude": "programming_fundamentals"
    }
    return cat_fallbacks.get(category, "percentages")

def run_ingestion(repo_path: str = None) -> dict:
    if repo_path is None:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
    print(f"Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    report = {
        "topics_seeded": 0,
        "lessons_seeded": 0,
        "questions_parsed": 0,
        "questions_inserted": 0,
        "questions_updated": 0,
        "errors": []
    }
    
    try:
        # 1. Seed or get default user
        user = db.query(User).filter_by(id="default_user").first()
        if not user:
            user = User(
                id="default_user",
                username="learner",
                preferences={"target_company": "TCS/Infosys", "daily_goal": 15, "theme": "system"}
            )
            db.add(user)
            db.commit()
            print("Default user initialized.")

        # 2. Seed Topics
        for t_def in TOPIC_DEFINITIONS:
            existing = db.query(Topic).filter_by(id=t_def["id"]).first()
            if not existing:
                topic = Topic(
                    id=t_def["id"],
                    name=t_def["name"],
                    category=t_def["category"],
                    parent_topic_id=t_def["parent_topic_id"],
                    description=t_def["description"],
                    prerequisites=t_def["prerequisites"],
                    icon=t_def["icon"],
                    order_index=t_def["order_index"]
                )
                db.add(topic)
                report["topics_seeded"] += 1
            else:
                existing.name = t_def["name"]
                existing.description = t_def["description"]
                existing.prerequisites = t_def["prerequisites"]
                existing.order_index = t_def["order_index"]
        db.commit()
        print(f"Seeded/updated {len(TOPIC_DEFINITIONS)} topics.")

        # 3. Seed Lessons
        for topic_id, lesson_data in LESSONS.items():
            existing_lesson = db.query(ConceptLesson).filter_by(id=topic_id).first()
            if not existing_lesson:
                lesson = ConceptLesson(
                    id=topic_id,
                    topic_id=topic_id,
                    category=lesson_data["category"],
                    title=lesson_data["title"],
                    concept_summary=lesson_data["concept_summary"],
                    why_needed=lesson_data["why_needed"],
                    simple_explanation=lesson_data["simple_explanation"],
                    real_world_example=lesson_data["real_world_example"],
                    intuition=lesson_data["intuition"],
                    important_terms=lesson_data["important_terms"],
                    formulas=lesson_data["formulas"],
                    step_by_step_example=lesson_data["step_by_step_example"],
                    placement_example=lesson_data["placement_example"],
                    common_traps=lesson_data["common_traps"],
                    key_takeaways=lesson_data["key_takeaways"]
                )
                db.add(lesson)
                report["lessons_seeded"] += 1
        db.commit()
        print(f"Seeded {report['lessons_seeded']} concept lessons.")

        # 4. Ingest All Questions
        print(f"Parsing questions from: {repo_path}")
        raw_questions = parse_all_repository_questions(repo_path)
        report["questions_parsed"] = len(raw_questions)
        
        seen_source_ids = {}
        
        for q_data in raw_questions:
            # Ensure strictly unique source_id across duplicate questions in source files
            base_source_id = q_data["source_id"]
            if base_source_id in seen_source_ids:
                seen_source_ids[base_source_id] += 1
                source_id = f"{base_source_id}_dup{seen_source_ids[base_source_id]}"
            else:
                seen_source_ids[base_source_id] = 1
                source_id = base_source_id

            topic_id = map_subtopic_to_topic_id(q_data["category"], q_data["subtopic"])
            
            diff_score = 1.0
            if q_data["level"] == "Intermediate":
                diff_score = 2.0
            elif q_data["level"] == "Advanced":
                diff_score = 3.0

            existing_q = db.query(Question).filter_by(source_id=source_id).first()
            if existing_q:
                existing_q.question_text = q_data["question_text"]
                existing_q.raw_question = q_data["raw_question"]
                existing_q.stimulus_context = q_data["stimulus_context"]
                existing_q.options = q_data["options"]
                existing_q.correct_answer = q_data["correct_answer"]
                existing_q.reference_solution = q_data["reference_solution"]
                existing_q.question_type = q_data["question_type"]
                existing_q.hints = q_data["hints"]
                existing_q.difficulty = diff_score
                report["questions_updated"] += 1
            else:
                new_q = Question(
                    source_id=source_id,
                    source_file=q_data["source_file"],
                    category=q_data["category"],
                    topic_id=topic_id,
                    subtopic_name=q_data["subtopic"],
                    level=q_data["level"],
                    stimulus_context=q_data["stimulus_context"],
                    question_text=q_data["question_text"],
                    raw_question=q_data["raw_question"],
                    question_type=q_data["question_type"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    reference_solution=q_data["reference_solution"],
                    difficulty=diff_score,
                    validation_status=q_data["validation_status"],
                    hints=q_data["hints"]
                )
                db.add(new_q)
                report["questions_inserted"] += 1

        db.commit()
        print(f"Ingestion finished: {report['questions_inserted']} inserted, {report['questions_updated']} updated.")

        # 5. Initialize TopicMastery for default user for all topics
        for t_def in TOPIC_DEFINITIONS:
            m = db.query(TopicMastery).filter_by(user_id="default_user", topic_id=t_def["id"]).first()
            if not m:
                m = TopicMastery(
                    user_id="default_user",
                    topic_id=t_def["id"],
                    mastery_score=0.0,
                    status="not_started",
                    total_attempted=0,
                    total_correct=0,
                    unassisted_correct=0
                )
                db.add(m)
        db.commit()

    except Exception as e:
        db.rollback()
        report["errors"].append(str(e))
        print(f"Error during ingestion: {e}")
        raise e
    finally:
        db.close()
        
    return report

if __name__ == '__main__':
    rep = run_ingestion()
    print("=== FINAL INGESTION REPORT ===")
    print(rep)
