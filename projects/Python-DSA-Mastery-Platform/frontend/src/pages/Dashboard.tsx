import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Terminal, Binary, Brain, ArrowRight, Zap, CheckCircle2,
  AlertTriangle, RotateCcw, Bug, ShieldCheck, Flame, BookOpen, Target
} from 'lucide-react';
import { api } from '../api/client';
import { DashboardData } from '../types';
import { useAuth } from '../context/AuthContext';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { currentUser } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, [currentUser]);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboard();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-400 gap-3">
        <div className="w-8 h-8 border-3 border-sky-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono">Loading developer diagnostics & progress...</p>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto text-slate-100">
      {/* Hero Banner */}
      <div className="bg-gradient-to-r from-sky-950 via-slate-900 to-indigo-950 border border-sky-900/50 rounded-3xl p-6 sm:p-8 relative overflow-hidden shadow-2xl">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20 text-xs font-bold text-sky-400">
            <Target className="w-3.5 h-3.5" />
            <span>Target: {currentUser?.target_goal || 'FAANG & Competitive DSA'}</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold tracking-tight text-white">
            Independent Coding Mastery
          </h1>

          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Move beyond memorization. Build algorithmic thinking to solve unfamiliar problems without tutorials, hints, or AI crutches.
          </p>

          <div className="pt-3 flex flex-wrap gap-3">
            {data.recommended_next_task ? (
              <button
                onClick={() => navigate(`/workspace/${data.recommended_next_task?.id}`)}
                className="px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 font-bold text-xs sm:text-sm text-slate-950 shadow-lg shadow-sky-500/25 flex items-center gap-2 transition-all cursor-pointer"
              >
                <span>Solve Recommended: {data.recommended_next_task.title}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={() => navigate('/problems')}
                className="px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 font-bold text-xs sm:text-sm text-slate-950 shadow-lg shadow-sky-500/25 flex items-center gap-2 transition-all cursor-pointer"
              >
                <span>Browse Practice Problems</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}

            <button
              onClick={() => navigate('/python')}
              className="px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 font-semibold text-xs sm:text-sm text-white border border-slate-700 flex items-center gap-2 transition-colors cursor-pointer"
            >
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span>Python Academy</span>
            </button>

            <button
              onClick={() => navigate('/logic')}
              className="px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 font-semibold text-xs sm:text-sm text-white border border-slate-700 flex items-center gap-2 transition-colors cursor-pointer"
            >
              <Brain className="w-4 h-4 text-purple-400" />
              <span>Logic Gym</span>
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-sm space-y-1">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Independent Solved</div>
          <div className="text-2xl font-black text-white">
            {data.independent_solved}{' '}
            <span className="text-xs font-normal text-slate-500">/ {data.total_solved} solved</span>
          </div>
          <div className="text-[11px] text-emerald-400 font-semibold flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>{data.independent_accuracy}% unassisted</span>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-sm space-y-1">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Overall Accuracy</div>
          <div className="text-2xl font-black text-sky-400">{data.overall_accuracy}%</div>
          <div className="text-[11px] text-slate-400 font-medium">{data.total_attempted} problems attempted</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-sm space-y-1">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Due For Revision</div>
          <div className="text-2xl font-black text-amber-400">{data.due_revisions_count}</div>
          <div className="text-[11px] text-amber-300 font-medium">SM-2 retention queue</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-sm space-y-1">
          <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Learning Streak</div>
          <div className="text-2xl font-black text-white flex items-center gap-1.5">
            <span>{data.streak_days} Days</span>
            <Flame className="w-5 h-5 text-orange-400" />
          </div>
          <div className="text-[11px] text-slate-400 font-medium">Consistent daily reasoning</div>
        </div>
      </div>

      {/* 2-Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Left Column (2 Cols): Active Topics & Focus Areas */}
        <div className="lg:col-span-2 space-y-6">
          {/* Active Mastery Topics */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Binary className="w-4 h-4 text-sky-400" />
                <h3 className="font-bold text-sm text-white">Active Curriculum Topics</h3>
              </div>
              <button
                onClick={() => navigate('/dsa')}
                className="text-xs font-semibold text-sky-400 hover:text-sky-300"
              >
                View Roadmap →
              </button>
            </div>

            {data.active_topics.length === 0 ? (
              <div className="py-8 text-center text-slate-500 text-xs">
                No active topics yet. Select a problem from the library to begin!
              </div>
            ) : (
              <div className="space-y-3">
                {data.active_topics.map((t) => (
                  <div
                    key={t.topic_id}
                    className="p-3.5 rounded-xl border border-slate-800/80 bg-slate-950/50 space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs font-bold">
                      <span className="text-white">{t.title}</span>
                      <span className="text-sky-400">{t.mastery_score}% mastery</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-sky-500 h-2 rounded-full transition-all"
                        style={{ width: `${Math.min(100, t.mastery_score)}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-400">
                      <span className="capitalize text-slate-300 font-medium">{t.status.replace('_', ' ')}</span>
                      <span>
                        {t.independent_solved} independent / {t.total_attempted} attempts
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Submissions */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
            <h3 className="font-bold text-sm text-white">Recent Problem Solves</h3>
            {data.recent_submissions.length === 0 ? (
              <div className="py-6 text-center text-slate-500 text-xs">
                No recent submissions recorded yet.
              </div>
            ) : (
              <div className="divide-y divide-slate-800">
                {data.recent_submissions.map((sub, idx) => (
                  <div key={idx} className="py-3 flex items-center justify-between text-xs">
                    <div>
                      <div className="font-bold text-white">{sub.problem_title}</div>
                      <div className="text-[10px] text-slate-400">
                        {sub.is_independent ? (
                          <span className="text-emerald-400 font-semibold">Independent solve</span>
                        ) : (
                          <span className="text-amber-400 font-semibold">{sub.hints_used} hints used</span>
                        )}
                        {' '}&bull; {sub.execution_time_ms} ms
                      </div>
                    </div>
                    <span
                      className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                        sub.status === 'Passed'
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                          : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                      }`}
                    >
                      {sub.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Mistake Patterns & Focus */}
        <div className="space-y-6">
          {/* Top Mistake Taxonomies */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bug className="w-4 h-4 text-rose-400" />
                <h3 className="font-bold text-sm text-white">Mistake Diagnostics</h3>
              </div>
              <button
                onClick={() => navigate('/mistakes')}
                className="text-xs font-semibold text-rose-400 hover:text-rose-300"
              >
                Notebook →
              </button>
            </div>
            <p className="text-xs text-slate-400">
              Recurring cognitive error patterns identified across test failures:
            </p>

            {data.top_mistake_patterns.length === 0 ? (
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-xs text-center font-medium">
                No repeated error patterns detected yet.
              </div>
            ) : (
              <div className="space-y-2">
                {data.top_mistake_patterns.map((m, idx) => (
                  <div
                    key={idx}
                    className="p-2.5 rounded-xl border border-slate-800 bg-slate-950 flex items-center justify-between text-xs"
                  >
                    <span className="text-slate-200 font-medium truncate mr-2">{m.error_category}</span>
                    <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-bold shrink-0">
                      {m.count}x
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Shortcuts */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3">
            <h3 className="font-bold text-xs uppercase text-slate-400 tracking-wider">Quick Actions</h3>
            <div className="grid grid-cols-1 gap-2">
              <button
                onClick={() => navigate('/debug-lab')}
                className="p-3 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-left flex items-center justify-between text-xs font-semibold transition-colors cursor-pointer"
              >
                <span>Debugging Laboratory</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>
              <button
                onClick={() => navigate('/playground')}
                className="p-3 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-left flex items-center justify-between text-xs font-semibold transition-colors cursor-pointer"
              >
                <span>Freeform Code Playground</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>
              <button
                onClick={() => navigate('/revision')}
                className="p-3 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-left flex items-center justify-between text-xs font-semibold transition-colors cursor-pointer"
              >
                <span>Spaced Retention Queue ({data.due_revisions_count})</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
