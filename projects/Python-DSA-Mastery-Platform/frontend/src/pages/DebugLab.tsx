import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { DebugExercise } from '../types';
import { 
  Bug, 
  Play, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Sparkles, 
  ChevronRight, 
  FileCode2, 
  RotateCcw,
  Terminal,
  Lightbulb
} from 'lucide-react';

export const DebugLab: React.FC = () => {
  const [exercises, setExercises] = useState<DebugExercise[]>([]);
  const [selectedExercise, setSelectedExercise] = useState<DebugExercise | null>(null);
  const [code, setCode] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{
    is_fixed: boolean;
    stdout: string;
    error?: string;
    explanation: string;
  } | null>(null);

  useEffect(() => {
    async function loadLab() {
      try {
        setLoading(true);
        const data = await api.getDebugExercises();
        setExercises(data);
        if (data.length > 0) {
          setSelectedExercise(data[0]);
          setCode(data[0].buggy_code);
        }
      } catch (err) {
        console.error('Failed to load debug exercises', err);
      } finally {
        setLoading(false);
      }
    }
    loadLab();
  }, []);

  const handleSelect = (ex: DebugExercise) => {
    setSelectedExercise(ex);
    setCode(ex.buggy_code);
    setResult(null);
  };

  const handleReset = () => {
    if (selectedExercise) {
      setCode(selectedExercise.buggy_code);
      setResult(null);
    }
  };

  const handleRunVerify = async () => {
    if (!selectedExercise) return;
    try {
      setRunning(true);
      const res = await api.submitDebugSolution(selectedExercise.id, code);
      setResult(res);
    } catch (err) {
      console.error('Debug verify failed', err);
    } finally {
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-rose-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-rose-950 to-slate-900 border border-rose-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/20 text-rose-300 text-xs font-bold mb-3 border border-rose-500/30">
            <Bug className="w-3.5 h-3.5" />
            <span>Interactive Bug Hunting & Root-Cause Analysis</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            The Debugging Laboratory
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Real programmers spend 70% of their time finding and fixing bugs. Trace the execution of real, broken Python and DSA code, find the silent failure, and fix the root cause.
          </p>
        </div>

        <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 flex items-center gap-4 shrink-0">
          <div className="w-10 h-10 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center">
            <Terminal className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Total Lab Scenarios</div>
            <div className="text-xl font-black text-white">{exercises.length} Exercises</div>
          </div>
        </div>
      </div>

      {/* Main Grid: Left exercise selector, Right interactive debugger */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Exercises List */}
        <div className="lg:col-span-1 space-y-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 px-1 mb-2">
            Bug Scenarios
          </h2>
          {exercises.map((ex) => {
            const isSelected = selectedExercise?.id === ex.id;
            return (
              <button
                key={ex.id}
                onClick={() => handleSelect(ex)}
                className={`w-full text-left p-4 rounded-xl border transition-all cursor-pointer flex items-start gap-3 ${
                  isSelected
                    ? 'bg-rose-950/40 border-rose-500/50 text-white shadow-md'
                    : 'bg-slate-900/60 border-slate-800/80 text-slate-300 hover:bg-slate-800/60'
                }`}
              >
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 text-xs font-bold ${
                  isSelected ? 'bg-rose-600 text-white' : 'bg-slate-800 text-slate-400'
                }`}>
                  <Bug className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-xs font-bold truncate">{ex.title}</div>
                  <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                    {ex.bug_category} • {ex.description}
                  </div>
                </div>
                <ChevronRight className={`w-4 h-4 shrink-0 mt-1 ${isSelected ? 'text-rose-400' : 'text-slate-600'}`} />
              </button>
            );
          })}
        </div>

        {/* Code Editor & Execution Panel */}
        <div className="lg:col-span-2 space-y-4">
          {selectedExercise && (
            <div className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
              {/* Scenario details */}
              <div className="p-5 border-b border-slate-800 bg-slate-950/50">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-500/20 text-rose-300 border border-rose-500/30">
                        {selectedExercise.bug_category}
                      </span>
                      <span className="text-xs text-slate-400 font-semibold">Debug Scenario</span>
                    </div>
                    <h3 className="text-lg font-bold text-white mt-1">{selectedExercise.title}</h3>
                    <p className="text-xs text-slate-300 mt-1">{selectedExercise.description}</p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleReset}
                      className="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      Reset Bug
                    </button>
                    <button
                      disabled={running}
                      onClick={handleRunVerify}
                      className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-md shadow-rose-600/30 flex items-center gap-1.5 cursor-pointer"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      {running ? 'Executing...' : 'Run & Verify Fix'}
                    </button>
                  </div>
                </div>

                {/* Bug Symptom Callout */}
                <div className="mt-3.5 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-200 text-xs flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400" />
                  <span>
                    <strong>Observed Symptom:</strong> The current code fails tests or produces unexpected side effects. Trace state step-by-step and fix the root issue.
                  </span>
                </div>
              </div>

              {/* Editable Code Box */}
              <div className="p-4 bg-slate-950">
                <div className="flex items-center justify-between text-xs text-slate-400 mb-2 px-1">
                  <span className="font-mono">solution.py (Editable)</span>
                  <span>Python 3.12 Isolated Runtime</span>
                </div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={14}
                  className="w-full font-mono text-xs text-emerald-300 bg-slate-900 border border-slate-800 rounded-xl p-4 focus:outline-none focus:border-rose-500 leading-relaxed resize-y selection:bg-rose-900/50"
                  spellCheck={false}
                />
              </div>

              {/* Execution Feedback */}
              {result && (
                <div className={`p-5 border-t ${
                  result.is_fixed
                    ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-200'
                    : 'bg-rose-950/20 border-rose-500/40 text-rose-200'
                }`}>
                  <div className="flex items-center gap-2 font-bold text-sm mb-2">
                    {result.is_fixed ? (
                      <>
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                        <span>Bug Resolved! All assertions and edge cases passed.</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-5 h-5 text-rose-400" />
                        <span>Tests still failing or exception raised:</span>
                      </>
                    )}
                  </div>

                  {result.stdout && (
                    <div className="mt-3">
                      <div className="text-[11px] font-bold text-slate-400 mb-1">Standard Output:</div>
                      <pre className="p-3 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs text-slate-200 overflow-x-auto">
                        {result.stdout}
                      </pre>
                    </div>
                  )}

                  {result.error && (
                    <div className="mt-3">
                      <div className="text-[11px] font-bold text-rose-400 mb-1">Execution Error:</div>
                      <pre className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/60 font-mono text-xs text-rose-300 overflow-x-auto">
                        {result.error}
                      </pre>
                    </div>
                  )}

                  {result.is_fixed && result.explanation && (
                    <div className="mt-3 p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300">
                      <div className="font-bold text-white mb-1 flex items-center gap-1.5">
                        <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                        Root Cause Breakdown:
                      </div>
                      <p className="leading-relaxed">{result.explanation}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
