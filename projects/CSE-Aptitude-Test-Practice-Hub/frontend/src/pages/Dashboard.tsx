import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen, Zap, RotateCcw, BookX, ArrowRight, CheckCircle2,
  AlertTriangle, TrendingUp, HelpCircle, Target
} from 'lucide-react';
import { api } from '../api/client';
import { DashboardData } from '../types';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboard();
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard metrics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-500 gap-3">
        <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-medium">Loading your personalized aptitude coach data...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-8">
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-sm">
          {error || 'Unable to connect to learning database.'}
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Hero Action Banner */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-400/30 text-xs font-semibold text-blue-200">
            <Target className="w-3.5 h-3.5 text-blue-300" />
            <span>Placement Preparation Hub</span>
          </div>
          <h1 className="text-xl sm:text-3xl font-extrabold tracking-tight">
            Master Aptitude Problem-Solving
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Move beyond memorization. Understand <span className="text-blue-300 font-semibold">HOW</span> to approach questions,{' '}
            <span className="text-blue-300 font-semibold">WHY</span> methods work, and{' '}
            <span className="text-blue-300 font-semibold">WHEN</span> to apply them under placement pressure.
          </p>

          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => navigate('/workspace')}
              className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 font-bold text-xs sm:text-sm text-white shadow-lg shadow-emerald-500/25 flex items-center gap-2 transition-all cursor-pointer"
            >
              <Zap className="w-4 h-4 text-amber-200" />
              <span>Solve Questions Now</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            {data.recommended_next_lesson ? (
              <button
                onClick={() => navigate(`/learn?topic=${data.recommended_next_lesson?.topic_id}`)}
                className="px-5 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 font-semibold text-xs sm:text-sm text-white shadow-lg shadow-blue-500/25 flex items-center gap-2 transition-all cursor-pointer"
              >
                <BookOpen className="w-4 h-4 text-blue-200" />
                <span>Concept Lesson: {data.recommended_next_lesson.topic_name}</span>
              </button>
            ) : (
              <button
                onClick={() => navigate('/practice')}
                className="px-5 py-2.5 rounded-xl bg-blue-500 hover:bg-blue-600 font-semibold text-xs sm:text-sm text-white shadow-lg shadow-blue-500/25 flex items-center gap-2 transition-all cursor-pointer"
              >
                <span>Practice Modes</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}

            <button
              onClick={() => navigate('/mock-tests')}
              className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 font-semibold text-xs sm:text-sm text-white border border-white/20 flex items-center gap-2 transition-colors cursor-pointer"
            >
              <Target className="w-4 h-4 text-amber-400" />
              <span>Placement Mock Exams</span>
            </button>

            {data.top_repeated_mistakes.length > 0 && (
              <button
                onClick={() => navigate('/mistakes')}
                className="px-4 py-2.5 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 border border-rose-400/30 font-semibold text-xs sm:text-sm flex items-center gap-2 transition-colors cursor-pointer"
              >
                <BookX className="w-4 h-4 text-rose-400" />
                <span>Review Mistakes ({data.top_repeated_mistakes.length})</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Verified Bank</div>
          <div className="text-2xl font-bold text-slate-900">{data.total_repository_questions}</div>
          <div className="text-[11px] text-emerald-600 font-medium">Original repository items</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Unique Solved</div>
          <div className="text-2xl font-bold text-slate-900">
            {data.total_solved_correct} <span className="text-xs text-slate-400 font-normal">/ {data.total_attempted_unique}</span>
          </div>
          <div className="text-[11px] text-blue-600 font-medium">Distinct questions attempted</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Unassisted Accuracy</div>
          <div className="text-2xl font-bold text-slate-900">{data.unassisted_accuracy}%</div>
          <div className="text-[11px] text-slate-500 font-medium">Overall accuracy: {data.overall_accuracy}%</div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Due For Revision</div>
          <div className="text-2xl font-bold text-amber-600">{data.due_revisions_count}</div>
          <div className="text-[11px] text-amber-700 font-medium">Spaced repetition queue</div>
        </div>
      </div>

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Studying & Needs Improvement */}
        <div className="lg:col-span-2 space-y-6">
          {/* Topics Needing Improvement */}
          {data.topics_needing_improvement.length > 0 && (
            <div className="bg-white rounded-xl border border-amber-200/80 shadow-xs p-5">
              <div className="flex items-center gap-2 mb-3">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
                <h3 className="font-bold text-slate-900 text-sm sm:text-base">Targeted Improvement Needed</h3>
              </div>
              <p className="text-xs text-slate-600 mb-4">
                These topics show lower accuracy or have errors requiring targeted remediation before placement tests.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {data.topics_needing_improvement.map((t) => (
                  <div
                    key={t.topic_id}
                    onClick={() => navigate(`/workspace?topic=${t.topic_id}`)}
                    className="p-3 rounded-lg border border-slate-200 bg-slate-50/70 hover:bg-white hover:border-blue-400 transition-all cursor-pointer flex items-center justify-between"
                  >
                    <div>
                      <div className="text-xs font-bold text-slate-800">{t.topic_name}</div>
                      <div className="text-[11px] text-slate-500">{t.category}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs font-bold text-amber-600">{t.mastery_score}% mastery</div>
                      <div className="text-[10px] text-slate-400">{t.total_correct}/{t.total_attempted} correct</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Current Studying Topics */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-600" />
                <h3 className="font-bold text-slate-900 text-sm sm:text-base">Active Study Topics</h3>
              </div>
              <button
                onClick={() => navigate('/learn')}
                className="text-xs font-semibold text-blue-600 hover:text-blue-700"
              >
                Browse Syllabus →
              </button>
            </div>

            {data.current_studying_topics.length === 0 ? (
              <div className="py-8 text-center text-slate-500 text-xs">
                No active topics yet. Start your first lesson from the syllabus or practice mode!
              </div>
            ) : (
              <div className="space-y-3">
                {data.current_studying_topics.map((t) => (
                  <div
                    key={t.topic_id}
                    className="p-3.5 rounded-xl border border-slate-200 bg-white hover:border-slate-300 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-bold text-slate-800">{t.topic_name}</span>
                      <span className="text-xs font-bold text-blue-600">{t.mastery_score}%</span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${Math.min(100, t.mastery_score)}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between mt-2 text-[11px] text-slate-500">
                      <span>Status: <span className="font-medium text-slate-700 capitalize">{t.status.replace('_', ' ')}</span></span>
                      <span>{t.total_correct} / {t.total_attempted} attempts correct</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Error Taxonomy & Recent Activity */}
        <div className="space-y-6">
          {/* Top Repeated Errors */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5">
            <div className="flex items-center gap-2 mb-3">
              <BookX className="w-5 h-5 text-rose-600" />
              <h3 className="font-bold text-slate-900 text-sm sm:text-base">Mistake Diagnostics</h3>
            </div>
            <p className="text-xs text-slate-600 mb-3">
              Top observed error patterns in your practice:
            </p>

            {data.top_repeated_mistakes.length === 0 ? (
              <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-200 text-emerald-800 text-xs text-center font-medium">
                No repeated error patterns yet. Keep up the clean problem-solving!
              </div>
            ) : (
              <div className="space-y-2">
                {data.top_repeated_mistakes.map((m, idx) => (
                  <div
                    key={idx}
                    className="p-2.5 rounded-lg border border-slate-200 bg-slate-50 flex items-center justify-between text-xs"
                  >
                    <span className="font-medium text-slate-800 truncate mr-2">{m.error_category}</span>
                    <span className="px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 font-bold shrink-0">
                      {m.count} {m.count === 1 ? 'time' : 'times'}
                    </span>
                  </div>
                ))}
                <button
                  onClick={() => navigate('/mistakes')}
                  className="w-full mt-2 py-2 text-xs font-semibold text-rose-700 hover:text-rose-800 hover:bg-rose-50 rounded-lg transition-colors"
                >
                  Open Mistake Notebook →
                </button>
              </div>
            )}
          </div>

          {/* Quick Revision Card */}
          <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl border border-amber-200 p-5 space-y-3">
            <div className="flex items-center gap-2 text-amber-900 font-bold text-sm">
              <RotateCcw className="w-4 h-4 text-amber-600" />
              <span>Spaced Repetition</span>
            </div>
            <p className="text-xs text-amber-900/80 leading-relaxed">
              Long-term retention requires retrieving concepts at calculated delays (1d, 3d, 7d, 14d).
            </p>
            <div className="flex items-center justify-between text-xs font-semibold text-amber-950 pt-1">
              <span>{data.due_revisions_count} questions waiting</span>
              <button
                onClick={() => navigate('/revision')}
                className="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-bold transition-colors cursor-pointer"
              >
                Review Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
