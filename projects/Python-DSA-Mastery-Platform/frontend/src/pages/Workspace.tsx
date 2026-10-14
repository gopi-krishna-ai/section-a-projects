import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  CheckCircle2, XCircle, Sparkles, BookOpen, Clock,
  ArrowRight, ArrowLeft, Terminal, ShieldAlert, Table, Code2, AlertTriangle
} from 'lucide-react';
import { api } from '../api/client';
import { ProblemDetail, SubmitSolutionResult } from '../types';
import { CodeEditor } from '../components/workspace/CodeEditor';
import { DryRunTable } from '../components/workspace/DryRunTable';
import { SocraticModal } from '../components/workspace/SocraticModal';
import { useAuth } from '../context/AuthContext';

export const Workspace: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { currentUser } = useAuth();

  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [code, setCode] = useState('');
  const [activeTab, setActiveTab] = useState<'problem' | 'dry_run' | 'understanding'>('problem');
  const [loading, setLoading] = useState(true);

  // Execution states
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isRunningSandbox, setIsRunningSandbox] = useState(false);
  const [sandboxOutput, setSandboxOutput] = useState<{ stdout: string; stderr: string; time_ms: number; error?: string } | null>(null);
  const [submitResult, setSubmitResult] = useState<SubmitSolutionResult | null>(null);

  // Socratic Mentor Modal
  const [isMentorOpen, setIsMentorOpen] = useState(false);
  const [hintsUnlocked, setHintsUnlocked] = useState(0);

  useEffect(() => {
    if (id) {
      loadProblem(id);
    }
  }, [id]);

  const loadProblem = async (problemId: string) => {
    try {
      setLoading(true);
      setSubmitResult(null);
      setSandboxOutput(null);
      const res = await api.getProblemDetail(problemId);
      setProblem(res);
      setCode(res.starter_code);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    if (problem && confirm('Reset code to original starter template?')) {
      setCode(problem.starter_code);
      setSubmitResult(null);
      setSandboxOutput(null);
    }
  };

  const handleRunSandbox = async () => {
    setIsRunningSandbox(true);
    setSandboxOutput(null);
    try {
      const res = await api.runCode(code);
      setSandboxOutput({
        stdout: res.stdout,
        stderr: res.stderr,
        time_ms: res.execution_time_ms,
        error: res.error_type
      });
    } catch (err: any) {
      setSandboxOutput({
        stdout: '',
        stderr: err.message || 'Sandbox execution failed',
        time_ms: 0,
        error: 'Execution Error'
      });
    } finally {
      setIsRunningSandbox(false);
    }
  };

  const handleSubmit = async () => {
    if (!problem) return;
    setIsSubmitting(true);
    try {
      const res = await api.submitSolution(problem.id, {
        code,
        hints_used: hintsUnlocked,
        solution_viewed: hintsUnlocked >= 6,
        user_id: currentUser?.id
      });
      setSubmitResult(res);
    } catch (err: any) {
      alert(err.message || 'Submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-400 gap-3">
        <div className="w-8 h-8 border-3 border-sky-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono">Loading problem workspace & execution environment...</p>
      </div>
    );
  }

  if (!problem) {
    return (
      <div className="p-8 text-center text-slate-400">
        <p className="text-sm">Problem not found.</p>
        <button
          onClick={() => navigate('/problems')}
          className="mt-3 px-4 py-2 rounded-lg bg-sky-600 text-white font-bold text-xs"
        >
          Return to Problem Library
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 max-w-7xl mx-auto space-y-4 text-slate-100">
      {/* Top Bar Navigation */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900 border border-slate-800 p-3.5 rounded-2xl shadow-sm">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/problems')}
            className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Back to Problems"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-sm sm:text-base text-white">{problem.title}</h1>
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                  problem.difficulty === 'Easy'
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : problem.difficulty === 'Medium'
                    ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                    : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                }`}
              >
                {problem.difficulty}
              </span>
            </div>
            <div className="text-[11px] text-slate-400 flex items-center gap-2 mt-0.5">
              <span>Time: <strong className="text-sky-300 font-mono">{problem.time_complexity}</strong></span>
              <span>&bull;</span>
              <span>Space: <strong className="text-sky-300 font-mono">{problem.space_complexity}</strong></span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setIsMentorOpen(true)}
            className="px-3.5 py-1.5 rounded-xl bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/40 text-indigo-300 font-bold text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Socratic Mentor ({hintsUnlocked}/6)</span>
          </button>
        </div>
      </div>

      {/* Main Workspace Split Layout: Problem / Dry Run (5 Cols) + Code Editor / Tests (7 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Problem Tabs & Understanding */}
        <div className="lg:col-span-5 space-y-4">
          {/* Tab Navigation */}
          <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setActiveTab('problem')}
              className={`flex-1 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
                activeTab === 'problem' ? 'bg-sky-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Statement</span>
            </button>
            <button
              onClick={() => setActiveTab('dry_run')}
              className={`flex-1 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
                activeTab === 'dry_run' ? 'bg-sky-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Table className="w-3.5 h-3.5" />
              <span>Dry Run</span>
            </button>
            <button
              onClick={() => setActiveTab('understanding')}
              className={`flex-1 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
                activeTab === 'understanding' ? 'bg-sky-600 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              <span>12-Step Method</span>
            </button>
          </div>

          {/* Statement Content */}
          {activeTab === 'problem' && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-4 max-h-[75vh] overflow-y-auto">
              <div className="space-y-2">
                <span className="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Description</span>
                <p className="text-xs sm:text-sm text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">
                  {problem.description}
                </p>
              </div>

              {/* Examples */}
              {problem.examples && problem.examples.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <span className="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Examples</span>
                  <div className="space-y-2.5">
                    {problem.examples.map((ex, i) => (
                      <div key={i} className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
                        <div>
                          <span className="text-slate-500">Input: </span>
                          <span className="text-sky-300">{JSON.stringify(ex.input)}</span>
                        </div>
                        <div>
                          <span className="text-slate-500">Output: </span>
                          <span className="text-amber-300">{JSON.stringify(ex.output)}</span>
                        </div>
                        {ex.explanation && (
                          <div className="text-[11px] text-slate-400 font-sans mt-1">
                            {ex.explanation}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Constraints */}
              {problem.constraints && problem.constraints.length > 0 && (
                <div className="space-y-1.5 pt-2 border-t border-slate-800">
                  <span className="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Constraints</span>
                  <ul className="list-disc pl-4 space-y-0.5 text-xs text-slate-400 font-mono">
                    {problem.constraints.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Dry Run Tab */}
          {activeTab === 'dry_run' && (
            <DryRunTable steps={problem.dry_run_steps} />
          )}

          {/* 12-Step Problem Solving Framework Tab */}
          {activeTab === 'understanding' && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm space-y-3.5 text-xs max-h-[75vh] overflow-y-auto">
              <h3 className="font-bold text-sm text-sky-400">12-Step Algorithmic Process</h3>
              <ol className="list-decimal pl-4 space-y-2 text-slate-300 leading-relaxed">
                <li><strong className="text-white">Understand:</strong> Identify exact inputs, required outputs, and invariants.</li>
                <li><strong className="text-white">Explore Examples:</strong> Manually calculate outputs for normal, empty, and negative bounds.</li>
                <li><strong className="text-white">Brute Force:</strong> Formulate simplest working solution to establish correctness first.</li>
                <li><strong className="text-white">Design Algorithm:</strong> Write clear pseudocode before touching code.</li>
                <li><strong className="text-white">Dry Run:</strong> Step through state variables using the Dry Run table.</li>
                <li><strong className="text-white">Implement:</strong> Translate clean logic into Python in the editor.</li>
                <li><strong className="text-white">Test:</strong> Execute against visible and hidden test suites.</li>
                <li><strong className="text-white">Debug:</strong> Locate root causes via 22 mistake diagnostic categories.</li>
                <li><strong className="text-white">Optimize:</strong> Verify runtime stays within asymptotic constraints.</li>
                <li><strong className="text-white">Explain:</strong> Justify why the invariant preserves correctness.</li>
                <li><strong className="text-white">Transfer:</strong> Apply pattern to related problems in the library.</li>
                <li><strong className="text-white">Reassess:</strong> Review again when scheduled by spaced repetition.</li>
              </ol>
            </div>
          )}
        </div>

        {/* Right Column: Code Editor & Execution Results */}
        <div className="lg:col-span-7 space-y-4">
          <CodeEditor
            code={code}
            onChange={setCode}
            onReset={handleReset}
            onSubmit={handleSubmit}
            onRunSandbox={handleRunSandbox}
            isSubmitting={isSubmitting}
            isRunning={isRunningSandbox}
          />

          {/* Sandbox Output Drawer */}
          {sandboxOutput && (
            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs space-y-2">
              <div className="flex items-center justify-between text-slate-400 border-b border-slate-800 pb-2">
                <div className="flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-amber-400" />
                  <span className="font-bold text-white">Execution Console Output</span>
                </div>
                <span>{sandboxOutput.time_ms} ms</span>
              </div>
              {sandboxOutput.stdout && (
                <div className="p-2.5 rounded-lg bg-slate-900 text-slate-200 whitespace-pre-wrap">
                  {sandboxOutput.stdout}
                </div>
              )}
              {sandboxOutput.stderr && (
                <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-900/50 text-rose-300 whitespace-pre-wrap">
                  {sandboxOutput.stderr}
                </div>
              )}
            </div>
          )}

          {/* Test Case Evaluation Results */}
          {submitResult && (
            <div
              className={`p-5 rounded-2xl border transition-all space-y-4 ${
                submitResult.status === 'Passed'
                  ? 'bg-emerald-950/20 border-emerald-500/40'
                  : 'bg-rose-950/20 border-rose-500/40'
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  {submitResult.status === 'Passed' ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-400 shrink-0" />
                  ) : (
                    <XCircle className="w-6 h-6 text-rose-400 shrink-0" />
                  )}
                  <div>
                    <h4
                      className={`font-black text-sm sm:text-base ${
                        submitResult.status === 'Passed' ? 'text-emerald-300' : 'text-rose-300'
                      }`}
                    >
                      {submitResult.status === 'Passed'
                        ? 'All Test Cases Passed! Perfect Execution'
                        : `${submitResult.status}: Passed ${submitResult.passes_count} / ${submitResult.total_tests} Tests`}
                    </h4>
                    <p className="text-xs text-slate-400">
                      Execution Time: {submitResult.execution_time_ms} ms &bull;{' '}
                      {submitResult.is_independent ? 'Independent unassisted solve' : 'Assisted with hints'}
                    </p>
                  </div>
                </div>

                {submitResult.mastery_update && (
                  <div className="text-right shrink-0">
                    <span className="text-xs font-bold text-sky-400">
                      {submitResult.mastery_update.mastery_score}% Mastery
                    </span>
                    <div className="text-[10px] text-slate-400 capitalize">
                      {submitResult.mastery_update.status.replace('_', ' ')}
                    </div>
                  </div>
                )}
              </div>

              {/* Mistake Intelligence Diagnosis */}
              {submitResult.mistake_diagnosis && (
                <div className="p-4 rounded-xl bg-slate-900/80 border border-rose-500/30 space-y-2 text-xs">
                  <div className="flex items-center gap-2 text-rose-400 font-bold">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Mistake Category: {submitResult.mistake_diagnosis.error_category}</span>
                  </div>
                  <p className="text-slate-300">
                    <strong className="text-slate-400">What went wrong: </strong>
                    {submitResult.mistake_diagnosis.what_went_wrong}
                  </p>
                  <p className="text-slate-300">
                    <strong className="text-slate-400">Root cause: </strong>
                    {submitResult.mistake_diagnosis.why_it_went_wrong}
                  </p>
                  <p className="text-emerald-300">
                    <strong className="text-slate-400">How to avoid: </strong>
                    {submitResult.mistake_diagnosis.how_to_avoid}
                  </p>
                </div>
              )}

              {/* Individual Test Results Grid */}
              <div className="space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                  Test Case Breakdown
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {submitResult.test_results.map((tr) => (
                    <div
                      key={tr.test_index}
                      className={`p-3 rounded-xl border text-xs font-mono space-y-1 ${
                        tr.passed
                          ? 'bg-slate-950/60 border-slate-800 text-slate-300'
                          : 'bg-rose-950/30 border-rose-800/60 text-rose-200'
                      }`}
                    >
                      <div className="flex items-center justify-between font-bold">
                        <span>Test #{tr.test_index} {tr.is_hidden && '(Hidden)'}</span>
                        <span className={tr.passed ? 'text-emerald-400' : 'text-rose-400'}>
                          {tr.passed ? 'PASS' : 'FAIL'}
                        </span>
                      </div>
                      {!tr.is_hidden && (
                        <>
                          <div className="text-[11px] text-slate-400 truncate">In: {tr.input_str}</div>
                          <div className="text-[11px] text-slate-400 truncate">Expected: {tr.expected_output_str}</div>
                          {tr.actual_output_str && (
                            <div className="text-[11px] text-slate-300 truncate">Actual: {tr.actual_output_str}</div>
                          )}
                        </>
                      )}
                      {tr.error && (
                        <div className="text-[10px] text-rose-300 font-bold truncate">{tr.error}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Socratic Mentor Modal */}
      <SocraticModal
        isOpen={isMentorOpen}
        onClose={() => setIsMentorOpen(false)}
        problemId={problem.id}
        problemTitle={problem.title}
        userCode={code}
        currentHintLevel={hintsUnlocked}
        onHintUnlocked={(lvl) => setHintsUnlocked(lvl)}
      />
    </div>
  );
};
