import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { LogicPuzzle } from '../types';
import { 
  Brain, 
  Sparkles, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  RotateCcw, 
  HelpCircle, 
  Lightbulb, 
  ChevronRight,
  ShieldCheck,
  Zap
} from 'lucide-react';

export const LogicGym: React.FC = () => {
  const [puzzles, setPuzzles] = useState<LogicPuzzle[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPuzzle, setSelectedPuzzle] = useState<LogicPuzzle | null>(null);
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [submissionResult, setSubmissionResult] = useState<{
    is_correct: boolean;
    correct_answer: string;
    explanation: string;
  } | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState<'puzzles' | 'patterns'>('puzzles');

  useEffect(() => {
    async function loadPuzzles() {
      try {
        setLoading(true);
        const data = await api.getLogicPuzzles();
        setPuzzles(data);
        if (data.length > 0) {
          setSelectedPuzzle(data[0]);
        }
      } catch (err) {
        console.error('Failed to load logic puzzles', err);
      } finally {
        setLoading(false);
      }
    }
    loadPuzzles();
  }, []);

  const handleSelectPuzzle = (puzzle: LogicPuzzle) => {
    setSelectedPuzzle(puzzle);
    setSelectedOption('');
    setSubmissionResult(null);
  };

  const handleSubmitAnswer = async () => {
    if (!selectedPuzzle || !selectedOption) return;
    try {
      setSubmitting(true);
      const res = await api.submitLogicAnswer(selectedPuzzle.id, selectedOption);
      setSubmissionResult(res);
    } catch (err) {
      console.error('Failed to submit answer', err);
    } finally {
      setSubmitting(false);
    }
  };

  const logicalPatterns = [
    { title: '1. Invariant Reasoning', desc: 'Identify a property that remains strictly true across every loop iteration or recursive step.' },
    { title: '2. Monotonicity & Predicates', desc: 'If property P(k) is True, does it guarantee P(k+1) is True? Enables O(log N) binary search on answer spaces.' },
    { title: '3. State Space Compression', desc: 'Instead of full history, determine the minimal information needed to make the next decision.' },
    { title: '4. Pigeonhole Principle', desc: 'If N items are put into M slots and N > M, at least one slot holds > 1 items. Proves cycle existence and collisions.' },
    { title: '5. Symmetry & Dual Problems', desc: 'Solving from back to front, or reversing perspective (e.g. buy/sell stock) simplifies state transitions.' },
    { title: '6. Extremal Principle', desc: 'Consider the smallest, largest, first, or last element to uncover structural constraints.' },
    { title: '7. Divide and Conquer', desc: 'Deconstruct a problem of size N into subproblems of size N/2, solve recursively, and combine in linear time.' },
    { title: '8. Greedy Choice Property', desc: 'Prove that local optimal choice leads to a global optimum using exchange arguments.' },
    { title: '9. Overlapping Subproblems', desc: 'Store previously computed intermediate results to reduce 2ⁿ branch explosions to polynomial time.' },
    { title: '10. Two-Pointer Convergent Space', desc: 'Shrink search intervals from both boundaries when sorting allows eliminating non-viable pairs.' },
    { title: '11. Sliding Window Boundary Invariant', desc: 'Maintain [left, right] window where condition holds, expanding right and contracting left.' },
    { title: '12. Fast & Slow Pointer Periodicity', desc: 'Move pointers at speeds 1 and 2 to detect linked list cycles and find midpoints in a single pass.' },
    { title: '13. Monotonic Stack/Queue Invariant', desc: 'Maintain elements in strictly increasing or decreasing order to resolve next greater element in O(N).' },
    { title: '14. Meet in the Middle', desc: 'Split search depth in half (e.g., 2⁴⁰ → 2²⁰ + 2²⁰) to solve otherwise intractable combinatorial searches.' },
    { title: '15. Counterexample Construction', desc: 'Stress test assumptions with edge cases: duplicates, empty inputs, negative numbers, odd/even parity.' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-purple-950 to-slate-900 border border-purple-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-bold mb-3 border border-purple-500/30">
            <Brain className="w-3.5 h-3.5" />
            <span>Algorithmic Thinking & Reasoning Gym</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Logic & Mental Model Gym
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Train your brain to recognize patterns, trace loops step-by-step, verify invariants, and construct counterexamples before typing code.
          </p>
        </div>

        {/* Tab switcher */}
        <div className="flex bg-slate-950 p-1.5 rounded-xl border border-slate-800 self-start md:self-center shrink-0">
          <button
            onClick={() => setActiveTab('puzzles')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              activeTab === 'puzzles'
                ? 'bg-purple-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Interactive Puzzles ({puzzles.length})
          </button>
          <button
            onClick={() => setActiveTab('patterns')}
            className={`px-4 py-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              activeTab === 'patterns'
                ? 'bg-purple-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            15 Reasoning Patterns
          </button>
        </div>
      </div>

      {activeTab === 'patterns' ? (
        /* 15 Patterns Reference */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {logicalPatterns.map((pat, idx) => (
            <div
              key={idx}
              className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-purple-500/40 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 rounded-md bg-purple-500/20 text-purple-400 flex items-center justify-center text-xs font-bold">
                    {idx + 1}
                  </div>
                  <h3 className="text-sm font-bold text-white">{pat.title.split('. ')[1]}</h3>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{pat.desc}</p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-purple-400 font-semibold">
                <span>Algorithmic Thinking</span>
                <Sparkles className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Puzzles Interface */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Puzzle selection column */}
          <div className="lg:col-span-1 space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 px-1 mb-2">
              Reasoning Challenges
            </h2>
            {puzzles.map((p) => {
              const isSelected = selectedPuzzle?.id === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => handleSelectPuzzle(p)}
                  className={`w-full text-left p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-3 ${
                    isSelected
                      ? 'bg-purple-600/20 border-purple-500/50 text-white shadow-md'
                      : 'bg-slate-900/60 border-slate-800/80 text-slate-300 hover:bg-slate-800/60'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                    isSelected ? 'bg-purple-600 text-white' : 'bg-slate-800 text-slate-400'
                  }`}>
                    <Zap className="w-4 h-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-bold truncate">{p.title}</div>
                    <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                      {p.category.toUpperCase()} • {p.reasoning_pattern}
                    </div>
                  </div>
                  <ChevronRight className={`w-4 h-4 shrink-0 mt-1 ${isSelected ? 'text-purple-400' : 'text-slate-600'}`} />
                </button>
              );
            })}
          </div>

          {/* Active Puzzle Playground */}
          <div className="lg:col-span-2">
            {selectedPuzzle ? (
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      {selectedPuzzle.category}
                    </span>
                    <span className="text-xs text-slate-400">Mental Reasoning Problem</span>
                  </div>
                  <h2 className="text-xl font-bold text-white mt-2">{selectedPuzzle.title}</h2>
                  <p className="text-xs text-slate-400 mt-1">{selectedPuzzle.reasoning_pattern}</p>
                </div>

                {/* Question Box */}
                <div className="p-5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-sm leading-relaxed whitespace-pre-wrap font-mono">
                  {selectedPuzzle.statement}
                </div>

                {/* Multiple Choice Options */}
                <div className="space-y-3">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                    Select the Correct Deduction:
                  </h3>
                  {selectedPuzzle.options && selectedPuzzle.options.map((opt, idx) => {
                    const isPicked = selectedOption === opt;
                    return (
                      <button
                        key={idx}
                        onClick={() => {
                          setSelectedOption(opt);
                          setSubmissionResult(null);
                        }}
                        className={`w-full text-left p-4 rounded-xl border text-xs font-medium transition-all cursor-pointer flex items-center gap-3 ${
                          isPicked
                            ? 'bg-purple-600/20 border-purple-500 text-white'
                            : 'bg-slate-950/80 border-slate-800 text-slate-300 hover:bg-slate-800/60'
                        }`}
                      >
                        <div className={`w-5 h-5 rounded-full border flex items-center justify-center text-[10px] font-bold shrink-0 ${
                          isPicked ? 'border-purple-400 bg-purple-500 text-white' : 'border-slate-700 text-slate-500'
                        }`}>
                          {String.fromCharCode(65 + idx)}
                        </div>
                        <span className="flex-1">{opt}</span>
                      </button>
                    );
                  })}
                </div>

                {/* Action button */}
                <div className="flex items-center justify-between pt-4 border-t border-slate-800">
                  <button
                    disabled={!selectedOption || submitting}
                    onClick={handleSubmitAnswer}
                    className="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-md shadow-purple-600/30 flex items-center gap-2 cursor-pointer"
                  >
                    {submitting ? 'Checking logic...' : 'Verify Deduction'}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* Result & Explanation */}
                {submissionResult && (
                  <div className={`p-5 rounded-xl border animate-fade-in ${
                    submissionResult.is_correct
                      ? 'bg-emerald-950/30 border-emerald-500/50 text-emerald-200'
                      : 'bg-rose-950/30 border-rose-500/50 text-rose-200'
                  }`}>
                    <div className="flex items-center gap-2 font-bold text-sm mb-2">
                      {submissionResult.is_correct ? (
                        <>
                          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                          <span>Correct Deduction! Excellent reasoning.</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="w-5 h-5 text-rose-400" />
                          <span>Incorrect deduction. Analyze the invariant below:</span>
                        </>
                      )}
                    </div>
                    <div className="text-xs text-slate-300 leading-relaxed mt-2 bg-slate-950/60 p-4 rounded-lg border border-slate-800">
                      <div className="font-bold text-slate-200 mb-1 flex items-center gap-1.5">
                        <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                        Formal Proof & Logic Breakdown:
                      </div>
                      <p className="whitespace-pre-wrap">{submissionResult.explanation}</p>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800">
                <Brain className="w-10 h-10 text-slate-600 mx-auto mb-3" />
                <p className="text-sm font-bold text-white">Select a puzzle from the list to begin</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
