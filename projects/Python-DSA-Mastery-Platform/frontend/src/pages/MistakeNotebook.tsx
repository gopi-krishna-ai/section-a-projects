import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { MistakeRecord } from '../types';
import { 
  BookX, 
  Search, 
  RotateCcw, 
  CheckCircle2, 
  Clock, 
  AlertTriangle, 
  ShieldAlert, 
  Code2, 
  X, 
  Play,
  Lightbulb
} from 'lucide-react';

export const MistakeNotebook: React.FC = () => {
  const [mistakes, setMistakes] = useState<MistakeRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  // Retest Modal state
  const [retestModalOpen, setRetestModalOpen] = useState(false);
  const [selectedMistake, setSelectedMistake] = useState<MistakeRecord | null>(null);
  const [retestCode, setRetestCode] = useState('');
  const [retesting, setRetesting] = useState(false);
  const [retestResult, setRetestResult] = useState<{
    is_resolved: boolean;
    passes_count: number;
    total_tests: number;
    feedback: string;
  } | null>(null);

  useEffect(() => {
    loadMistakes();
  }, [categoryFilter, statusFilter]);

  async function loadMistakes() {
    try {
      setLoading(true);
      const data = await api.getMistakes(
        undefined,
        statusFilter === 'all' ? undefined : statusFilter,
        categoryFilter === 'all' ? undefined : categoryFilter
      );
      setMistakes(data);
    } catch (err) {
      console.error('Failed to load mistakes', err);
    } finally {
      setLoading(false);
    }
  }

  const handleOpenRetest = (m: MistakeRecord) => {
    setSelectedMistake(m);
    setRetestCode(m.submitted_code || '# Write your corrected solution here\n');
    setRetestResult(null);
    setRetestModalOpen(true);
  };

  const handleExecuteRetest = async () => {
    if (!selectedMistake) return;
    try {
      setRetesting(true);
      const res = await api.retestMistake(selectedMistake.id, retestCode);
      setRetestResult(res);
      if (res.is_resolved) {
        // Refresh mistake list
        loadMistakes();
      }
    } catch (err) {
      console.error('Retest execution failed', err);
    } finally {
      setRetesting(false);
    }
  };

  const filteredMistakes = mistakes.filter(m => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      m.error_category.toLowerCase().includes(q) ||
      m.what_went_wrong.toLowerCase().includes(q) ||
      m.why_it_went_wrong.toLowerCase().includes(q) ||
      m.how_to_avoid.toLowerCase().includes(q)
    );
  });

  const resolvedCount = mistakes.filter(m => m.retest_status === 'resolved').length;
  const pendingCount = mistakes.filter(m => m.retest_status === 'pending').length;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-rose-950 to-slate-900 border border-rose-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 text-xs font-bold mb-3 border border-rose-500/30">
            <BookX className="w-3.5 h-3.5" />
            <span>22-Pattern Cognitive Mistake Taxonomy</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Mistake Notebook & Error Diagnosis
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Every failed test or syntax error is categorized into our 22-category taxonomy. Retest your past mistakes to prove genuine retention and eradicate recurring cognitive blindspots.
          </p>
        </div>

        <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 flex items-center gap-6 shrink-0">
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Pending Retests</div>
            <div className="text-2xl font-black text-amber-400">{pendingCount}</div>
          </div>
          <div className="h-8 w-px bg-slate-800" />
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Resolved</div>
            <div className="text-2xl font-black text-emerald-400">{resolvedCount}</div>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-900/70 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search mistakes, causes..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {/* Status filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-rose-500"
          >
            <option value="all">All Statuses</option>
            <option value="pending">Pending Retest</option>
            <option value="resolved">Resolved</option>
          </select>

          {/* Category filter */}
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-rose-500 max-w-[200px]"
          >
            <option value="all">All 22 Categories</option>
            <option value="off_by_one">Off-by-One Boundary</option>
            <option value="mutation_of_shared_state">Mutation of Shared State</option>
            <option value="shallow_copy_mutability">Shallow Copy Mutability</option>
            <option value="recursion_missing_base_case">Recursion Base Case</option>
            <option value="unhandled_empty_input">Unhandled Empty Input</option>
            <option value="unhandled_single_element">Unhandled Single Element</option>
            <option value="hash_collision_key_error">Key Error / Dict Lookup</option>
            <option value="time_limit_exceeded">Time Limit Exceeded</option>
            <option value="memory_limit_exceeded">Memory Limit Exceeded</option>
          </select>
        </div>
      </div>

      {/* Mistake Cards */}
      {loading ? (
        <div className="flex items-center justify-center min-h-[300px]">
          <div className="w-8 h-8 border-4 border-rose-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : filteredMistakes.length === 0 ? (
        <div className="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800">
          <CheckCircle2 className="w-10 h-10 text-emerald-400 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white">No mistakes found</h3>
          <p className="text-xs text-slate-400 mt-1">
            {search || categoryFilter !== 'all' || statusFilter !== 'all'
              ? 'No records match your selected criteria.'
              : 'You have zero unaddressed mistakes. Excellent execution!'}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredMistakes.map((m) => (
            <div
              key={m.id}
              className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between space-y-4"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-rose-500/10 text-rose-400 border border-rose-500/20">
                    {m.error_category.replace(/_/g, ' ')}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase flex items-center gap-1 ${
                    m.retest_status === 'resolved'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  }`}>
                    {m.retest_status === 'resolved' ? (
                      <CheckCircle2 className="w-3 h-3" />
                    ) : (
                      <Clock className="w-3 h-3" />
                    )}
                    {m.retest_status}
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div>
                    <span className="font-bold text-slate-300">Root Cause:</span>
                    <p className="text-slate-400 mt-0.5 leading-relaxed">{m.what_went_wrong}</p>
                    {m.why_it_went_wrong && (
                      <p className="text-slate-500 mt-0.5 italic">{m.why_it_went_wrong}</p>
                    )}
                  </div>

                  <div className="p-3 rounded-lg bg-slate-950 border border-slate-800/80">
                    <span className="font-bold text-amber-300 flex items-center gap-1">
                      <Lightbulb className="w-3 h-3" /> Corrective Check:
                    </span>
                    <p className="text-slate-300 mt-1 leading-relaxed">{m.how_to_avoid}</p>
                  </div>

                  {m.submitted_code && (
                    <div className="mt-2">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1">
                        Recorded Code Snippet:
                      </div>
                      <pre className="p-2.5 rounded-lg bg-slate-950 font-mono text-[11px] text-slate-400 overflow-x-auto max-h-24">
                        {m.submitted_code}
                      </pre>
                    </div>
                  )}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  Recorded: {new Date(m.created_at).toLocaleDateString()}
                </span>
                <button
                  onClick={() => handleOpenRetest(m)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-all shadow-md shadow-rose-600/20 cursor-pointer"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  Retest Question
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Retest Modal */}
      {retestModalOpen && selectedMistake && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl overflow-y-auto max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <RotateCcw className="w-4 h-4 text-rose-400" />
                  Retest & Resolve Mistake
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Category: {selectedMistake.error_category.replace(/_/g, ' ')}
                </p>
              </div>
              <button
                onClick={() => setRetestModalOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200">
              <strong>Corrective Invariant:</strong> {selectedMistake.how_to_avoid}
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1">
                Your Corrected Python Code:
              </label>
              <textarea
                value={retestCode}
                onChange={(e) => setRetestCode(e.target.value)}
                rows={10}
                className="w-full font-mono text-xs text-emerald-300 bg-slate-950 border border-slate-800 rounded-xl p-3.5 focus:outline-none focus:border-rose-500 leading-relaxed"
                spellCheck={false}
              />
            </div>

            {retestResult && (
              <div className={`p-4 rounded-xl border text-xs ${
                retestResult.is_resolved
                  ? 'bg-emerald-950/30 border-emerald-500/50 text-emerald-200'
                  : 'bg-rose-950/30 border-rose-500/50 text-rose-200'
              }`}>
                <div className="font-bold mb-1 flex items-center gap-2 text-sm">
                  {retestResult.is_resolved ? (
                    <>
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      Resolved! ({retestResult.passes_count}/{retestResult.total_tests} tests passed)
                    </>
                  ) : (
                    <>
                      <AlertTriangle className="w-4 h-4 text-rose-400" />
                      Not yet resolved ({retestResult.passes_count}/{retestResult.total_tests} tests passed)
                    </>
                  )}
                </div>
                <p>{retestResult.feedback}</p>
              </div>
            )}

            <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
              <button
                onClick={() => setRetestModalOpen(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Close
              </button>
              <button
                disabled={retesting}
                onClick={handleExecuteRetest}
                className="px-5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-all shadow-md flex items-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                {retesting ? 'Testing...' : 'Verify Corrected Code'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
