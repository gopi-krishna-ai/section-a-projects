export interface UserAccount {
  id: string;
  username: string;
  email?: string;
  full_name?: string;
  skill_level: string;
  target_goal: string;
  avatar: string;
}

export interface Topic {
  id: string;
  track: string;
  level: string;
  title: string;
  description: string;
  order_index: number;
  icon: string;
  total_problems: number;
  mastery_score: number;
  status: string;
}

export interface Lesson {
  id: string;
  topic_id: string;
  title: string;
  content: string;
  runnable_snippets: Array<{
    title: string;
    code: string;
    explanation: string;
  }>;
  key_takeaways: string[];
}

export interface ProblemSummary {
  id: string;
  slug: string;
  title: string;
  topic_id: string;
  track: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  time_complexity: string;
  space_complexity: string;
  tags: string[];
  has_attempted: boolean;
  is_solved: boolean;
}

export interface ProblemDetail {
  id: string;
  slug: string;
  title: string;
  topic_id: string;
  track: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  description: string;
  constraints: string[];
  examples: Array<{
    input: any;
    output: any;
    explanation?: string;
  }>;
  starter_code: string;
  time_complexity: string;
  space_complexity: string;
  hints: Array<{
    level?: number;
    title?: string;
    content?: string;
  }>;
  visible_tests: Array<{
    input: any;
    expected_output: any;
    is_hidden?: boolean;
    explanation?: string;
  }>;
  tags: string[];
  dry_run_steps: Array<{
    step: number;
    action: string;
    state: Record<string, any>;
  }>;
}

export interface TestResultItem {
  test_index: number;
  input_str: string;
  expected_output_str: string;
  actual_output_str?: string;
  passed: boolean;
  is_hidden: boolean;
  execution_time_ms: number;
  error?: string;
}

export interface SubmitSolutionResult {
  status: 'Passed' | 'Failed' | 'Runtime Error' | 'Timeout';
  passes_count: number;
  total_tests: number;
  execution_time_ms: number;
  is_independent: boolean;
  test_results: TestResultItem[];
  mistake_diagnosis?: {
    error_category: string;
    what_went_wrong: string;
    why_it_went_wrong: string;
    how_to_avoid: string;
    corrective_exercise?: {
      title: string;
      prompt: string;
    };
  };
  mastery_update?: {
    topic_id: string;
    mastery_score: number;
    status: string;
    independent_solved: number;
    assisted_solved: number;
    total_attempted: number;
  };
}

export interface MistakeRecord {
  id: string;
  problem_id: string;
  problem_title: string;
  topic_id: string;
  error_category: string;
  submitted_code: string;
  failing_test_case?: {
    input?: string;
    expected_output?: string;
    actual_output?: string;
  };
  what_went_wrong: string;
  why_it_went_wrong: string;
  how_to_avoid: string;
  retest_status: 'pending' | 'resolved';
  created_at: string;
}

export interface DebugExercise {
  id: string;
  title: string;
  topic: string;
  difficulty: string;
  buggy_code: string;
  bug_category: string;
  description: string;
  hint: string;
  test_cases: any[];
}

export interface LogicPuzzle {
  id: string;
  title: string;
  category: string;
  statement: string;
  code_snippet?: string;
  options?: string[];
  reasoning_pattern: string;
}

export interface RevisionItem {
  id: string;
  problem_id: string;
  problem_title: string;
  difficulty: string;
  topic_title: string;
  interval_days: number;
  repetition_number: number;
  due_at: string;
}

export interface DashboardData {
  total_problems_in_bank: number;
  total_attempted: number;
  total_solved: number;
  independent_solved: number;
  independent_accuracy: number;
  overall_accuracy: number;
  streak_days: number;
  active_topics: Array<{
    topic_id: string;
    title: string;
    track: string;
    mastery_score: number;
    status: string;
    total_attempted: number;
    independent_solved: number;
  }>;
  topics_needing_focus: Array<{
    topic_id: string;
    title: string;
    track: string;
    mastery_score: number;
    status: string;
  }>;
  top_mistake_patterns: Array<{
    error_category: string;
    count: number;
  }>;
  due_revisions_count: number;
  recent_submissions: Array<{
    problem_id: string;
    problem_title: string;
    status: string;
    is_independent: boolean;
    hints_used: number;
    execution_time_ms: number;
    submitted_at: string;
  }>;
  recommended_next_task?: {
    type: string;
    id: string;
    title: string;
    topic: string;
    difficulty: string;
    reason: string;
  };
}
