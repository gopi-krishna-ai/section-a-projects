import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  PenTool, CheckCircle2, XCircle, HelpCircle, Sparkles, Book,
  Bookmark, ArrowRight, ArrowLeft, RotateCcw, AlertTriangle, ShieldCheck
} from 'lucide-react';
import { api } from '../api/client';
import { Question, SubmitAnswerResult, ProgressiveHint } from '../types';
import { Scratchpad } from '../components/workspace/Scratchpad';
import { FormulaModal } from '../components/workspace/FormulaModal';
import { StepTutorModal } from '../components/workspace/StepTutorModal';

export const Workspace: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  // Solving State
  const [submittedAnswer, setSubmittedAnswer] = useState('');
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [scratchpadText, setScratchpadText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<SubmitAnswerResult | null>(null);
  const [timeSpent, setTimeSpent] = useState(0);

  // Hints & Modals
  const [hintsUsed, setHintsUsed] = useState(0);
  const [currentHint, setCurrentHint] = useState<ProgressiveHint | null>(null);
  const [hintLoading, setHintLoading] = useState(false);
  const [showFormulaModal, setShowFormulaModal] = useState(false);
  const [showStepTutorModal, setShowStepTutorModal] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);

  // Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeSpent((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [currentIndex]);

  useEffect(() => {
    loadQuestions();
  }, [searchParams]);

  const loadQuestions = async () => {
    setLoading(true);
    setResult(null);
    setSubmittedAnswer('');
    setSelectedOption(null);
    setTimeSpent(0);
    setHintsUsed(0);
    setCurrentHint(null);

    const topicId = searchParams.get('topic');
    const qId = searchParams.get('qid');
    const level = searchParams.get('level');

    try {
      if (qId) {
        const singleQ = await api.getQuestionDetail(qId);
        setQuestions([singleQ]);
        setCurrentIndex(0);
        setIsBookmarked(!!singleQ.is_bookmarked);
      } else {
        const res = await api.getQuestions({
          topic_id: topicId || undefined,
          level: level || undefined,
          limit: 20
        });
        setQuestions(res);
        setCurrentIndex(0);
        if (res.length > 0) {
          setIsBookmarked(!!res[0].is_bookmarked);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const currentQ = questions[currentIndex];

  const handleNextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setResult(null);
      setSubmittedAnswer('');
      setSelectedOption(null);
      setTimeSpent(0);
      setHintsUsed(0);
      setCurrentHint(null);
      setIsBookmarked(!!questions[currentIndex + 1]?.is_bookmarked);
    }
  };

  const handlePrevQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
      setResult(null);
      setSubmittedAnswer('');
      setSelectedOption(null);
      setTimeSpent(0);
      setHintsUsed(0);
      setCurrentHint(null);
      setIsBookmarked(!!questions[currentIndex - 1]?.is_bookmarked);
    }
  };

  const handleFetchNextHint = async () => {
    if (!currentQ) return;
    const nextLevel = Math.min(hintsUsed + 1, 4);
    setHintLoading(true);
    try {
      const hint = await api.getHint(currentQ.id, nextLevel, submittedAnswer);
      setCurrentHint(hint);
      setHintsUsed(nextLevel);
    } catch (err) {
      console.error(err);
    } finally {
      setHintLoading(false);
    }
  };

  const handleToggleBookmark = async () => {
    if (!currentQ) return;
    try {
      const res = await api.toggleBookmark(currentQ.id);
      setIsBookmarked(res.is_bookmarked);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQ) return;

    const answerToSubmit = selectedOption || submittedAnswer;
    if (!answerToSubmit.trim()) return;

    setIsSubmitting(true);
    try {
      const res = await api.submitAnswer(currentQ.id, {
        submitted_answer: answerToSubmit,
        time_spent: timeSpent,
        hints_used: hintsUsed,
        scratchpad_notes: scratchpadText || null
      });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-500 gap-3">
        <div className="w-8 h-8 border-3 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-medium">Preparing question workspace...</p>
      </div>
    );
  }

  if (!currentQ) {
    return (
      <div className="p-8 max-w-lg mx-auto text-center space-y-4">
        <p className="text-slate-600 text-sm">No questions available for this selection.</p>
        <button
          onClick={() => navigate('/practice')}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold"
        >
          Return to Practice Modes
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Top Bar: Navigation & Tools */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold px-2.5 py-1 rounded-md bg-blue-100 text-blue-800">
            Question {currentIndex + 1} of {questions.length}
          </span>
          <span className="text-xs font-semibold text-slate-600">
            {currentQ.category} &bull; <span className="text-slate-900">{currentQ.subtopic_name}</span>
          </span>
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
            currentQ.level === 'Basic' ? 'bg-emerald-100 text-emerald-800' :
            currentQ.level === 'Intermediate' ? 'bg-amber-100 text-amber-800' :
            'bg-rose-100 text-rose-800'
          }`}>
            {currentQ.level}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Timer display */}
          <div className="text-xs font-mono font-semibold text-slate-500 px-2.5 py-1 bg-slate-100 rounded-lg">
            ⏱ {Math.floor(timeSpent / 60)}:{(timeSpent % 60).toString().padStart(2, '0')}
          </div>

          <button
            type="button"
            onClick={handleToggleBookmark}
            className={`p-2 rounded-lg border transition-colors cursor-pointer ${
              isBookmarked
                ? 'bg-amber-50 border-amber-300 text-amber-600'
                : 'border-slate-200 text-slate-500 hover:bg-slate-50'
            }`}
            title="Bookmark Question"
          >
            <Bookmark className="w-4 h-4" />
          </button>

          <button
            type="button"
            onClick={() => setShowFormulaModal(true)}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 cursor-pointer"
          >
            <Book className="w-3.5 h-3.5 text-blue-600" />
            <span className="hidden sm:inline">Formulas</span>
          </button>

          <button
            type="button"
            onClick={() => setShowStepTutorModal(true)}
            className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-50 border border-indigo-200 text-indigo-700 hover:bg-indigo-100 flex items-center gap-1.5 cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>AI Step Coach</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Problem Workspace (8 Cols) + Scratchpad & Hints (4 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Problem & Solving Form */}
        <div className="lg:col-span-8 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-5">
            {/* Shared Stimulus Context (Tables, Passages, Charts) */}
            {currentQ.stimulus_context && (
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs sm:text-sm text-slate-800 overflow-x-auto whitespace-pre-wrap font-mono leading-relaxed">
                {currentQ.stimulus_context}
              </div>
            )}

            {/* Question Text */}
            <div className="space-y-2">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">Problem Statement</div>
              <p className="text-base sm:text-lg font-semibold text-slate-900 leading-relaxed">
                {currentQ.question_text}
              </p>
            </div>

            {/* Form submission */}
            <form onSubmit={handleSubmit} className="space-y-4 pt-2">
              {/* If MCQ: Render Options */}
              {currentQ.options && currentQ.options.length > 0 ? (
                <div className="space-y-2.5">
                  <div className="text-xs font-bold text-slate-600">Select the correct option:</div>
                  <div className="grid grid-cols-1 gap-2.5">
                    {currentQ.options.map((opt, idx) => {
                      const isSelected = selectedOption === opt || selectedOption === opt.slice(0, 1);
                      return (
                        <label
                          key={idx}
                          className={`p-3.5 rounded-xl border text-xs sm:text-sm font-medium flex items-center gap-3 cursor-pointer transition-all ${
                            isSelected
                              ? 'border-blue-600 bg-blue-50/70 text-blue-950 font-bold shadow-xs'
                              : 'border-slate-200 hover:border-slate-300 bg-white text-slate-800'
                          }`}
                        >
                          <input
                            type="radio"
                            name="mcq_option"
                            value={opt}
                            checked={isSelected}
                            onChange={() => {
                              setSelectedOption(opt);
                              setSubmittedAnswer(opt);
                            }}
                            className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                          />
                          <span>{opt}</span>
                        </label>
                      );
                    })}
                  </div>
                </div>
              ) : (
                /* Numeric or Text Input */
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-700">
                    Your Calculated Answer:
                  </label>
                  <input
                    type="text"
                    value={submittedAnswer}
                    onChange={(e) => setSubmittedAnswer(e.target.value)}
                    placeholder="Enter numerical value or text (e.g. 100, 187.5, 9:10)..."
                    className="w-full px-4 py-3 rounded-xl border border-slate-300 text-sm font-mono text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleFetchNextHint}
                  disabled={hintLoading || hintsUsed >= 4}
                  className="px-3.5 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 transition-colors disabled:opacity-40 cursor-pointer"
                >
                  <HelpCircle className="w-3.5 h-3.5 text-amber-500" />
                  <span>
                    {hintsUsed === 0 ? 'Request Hint 1' :
                     hintsUsed === 1 ? 'Need Hint 2 (Formula)' :
                     hintsUsed === 2 ? 'Need Hint 3 (Step 1)' :
                     'Show Full Solution'}
                  </span>
                </button>

                <div className="flex items-center gap-2">
                  <button
                    type="submit"
                    disabled={isSubmitting || (!submittedAnswer.trim() && !selectedOption)}
                    className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 font-bold text-xs sm:text-sm text-white shadow-sm transition-all disabled:opacity-40 cursor-pointer flex items-center gap-2"
                  >
                    {isSubmitting ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        <span>Verifying...</span>
                      </>
                    ) : (
                      <>
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Check Answer</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </form>

            {/* Answer Evaluation Result Card */}
            {result && (
              <div className={`p-5 rounded-2xl border transition-all space-y-4 ${
                result.is_correct
                  ? 'bg-emerald-50/80 border-emerald-200'
                  : 'bg-rose-50/80 border-rose-200'
              }`}>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    {result.is_correct ? (
                      <CheckCircle2 className="w-6 h-6 text-emerald-600 shrink-0" />
                    ) : (
                      <XCircle className="w-6 h-6 text-rose-600 shrink-0" />
                    )}
                    <div>
                      <h4 className={`font-bold text-sm sm:text-base ${
                        result.is_correct ? 'text-emerald-900' : 'text-rose-900'
                      }`}>
                        {result.is_correct ? 'Accurate! Solved Successfully' : 'Not Quite Correct'}
                      </h4>
                      <p className="text-xs text-slate-600 font-medium">{result.feedback}</p>
                    </div>
                  </div>

                  {result.mastery_update && (
                    <div className="text-right shrink-0">
                      <div className="text-xs font-bold text-slate-800">
                        {result.mastery_update.mastery_score}% Topic Mastery
                      </div>
                      <div className="text-[10px] text-slate-500 capitalize">
                        Status: {result.mastery_update.status.replace('_', ' ')}
                      </div>
                    </div>
                  )}
                </div>

                {/* Mistake Diagnosis if Incorrect */}
                {!result.is_correct && result.error_diagnosis && (
                  <div className="p-4 rounded-xl bg-white border border-rose-200 space-y-2.5">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 text-[10px] font-bold uppercase tracking-wider">
                        Diagnosis: {result.error_diagnosis.error_category}
                      </span>
                    </div>
                    <div className="text-xs text-slate-800 leading-relaxed">
                      <span className="font-bold">What went wrong:</span> {result.error_diagnosis.what_went_wrong}
                    </div>
                    <div className="text-xs text-slate-800 leading-relaxed">
                      <span className="font-bold">Why it happened:</span> {result.error_diagnosis.why_it_went_wrong}
                    </div>
                    <div className="text-xs text-slate-800 leading-relaxed">
                      <span className="font-bold">How to avoid next time:</span> {result.error_diagnosis.how_to_avoid}
                    </div>
                    {result.error_diagnosis.corrective_exercise && (
                      <div className="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-950 font-medium">
                        <span className="font-bold">Corrective Check:</span> {result.error_diagnosis.corrective_exercise.prompt}
                      </div>
                    )}
                  </div>
                )}

                {/* Verified Reference Solution */}
                <div className="p-4 rounded-xl bg-white border border-slate-200 space-y-2">
                  <div className="text-xs font-bold text-slate-900 flex items-center justify-between">
                    <span>Verified Step-by-Step Solution</span>
                    <span className="font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-xs font-bold">
                      Answer: {result.correct_answer}
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-mono whitespace-pre-line">
                    {result.reference_solution}
                  </p>
                </div>

                {/* Next Question Shortcut */}
                <div className="flex justify-end pt-1">
                  <button
                    onClick={handleNextQuestion}
                    className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs flex items-center gap-2 transition-colors cursor-pointer"
                  >
                    <span>Proceed to Next Question</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Bottom Pagination */}
          <div className="flex items-center justify-between pt-2">
            <button
              onClick={handlePrevQuestion}
              disabled={currentIndex === 0}
              className="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 flex items-center gap-1.5 cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Previous Question</span>
            </button>
            <button
              onClick={handleNextQuestion}
              disabled={currentIndex >= questions.length - 1}
              className="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-40 flex items-center gap-1.5 cursor-pointer"
            >
              <span>Next Question</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Right: Calculation Scratchpad & Progressive Hints */}
        <div className="lg:col-span-4 space-y-6">
          <Scratchpad value={scratchpadText} onChange={setScratchpadText} />

          {/* Progressive Hint Box */}
          {currentHint && (
            <div className="bg-white rounded-xl border border-amber-200 p-4 space-y-2 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-900 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                  {currentHint.title}
                </span>
                <span className="text-[10px] font-bold text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">
                  Level {currentHint.hint_level} / 4
                </span>
              </div>
              <p className="text-xs text-amber-950 font-medium leading-relaxed whitespace-pre-line">
                {currentHint.content}
              </p>
              {currentHint.educational_takeaway && (
                <div className="text-[11px] text-amber-800 pt-1 border-t border-amber-100 font-semibold">
                  Takeaway: {currentHint.educational_takeaway}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Formula & Step Tutor Modals */}
      <FormulaModal
        isOpen={showFormulaModal}
        onClose={() => setShowFormulaModal(false)}
        category={currentQ.category}
        topicName={currentQ.subtopic_name}
      />

      <StepTutorModal
        isOpen={showStepTutorModal}
        onClose={() => setShowStepTutorModal(false)}
        questionId={currentQ.id}
        questionText={currentQ.question_text}
      />
    </div>
  );
};
