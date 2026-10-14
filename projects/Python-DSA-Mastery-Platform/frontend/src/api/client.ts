import {
  UserAccount, Topic, Lesson, ProblemSummary, ProblemDetail,
  SubmitSolutionResult, MistakeRecord, DebugExercise, LogicPuzzle,
  RevisionItem, DashboardData
} from '../types';

const API_BASE = '/api';

export const getStoredUserId = (): string => {
  return localStorage.getItem('python_dsa_user_id') || 'default_user';
};

export const getStoredToken = (): string | null => {
  return localStorage.getItem('python_dsa_token');
};

const getAuthHeaders = (): Record<string, string> => {
  const token = getStoredToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

export const api = {
  // Auth
  async login(username: string, password: string): Promise<{ token: string; user: UserAccount }> {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Login failed');
    }
    const data = await res.json();
    localStorage.setItem('python_dsa_token', data.token);
    localStorage.setItem('python_dsa_user_id', data.user.id);
    localStorage.setItem('python_dsa_user', JSON.stringify(data.user));
    return data;
  },

  async register(params: {
    username: string;
    password: string;
    email?: string;
    full_name?: string;
    target_goal?: string;
    skill_level?: string;
  }): Promise<{ token: string; user: UserAccount }> {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Registration failed');
    }
    const data = await res.json();
    localStorage.setItem('python_dsa_token', data.token);
    localStorage.setItem('python_dsa_user_id', data.user.id);
    localStorage.setItem('python_dsa_user', JSON.stringify(data.user));
    return data;
  },

  async getDemoUsers(): Promise<UserAccount[]> {
    const res = await fetch(`${API_BASE}/auth/demo_users`);
    if (!res.ok) throw new Error('Failed to fetch demo accounts');
    return res.json();
  },

  async switchDemo(username: string): Promise<{ token: string; user: UserAccount }> {
    const res = await fetch(`${API_BASE}/auth/switch_demo`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to switch demo account');
    }
    const data = await res.json();
    localStorage.setItem('python_dsa_token', data.token);
    localStorage.setItem('python_dsa_user_id', data.user.id);
    localStorage.setItem('python_dsa_user', JSON.stringify(data.user));
    return data;
  },

  logout(): void {
    localStorage.removeItem('python_dsa_token');
    localStorage.removeItem('python_dsa_user_id');
    localStorage.removeItem('python_dsa_user');
  },

  // Dashboard
  async getDashboard(userId = getStoredUserId()): Promise<DashboardData> {
    const res = await fetch(`${API_BASE}/analytics/dashboard?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load dashboard metrics');
    return res.json();
  },

  // Curriculum
  async getTopics(track?: string, userId = getStoredUserId()): Promise<Topic[]> {
    const url = track
      ? `${API_BASE}/curriculum/topics?track=${track}&user_id=${userId}`
      : `${API_BASE}/curriculum/topics?user_id=${userId}`;
    const res = await fetch(url, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load curriculum topics');
    return res.json();
  },

  async getTopicLessons(topicId: string): Promise<Lesson[]> {
    const res = await fetch(`${API_BASE}/curriculum/topics/${topicId}/lessons`);
    if (!res.ok) throw new Error('Failed to load topic lessons');
    return res.json();
  },

  // Problems
  async getProblems(params: {
    topic_id?: string;
    difficulty?: string;
    track?: string;
    search?: string;
    user_id?: string;
  } = {}): Promise<ProblemSummary[]> {
    const q = new URLSearchParams();
    if (params.topic_id) q.append('topic_id', params.topic_id);
    if (params.difficulty) q.append('difficulty', params.difficulty);
    if (params.track) q.append('track', params.track);
    if (params.search) q.append('search', params.search);
    q.append('user_id', params.user_id || getStoredUserId());

    const res = await fetch(`${API_BASE}/problems?${q.toString()}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load problems');
    return res.json();
  },

  async getProblemDetail(problemId: string): Promise<ProblemDetail> {
    const res = await fetch(`${API_BASE}/problems/${problemId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load problem');
    return res.json();
  },

  async fetchHint(problemId: string, level: number): Promise<{ level: number; title: string; content: string; is_full_solution: boolean }> {
    const res = await fetch(`${API_BASE}/problems/${problemId}/hints?hint_level=${level}`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch hint');
    return res.json();
  },

  async askMentor(problemId: string, payload: { code: string; query: string; error_message?: string }): Promise<{ provider: string; response: string }> {
    const res = await fetch(`${API_BASE}/problems/${problemId}/ask_mentor`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Mentor unavailable');
    return res.json();
  },

  async submitSolution(problemId: string, payload: {
    code: string;
    hints_used: number;
    solution_viewed: boolean;
    user_id?: string;
  }): Promise<SubmitSolutionResult> {
    const res = await fetch(`${API_BASE}/problems/${problemId}/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        problem_id: problemId,
        user_id: payload.user_id || getStoredUserId(),
        ...payload
      }),
    });
    if (!res.ok) throw new Error('Failed to evaluate solution');
    return res.json();
  },

  // Code Execution (Playground)
  async runCode(code: string, stdinInput?: string): Promise<{
    stdout: string;
    stderr: string;
    exit_code: number;
    execution_time_ms: number;
    error_type?: string;
  }> {
    const res = await fetch(`${API_BASE}/execution/run`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ code, stdin_input: stdinInput }),
    });
    if (!res.ok) throw new Error('Execution failed');
    return res.json();
  },

  // Mistake Notebook
  async getMistakes(userId = getStoredUserId(), status?: string, category?: string): Promise<MistakeRecord[]> {
    const q = new URLSearchParams();
    q.append('user_id', userId);
    if (status) q.append('retest_status', status);
    if (category) q.append('category', category);

    const res = await fetch(`${API_BASE}/mistakes?${q.toString()}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load mistakes');
    return res.json();
  },

  async retestMistake(mistakeId: string, code: string): Promise<{
    mistake_id: string;
    is_resolved: boolean;
    passes_count: number;
    total_tests: number;
    feedback: string;
  }> {
    const res = await fetch(`${API_BASE}/mistakes/${mistakeId}/retest`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ mistake_id: mistakeId, code, user_id: getStoredUserId() }),
    });
    if (!res.ok) throw new Error('Retest failed');
    return res.json();
  },

  // Spaced Revision
  async getDueRevisions(userId = getStoredUserId()): Promise<RevisionItem[]> {
    const res = await fetch(`${API_BASE}/revisions/due?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load due revisions');
    return res.json();
  },

  async completeRevision(revisionId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/revisions/${revisionId}/complete`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to complete revision');
    return res.json();
  },

  // Debug Lab
  async getDebugExercises(): Promise<DebugExercise[]> {
    const res = await fetch(`${API_BASE}/debug_lab`);
    if (!res.ok) throw new Error('Failed to load debug exercises');
    return res.json();
  },

  async getDebugExercise(id: string): Promise<DebugExercise> {
    const res = await fetch(`${API_BASE}/debug_lab/${id}`);
    if (!res.ok) throw new Error('Failed to load debug exercise');
    return res.json();
  },

  async submitDebugSolution(id: string, code: string): Promise<{
    is_fixed: boolean;
    stdout: string;
    error?: string;
    explanation: string;
  }> {
    const res = await fetch(`${API_BASE}/debug_lab/${id}/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ exercise_id: id, code, user_id: getStoredUserId() }),
    });
    if (!res.ok) throw new Error('Debug submission failed');
    return res.json();
  },

  // Logic Gym
  async getLogicPuzzles(): Promise<LogicPuzzle[]> {
    const res = await fetch(`${API_BASE}/logic_gym`);
    if (!res.ok) throw new Error('Failed to load logic puzzles');
    return res.json();
  },

  async submitLogicAnswer(puzzleId: string, answer: string): Promise<{
    is_correct: boolean;
    correct_answer: string;
    explanation: string;
  }> {
    const res = await fetch(`${API_BASE}/logic_gym/${puzzleId}/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ puzzle_id: puzzleId, answer, user_id: getStoredUserId() }),
    });
    if (!res.ok) throw new Error('Logic answer submission failed');
    return res.json();
  }
};
