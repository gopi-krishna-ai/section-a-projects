import React, { useEffect, useState } from 'react';
import { RotateCcw, CheckCircle2, Clock, Calendar, Check, XCircle } from 'lucide-react';
import { api } from '../api/client';
import { RevisionItem } from '../types';

export const Revision: React.FC = () => {
  const [items, setItems] = useState<RevisionItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [submittedAnswer, setSubmittedAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<any | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadRevisions();
  }, []);

  const loadRevisions = async () => {
    try {
      setLoading(true);
      const res = await api.getDueRevisions();
      setItems(res);
      setCurrentIndex(0);
      setResult(null);
      setSubmittedAnswer('');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const currentItem = items[currentIndex];

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentItem || !submittedAnswer.trim()) return;

    setIsSubmitting(true);
    try {
      const res = await api.reviewRevisionItem(currentItem.id, submittedAnswer);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < items.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setResult(null);
      setSubmittedAnswer('');
    } else {
      loadRevisions();
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-500 gap-3">
        <div className="w-8 h-8 border-3 border-amber-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-medium">Loading spaced revision queue...</p>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Spaced Revision Engine</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Reinforce long-term placement retention using spaced intervals (1d, 3d, 7d, 14d).
        </p>
      </div>

      {items.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 space-y-3">
          <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 mx-auto">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">All Revisions Cleared!</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            You have no pending spaced repetition cards due right now. Solve more questions in Practice Mode to build your schedule!
          </p>
        </div>
      ) : currentItem ? (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-5 p-6">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-amber-800 bg-amber-100 px-2.5 py-1 rounded-md">
                Card {currentIndex + 1} of {items.length}
              </span>
              <span className="text-xs font-semibold text-slate-700">
                {currentItem.topic_name} ({currentItem.category})
              </span>
            </div>

            <div className="flex items-center gap-3 text-xs text-slate-500">
              <span className="flex items-center gap-1 font-medium">
                <Clock className="w-3.5 h-3.5 text-slate-400" />
                Interval: {currentItem.interval_days} days
              </span>
              <span className="flex items-center gap-1 font-medium">
                <Calendar className="w-3.5 h-3.5 text-slate-400" />
                Repetition #{currentItem.repetition_number}
              </span>
            </div>
          </div>

          {/* Context if table/passage */}
          {currentItem.stimulus_context && (
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs font-mono whitespace-pre-wrap">
              {currentItem.stimulus_context}
            </div>
          )}

          {/* Question Text */}
          <div className="space-y-1">
            <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Test Problem</div>
            <p className="text-base sm:text-lg font-semibold text-slate-900 leading-relaxed">
              {currentItem.question_text}
            </p>
          </div>

          {/* Options if MCQ */}
          {currentItem.options && currentItem.options.length > 0 && (
            <div className="space-y-2">
              <div className="text-xs font-bold text-slate-600">Options:</div>
              <div className="grid grid-cols-1 gap-2">
                {currentItem.options.map((opt, i) => (
                  <div key={i} className="p-3 rounded-lg border border-slate-200 text-xs font-medium text-slate-800 bg-slate-50">
                    {opt}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Submission Form */}
          {!result ? (
            <form onSubmit={handleReviewSubmit} className="space-y-4 pt-2">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Retrieve and enter your answer:</label>
                <input
                  type="text"
                  value={submittedAnswer}
                  onChange={(e) => setSubmittedAnswer(e.target.value)}
                  placeholder="Enter answer from memory..."
                  className="w-full px-4 py-3 rounded-xl border border-slate-300 text-sm font-mono text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={isSubmitting || !submittedAnswer.trim()}
                  className="px-5 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs sm:text-sm shadow-sm transition-all disabled:opacity-40 cursor-pointer"
                >
                  {isSubmitting ? 'Verifying...' : 'Submit Retrieval Check'}
                </button>
              </div>
            </form>
          ) : (
            <div className={`p-5 rounded-2xl border space-y-3 ${
              result.is_correct ? 'bg-emerald-50 border-emerald-200' : 'bg-rose-50 border-rose-200'
            }`}>
              <div className="flex items-center gap-2">
                {result.is_correct ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-rose-600" />
                )}
                <span className={`text-sm font-bold ${
                  result.is_correct ? 'text-emerald-900' : 'text-rose-900'
                }`}>
                  {result.is_correct ? 'Retention Verified! Interval Advanced.' : 'Recall Lapsed. Reset to 1-Day Review.'}
                </span>
              </div>
              <div className="text-xs text-slate-700">{result.feedback}</div>

              <div className="p-3 bg-white rounded-xl border border-slate-200 text-xs text-slate-800 space-y-1">
                <div className="font-bold">Verified Reference Solution:</div>
                <div className="font-mono whitespace-pre-line text-slate-700">{result.reference_solution}</div>
              </div>

              <div className="flex justify-end pt-1">
                <button
                  onClick={handleNext}
                  className="px-4 py-2 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition-colors cursor-pointer"
                >
                  {currentIndex < items.length - 1 ? 'Next Revision Card →' : 'Finish Revision Set'}
                </button>
              </div>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
};
