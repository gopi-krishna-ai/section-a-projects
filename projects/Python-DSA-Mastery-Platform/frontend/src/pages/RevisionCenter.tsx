import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { RevisionItem } from '../types';
import { 
  RotateCcw, 
  Calendar, 
  CheckCircle2, 
  Clock, 
  ArrowRight, 
  Sparkles, 
  BookOpen, 
  Zap,
  TrendingUp,
  Brain
} from 'lucide-react';

export const RevisionCenter: React.FC = () => {
  const [revisions, setRevisions] = useState<RevisionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [completingId, setCompletingId] = useState<string | null>(null);

  useEffect(() => {
    loadRevisions();
  }, []);

  async function loadRevisions() {
    try {
      setLoading(true);
      const data = await api.getDueRevisions();
      setRevisions(data);
    } catch (err) {
      console.error('Failed to load revisions', err);
    } finally {
      setLoading(false);
    }
  }

  const handleComplete = async (revId: string) => {
    try {
      setCompletingId(revId);
      await api.completeRevision(revId);
      setRevisions(prev => prev.filter(r => r.id !== revId));
    } catch (err) {
      console.error('Failed to complete revision', err);
    } finally {
      setCompletingId(null);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-amber-950 to-slate-900 border border-amber-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-bold mb-3 border border-amber-500/30">
            <RotateCcw className="w-3.5 h-3.5" />
            <span>SuperMemo SM-2 Spaced Repetition Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Spaced Repetition & Retention Center
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            The human brain forgets 80% of learned coding algorithms within 7 days unless strategically reactivated. Our SM-2 engine schedules reviews at 1, 3, 7, 14, and 30-day intervals for permanent long-term memory.
          </p>
        </div>

        <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 flex items-center gap-6 shrink-0">
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Due for Review</div>
            <div className="text-2xl font-black text-amber-400">{revisions.length}</div>
          </div>
          <div className="h-8 w-px bg-slate-800" />
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Algorithm</div>
            <div className="text-sm font-bold text-white">SM-2 Spaced</div>
          </div>
        </div>
      </div>

      {/* Due Items List */}
      {loading ? (
        <div className="flex items-center justify-center min-h-[300px]">
          <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : revisions.length === 0 ? (
        <div className="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800">
          <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white">All Caught Up!</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-md mx-auto">
            You have completed all scheduled spaced revisions for today. Continue learning in Python Academy or solve new challenges in the Problem Library!
          </p>
          <div className="flex justify-center gap-3 mt-5">
            <Link
              to="/python"
              className="px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition-all"
            >
              Python Academy
            </Link>
            <Link
              to="/problems"
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all border border-slate-700"
            >
              Browse Problems
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 px-1">
            Items Requiring Memory Reactivation ({revisions.length})
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {revisions.map((rev) => (
              <div
                key={rev.id}
                className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/40 transition-all flex flex-col justify-between space-y-4 shadow-lg"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    <span className="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 text-amber-300 border border-amber-500/20 flex items-center gap-1.5">
                      <Clock className="w-3 h-3" />
                      Repetition #{rev.repetition_number + 1}
                    </span>
                    <span className="text-[11px] text-slate-400 font-semibold">
                      Interval: {rev.interval_days} {rev.interval_days === 1 ? 'day' : 'days'}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-white">
                    {rev.problem_title || 'Core Algorithmic Concept'}
                  </h3>

                  <div className="mt-3 p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs text-slate-300 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Topic:</span>
                      <span className="font-semibold text-white">{rev.topic_title}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Difficulty:</span>
                      <span className="font-bold text-amber-300">{rev.difficulty}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-400">Scheduled Due:</span>
                      <span className="text-slate-300">{new Date(rev.due_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-3">
                  {rev.problem_id ? (
                    <Link
                      to={`/workspace/${rev.problem_id}`}
                      className="inline-flex items-center gap-1 text-xs font-bold text-sky-400 hover:text-sky-300 transition-colors"
                    >
                      <span>Review Problem</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <span className="text-xs text-slate-500">Conceptual Review</span>
                  )}

                  <button
                    disabled={completingId === rev.id}
                    onClick={() => handleComplete(rev.id)}
                    className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-md shadow-emerald-600/20 flex items-center gap-1.5 cursor-pointer"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    {completingId === rev.id ? 'Saving...' : 'Mark Reviewed'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
