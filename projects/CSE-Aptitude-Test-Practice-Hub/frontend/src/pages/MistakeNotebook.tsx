import React, { useEffect, useState } from 'react';
import { BookX, CheckCircle2, RotateCcw, Search, Filter, AlertCircle, X } from 'lucide-react';
import { api } from '../api/client';
import { MistakeRecord, Topic } from '../types';

export const MistakeNotebook: React.FC = () => {
  const [mistakes, setMistakes] = useState<MistakeRecord[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');

  // Retest Modal state
  const [activeRetest, setActiveRetest] = useState<MistakeRecord | null>(null);
  const [retestAnswer, setRetestAnswer] = useState('');
  const [retestResult, setRetestResult] = useState<{ is_correct: boolean; feedback: string } | null>(null);
  const [isRetesting, setIsRetesting] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [mRes, tRes] = await Promise.all([
        api.getMistakes(),
        api.getTopics()
      ]);
      setMistakes(mRes);
      setTopics(tRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRetestSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeRetest || !retestAnswer.trim()) return;

    setIsRetesting(true);
    try {
      const res = await api.retestMistake(activeRetest.id, retestAnswer);
      setRetestResult(res);
      // Refresh mistakes list
      const updated = await api.getMistakes();
      setMistakes(updated);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRetesting(false);
    }
  };

  const filteredMistakes = mistakes.filter((m) => {
    if (selectedTopic !== 'All' && m.topic_id !== selectedTopic) return false;
    if (selectedCategory !== 'All' && m.error_category !== selectedCategory) return false;
    if (selectedStatus !== 'All' && m.retest_status !== selectedStatus) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        m.question_text.toLowerCase().includes(q) ||
        m.what_went_wrong.toLowerCase().includes(q) ||
        m.error_category.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const errorCategories = ['All', ...new Set(mistakes.map((m) => m.error_category))];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Mistake Notebook</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Transform errors into lasting intuition. Diagnose root causes and retest until mastery is achieved.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search mistakes by problem keywords or diagnosis..."
              className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              <option value="All">All Topics</option>
              {topics.map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              <option value="All">All Error Types</option>
              {errorCategories.filter((c) => c !== 'All').map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              <option value="All">All Statuses</option>
              <option value="pending">Pending Retest</option>
              <option value="retested_passed">Passed Retest</option>
              <option value="retested_failed">Failed Retest</option>
            </select>
          </div>
        </div>
      </div>

      {/* Mistake Records List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center text-slate-400 gap-2">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs">Loading notebook records...</p>
        </div>
      ) : filteredMistakes.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 space-y-2">
          <BookX className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-sm font-bold text-slate-800">No Mistakes Recorded</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            When you solve questions and encounter an incorrect result, the AI diagnosis engine logs the error here with corrective steps.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredMistakes.map((m) => (
            <div
              key={m.id}
              className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-4 hover:border-slate-300 transition-colors"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md">
                    {m.topic_name}
                  </span>
                  <span className="text-xs font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-md">
                    {m.error_category}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full capitalize ${
                    m.retest_status === 'retested_passed'
                      ? 'bg-emerald-100 text-emerald-800'
                      : m.retest_status === 'retested_failed'
                      ? 'bg-rose-100 text-rose-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}>
                    {m.retest_status.replace('_', ' ')}
                  </span>
                  <button
                    onClick={() => {
                      setActiveRetest(m);
                      setRetestAnswer('');
                      setRetestResult(null);
                    }}
                    className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
                  >
                    <RotateCcw className="w-3 h-3" />
                    <span>Retest Concept</span>
                  </button>
                </div>
              </div>

              {/* Problem & Given Answer */}
              <div className="space-y-1">
                <div className="text-xs font-bold text-slate-500">Question:</div>
                <div className="text-xs sm:text-sm font-semibold text-slate-900">{m.question_text}</div>
                <div className="flex items-center gap-4 text-xs pt-1 font-mono">
                  <span className="text-rose-700">Your Answer: <strong>{m.submitted_answer || '(Empty)'}</strong></span>
                  <span className="text-emerald-700">Expected: <strong>{m.correct_answer}</strong></span>
                </div>
              </div>

              {/* Diagnosis Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                <div>
                  <span className="font-bold text-slate-800">Root Cause:</span> {m.what_went_wrong}
                </div>
                <div>
                  <span className="font-bold text-slate-800">Correct Reasoning:</span> {m.correct_reasoning}
                </div>
                <div className="md:col-span-2 text-blue-900 border-t border-slate-200/60 pt-2 font-medium">
                  <span className="font-bold">How to Avoid Next Time:</span> {m.how_to_avoid}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Retest Modal */}
      {activeRetest && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
            <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
              <div className="flex items-center gap-2">
                <RotateCcw className="w-5 h-5 text-blue-600" />
                <h3 className="font-bold text-slate-900 text-sm">Retest Concept: {activeRetest.topic_name}</h3>
              </div>
              <button
                onClick={() => setActiveRetest(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleRetestSubmit} className="p-5 space-y-4">
              <div className="text-xs text-slate-800 font-semibold p-3 bg-slate-50 rounded-xl border border-slate-200">
                {activeRetest.question_text}
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700">Your New Calculated Answer:</label>
                <input
                  type="text"
                  value={retestAnswer}
                  onChange={(e) => setRetestAnswer(e.target.value)}
                  placeholder="Enter corrected answer..."
                  className="w-full px-3 py-2 text-xs font-mono rounded-lg border border-slate-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              {retestResult && (
                <div className={`p-3 rounded-xl border text-xs font-medium ${
                  retestResult.is_correct
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                    : 'bg-rose-50 border-rose-200 text-rose-900'
                }`}>
                  {retestResult.feedback}
                </div>
              )}

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setActiveRetest(null)}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-100"
                >
                  Close
                </button>
                <button
                  type="submit"
                  disabled={isRetesting || !retestAnswer.trim()}
                  className="px-4 py-1.5 text-xs font-bold rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-40"
                >
                  {isRetesting ? 'Checking...' : 'Submit Retest'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
