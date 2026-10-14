export interface UserAccount {
  id: string;
  username: string;
  full_name?: string | null;
  email?: string | null;
  target_company: string;
  avatar?: string;
  preferences?: Record<string, any>;
}

export interface Topic {
  id: string;
  name: string;
  category: string;
  parent_topic_id?: string | null;
  description: string;
  prerequisites: string[];
  icon: string;
  order_index: number;
  total_questions: number;
  mastery_score: number;
  status: 'not_started' | 'learning' | 'needs_practice' | 'improving' | 'proficient' | 'needs_revision';
  unassisted_accuracy: number;
}

export interface Question {
  id: string;
  source_id: string;
  source_file: string;
  category: string;
  topic_id: string;
  subtopic_name: string;
  level: 'Basic' | 'Intermediate' | 'Advanced';
  stimulus_context?: string | null;
  question_text: string;
  question_type: 'numeric' | 'mcq' | 'text_correction' | 'short_answer';
  options?: string[] | null;
  difficulty: number;
  hints: string[];
  formula_reference?: string | null;
  is_bookmarked?: boolean;
  correct_answer?: string;
  reference_solution?: string;
}

export interface SubmitAnswerResult {
  is_correct: boolean;
  submitted_answer: string;
  correct_answer: string;
  reference_solution: string;
  match_type: string;
  feedback: string;
  attempt_id: string;
  hints_used: number;
  error_diagnosis?: {
    error_category: string;
    what_went_wrong: string;
    why_it_went_wrong: string;
    correct_reasoning: string;
    how_to_avoid: string;
    corrective_exercise?: {
      prompt: string;
      hint: string;
    };
  } | null;
  mastery_update?: {
    topic_id: string;
    mastery_score: number;
    status: string;
    total_attempted: number;
    total_correct: number;
  } | null;
}

export interface ProgressiveHint {
  hint_level: number;
  title: string;
  content: string;
  educational_takeaway?: string;
  correct_answer?: string;
}

export interface StepGuidance {
  step: string;
  title: string;
  content: string;
  guiding_question?: string;
}

export interface MistakeRecord {
  id: string;
  attempt_id: string;
  question_id: string;
  topic_id: string;
  topic_name: string;
  category: string;
  question_text: string;
  submitted_answer: string;
  correct_answer: string;
  error_category: string;
  what_went_wrong: string;
  why_it_went_wrong: string;
  correct_reasoning: string;
  how_to_avoid: string;
  corrective_exercise?: {
    prompt: string;
    hint: string;
  };
  retest_status: 'pending' | 'retested_passed' | 'retested_failed';
  created_at: string;
}

export interface RevisionItem {
  id: string;
  question_id: string;
  topic_id: string;
  topic_name: string;
  category: string;
  question_text: string;
  stimulus_context?: string | null;
  options?: string[] | null;
  due_at: string;
  interval_days: number;
  repetition_number: number;
  review_status: string;
}

export interface ConceptLesson {
  id: string;
  topic_id: string;
  category: string;
  title: string;
  concept_summary: string;
  why_needed: string;
  simple_explanation: string;
  real_world_example: string;
  intuition: string;
  important_terms: Array<{ term: string; definition: string }>;
  formulas: Array<{ name: string; formula: string; why_works: string; when_to_use: string }>;
  step_by_step_example: {
    question: string;
    steps: string[];
    solution: string;
  };
  placement_example: {
    question: string;
    approach: string;
    solution: string;
    trap: string;
  };
  common_traps: string[];
  key_takeaways: string[];
}

export interface DashboardData {
  total_repository_questions: number;
  total_attempted_unique: number;
  total_solved_correct: number;
  overall_accuracy: number;
  unassisted_accuracy: number;
  current_studying_topics: Array<{
    topic_id: string;
    topic_name: string;
    category: string;
    mastery_score: number;
    status: string;
    total_attempted: number;
    total_correct: number;
  }>;
  topics_needing_improvement: Array<{
    topic_id: string;
    topic_name: string;
    category: string;
    mastery_score: number;
    status: string;
    total_attempted: number;
    total_correct: number;
  }>;
  top_repeated_mistakes: Array<{
    error_category: string;
    count: number;
  }>;
  due_revisions_count: number;
  recent_attempts: Array<{
    attempt_id: string;
    question_id: string;
    question_text: string;
    category: string;
    is_correct: boolean;
    hints_used: number;
    time_spent: number;
    attempted_at: string;
  }>;
  recommended_next_lesson?: {
    topic_id: string;
    topic_name: string;
    category: string;
    reason: string;
  } | null;
}
