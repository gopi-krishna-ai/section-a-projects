import {
  Topic, Question, SubmitAnswerResult, ProgressiveHint,
  StepGuidance, MistakeRecord, RevisionItem, ConceptLesson, DashboardData, UserAccount
} from '../types';

const API_BASE = '/api';

export const getStoredUserId = (): string => {
  return localStorage.getItem('aptitude_user_id') || 'default_user';
};

export const getStoredToken = (): string | null => {
  return localStorage.getItem('aptitude_auth_token');
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
  // Authentication & Users
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
    localStorage.setItem('aptitude_auth_token', data.token);
    localStorage.setItem('aptitude_user_id', data.user.id);
    localStorage.setItem('aptitude_user', JSON.stringify(data.user));
    return data;
  },

  async register(params: {
    username: string;
    password: string;
    email?: string;
    full_name?: string;
    target_company?: string;
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
    localStorage.setItem('aptitude_auth_token', data.token);
    localStorage.setItem('aptitude_user_id', data.user.id);
    localStorage.setItem('aptitude_user', JSON.stringify(data.user));
    return data;
  },

  async getMe(): Promise<UserAccount> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return res.json();
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
    localStorage.setItem('aptitude_auth_token', data.token);
    localStorage.setItem('aptitude_user_id', data.user.id);
    localStorage.setItem('aptitude_user', JSON.stringify(data.user));
    return data;
  },

  logout(): void {
    localStorage.removeItem('aptitude_auth_token');
    localStorage.removeItem('aptitude_user_id');
    localStorage.removeItem('aptitude_user');
  },

  // Dashboard & Analytics
  async getDashboard(userId = getStoredUserId()): Promise<DashboardData> {
    const res = await fetch(`${API_BASE}/analytics/dashboard?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load dashboard metrics');
    return res.json();
  },

  // Topics & Lessons
  async getTopics(userId = getStoredUserId()): Promise<Topic[]> {
    const res = await fetch(`${API_BASE}/topics?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load syllabus topics');
    return res.json();
  },

  async getTopicDetail(topicId: string, userId = getStoredUserId()): Promise<Topic> {
    const res = await fetch(`${API_BASE}/topics/${topicId}?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load topic details');
    return res.json();
  },

  async getTopicLesson(topicId: string): Promise<ConceptLesson> {
    const res = await fetch(`${API_BASE}/topics/${topicId}/lesson`);
    if (!res.ok) throw new Error('Failed to load concept lesson');
    return res.json();
  },

  // Questions
  async getQuestions(params: {
    topic_id?: string;
    category?: string;
    level?: string;
    question_type?: string;
    search?: string;
    skip?: number;
    limit?: number;
    user_id?: string;
  }): Promise<Question[]> {
    const query = new URLSearchParams();
    if (params.topic_id) query.append('topic_id', params.topic_id);
    if (params.category) query.append('category', params.category);
    if (params.level) query.append('level', params.level);
    if (params.question_type) query.append('question_type', params.question_type);
    if (params.search) query.append('search', params.search);
    query.append('user_id', params.user_id || getStoredUserId());
    if (params.skip !== undefined) query.append('skip', String(params.skip));
    if (params.limit !== undefined) query.append('limit', String(params.limit));

    const res = await fetch(`${API_BASE}/questions?${query.toString()}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load questions');
    return res.json();
  },

  async getQuestionDetail(questionId: string, userId = getStoredUserId()): Promise<Question> {
    const res = await fetch(`${API_BASE}/questions/${questionId}?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load question details');
    return res.json();
  },

  async submitAnswer(questionId: string, data: {
    submitted_answer: string;
    time_spent: number;
    hints_used: number;
    session_id?: string | null;
    scratchpad_notes?: string | null;
    user_id?: string;
  }): Promise<SubmitAnswerResult> {
    const res = await fetch(`${API_BASE}/questions/${questionId}/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: data.user_id || getStoredUserId(), ...data }),
    });
    if (!res.ok) throw new Error('Failed to submit answer');
    return res.json();
  },

  async getHint(questionId: string, hintLevel: number, currentAttempt?: string): Promise<ProgressiveHint> {
    const res = await fetch(`${API_BASE}/questions/${questionId}/hints`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ hint_level: hintLevel, current_attempt: currentAttempt }),
    });
    if (!res.ok) throw new Error('Failed to fetch hint');
    return res.json();
  },

  async getStepGuidance(questionId: string, stepName: string): Promise<StepGuidance> {
    const res = await fetch(`${API_BASE}/questions/${questionId}/step_tutor`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ step_name: stepName }),
    });
    if (!res.ok) throw new Error('Failed to fetch step guidance');
    return res.json();
  },

  async askAiTutor(questionId: string, query: string): Promise<{ provider: string; explanation: string; source: string }> {
    const res = await fetch(`${API_BASE}/questions/${questionId}/ask_ai`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error('AI Tutor unavailable');
    return res.json();
  },

  async toggleBookmark(questionId: string, notes?: string): Promise<{ is_bookmarked: boolean }> {
    const res = await fetch(`${API_BASE}/questions/${questionId}/bookmark`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: getStoredUserId(), notes }),
    });
    if (!res.ok) throw new Error('Failed to toggle bookmark');
    return res.json();
  },

  // Sessions
  async startSession(params: {
    mode: string;
    topic_id?: string | null;
    num_questions?: number;
    level?: string | null;
    user_id?: string;
  }): Promise<{ session_id: string; total_questions: number; questions: Question[] }> {
    const res = await fetch(`${API_BASE}/sessions/start`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: params.user_id || getStoredUserId(), ...params }),
    });
    if (!res.ok) throw new Error('Failed to start session');
    return res.json();
  },

  async completeSession(sessionId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/sessions/${sessionId}/complete`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to complete session');
    return res.json();
  },

  // Mistakes
  async getMistakes(params: {
    topic_id?: string;
    error_category?: string;
    retest_status?: string;
    user_id?: string;
  } = {}): Promise<MistakeRecord[]> {
    const query = new URLSearchParams();
    query.append('user_id', params.user_id || getStoredUserId());
    if (params.topic_id) query.append('topic_id', params.topic_id);
    if (params.error_category) query.append('error_category', params.error_category);
    if (params.retest_status) query.append('retest_status', params.retest_status);

    const res = await fetch(`${API_BASE}/mistakes?${query.toString()}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load mistakes');
    return res.json();
  },

  async retestMistake(mistakeId: string, submittedAnswer: string, timeSpent = 0): Promise<{
    mistake_id: string;
    is_correct: boolean;
    feedback: string;
    new_retest_status: string;
  }> {
    const res = await fetch(`${API_BASE}/mistakes/${mistakeId}/retest`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: getStoredUserId(), submitted_answer: submittedAnswer, time_spent: timeSpent }),
    });
    if (!res.ok) throw new Error('Failed to retest mistake');
    return res.json();
  },

  // Spaced Revisions
  async getDueRevisions(userId = getStoredUserId()): Promise<RevisionItem[]> {
    const res = await fetch(`${API_BASE}/revisions/due?user_id=${userId}`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Failed to load due revisions');
    return res.json();
  },

  async reviewRevisionItem(revisionId: string, submittedAnswer: string): Promise<any> {
    const res = await fetch(`${API_BASE}/revisions/${revisionId}/review`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: getStoredUserId(), submitted_answer: submittedAnswer }),
    });
    if (!res.ok) throw new Error('Failed to review revision item');
    return res.json();
  },

  // Mock Tests
  async getCompanyProfiles(): Promise<Record<string, any>> {
    const res = await fetch(`${API_BASE}/mock_tests/profiles`);
    if (!res.ok) throw new Error('Failed to load exam profiles');
    return res.json();
  },

  async startMockTest(params: {
    profile_id?: string;
    custom_categories?: string[];
    question_count?: number;
    time_limit_minutes?: number;
    user_id?: string;
  }): Promise<{
    session_id: string;
    title: string;
    time_limit_seconds: number;
    total_questions: number;
    questions: any[];
  }> {
    const res = await fetch(`${API_BASE}/mock_tests/start`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: params.user_id || getStoredUserId(), ...params }),
    });
    if (!res.ok) throw new Error('Failed to start mock test');
    return res.json();
  },

  async submitMockTest(sessionId: string, answers: Array<{
    question_id: string;
    submitted_answer: string;
    time_spent: number;
    is_marked_for_review: boolean;
  }>): Promise<any> {
    const res = await fetch(`${API_BASE}/mock_tests/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ user_id: getStoredUserId(), session_id: sessionId, answers }),
    });
    if (!res.ok) throw new Error('Failed to submit mock test');
    return res.json();
  }
};
