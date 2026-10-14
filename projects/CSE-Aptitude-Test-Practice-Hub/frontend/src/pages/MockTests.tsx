import React, { useState, useEffect } from 'react';
import {
  FileCheck, Clock, Bookmark, AlertCircle, CheckCircle2,
  XCircle, ArrowRight, ArrowLeft, RefreshCw, Award
} from 'lucide-react';
import { api } from '../api/client';

export const MockTests: React.FC = () => {
  const [profiles, setProfiles] = useState<Record<string, any>>({});
  const [selectedProfile, setSelectedProfile] = useState('tcs_nqt');
  const [loading, setLoading] = useState(false);

  // Active Exam State
  const [isExamActive, setIsExamActive] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [examTitle, setExamTitle] = useState('');
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [markedForReview, setMarkedForReview] = useState<Record<string, boolean>>({});
  const [timeRemaining, setTimeRemaining] = useState(0); // in seconds
  const [timeSpentMap, setTimeSpentMap] = useState<Record<string, number>>({});

  // Exam Result State
  const [examResult, setExamResult] = useState<any | null>(null);

  useEffect(() => {
    api.getCompanyProfiles().then(setProfiles);
  }, []);

  // Timer effect
  useEffect(() => {
    if (!isExamActive || timeRemaining <= 0) return;
    const interval = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          handleSubmitExam();
          return 0;
        }
        return prev - 1;
      });
      if (questions[currentIndex]) {
        const qid = questions[currentIndex].id;
        setTimeSpentMap((prev) => ({ ...prev, [qid]: (prev[qid] || 0) + 1 }));
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [isExamActive, timeRemaining, currentIndex, questions]);

  const handleStartExam = async (profileId: string) => {
    setLoading(true);
    try {
      const res = await api.startMockTest({ profile_id: profileId });
      setSessionId(res.session_id);
      setExamTitle(res.title);
      setQuestions(res.questions);
      setTimeRemaining(res.time_limit_seconds);
      setCurrentIndex(0);
      setAnswers({});
      setMarkedForReview({});
      setTimeSpentMap({});
      setExamResult(null);
      setIsExamActive(true);
    } catch (err: any) {
      alert(err.message || 'Failed to start exam');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (ans: string) => {
    const qid = questions[currentIndex].id;
    setAnswers((prev) => ({ ...prev, [qid]: ans }));
  };

  const toggleMarkForReview = () => {
    const qid = questions[currentIndex].id;
    setMarkedForReview((prev) => ({ ...prev, [qid]: !prev[qid] }));
  };

  const handleSubmitExam = async () => {
    if (!sessionId) return;
    const confirmSubmit = window.confirm('Are you sure you want to finalize and submit this assessment?');
    if (!confirmSubmit && timeRemaining > 0) return;

    setLoading(true);
    try {
      const payloadAnswers = questions.map((q) => ({
        question_id: q.id,
        submitted_answer: answers[q.id] || '',
        time_spent: timeSpentMap[q.id] || 0,
        is_marked_for_review: !!markedForReview[q.id]
      }));

      const res = await api.submitMockTest(sessionId, payloadAnswers);
      setExamResult(res);
      setIsExamActive(false);
    } catch (err: any) {
      alert(err.message || 'Failed to submit exam');
    } finally {
      setLoading(false);
    }
  };

  const currentQ = questions[currentIndex];

  // If viewing post-exam result
  if (examResult) {
    return (
      <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-5xl mx-auto">
        {/* Scorecard Banner */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
            <div>
              <div className="text-xs font-bold text-blue-600 uppercase tracking-wider">Assessment Report</div>
              <h2 className="text-2xl font-extrabold text-slate-900">{examTitle}</h2>
            </div>
            <button
              onClick={() => setExamResult(null)}
              className="px-4 py-2 bg-slate-900 text-white rounded-xl text-xs font-bold hover:bg-slate-800 transition-colors cursor-pointer self-start sm:self-auto"
            >
              Take Another Test
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-xs font-bold text-slate-500 uppercase">Score</div>
              <div className="text-2xl font-black text-slate-900">
                {examResult.score} <span className="text-xs text-slate-400 font-normal">/ {examResult.total_questions}</span>
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-xs font-bold text-slate-500 uppercase">Accuracy</div>
              <div className="text-2xl font-black text-blue-600">{examResult.accuracy}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-xs font-bold text-slate-500 uppercase">Status</div>
              <div className={`text-base font-bold mt-1 ${
                examResult.accuracy >= 70 ? 'text-emerald-600' : 'text-amber-600'
              }`}>
                {examResult.accuracy >= 70 ? 'Placement Cleared' : 'Needs Practice'}
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
              <div className="text-xs font-bold text-slate-500 uppercase">Speed</div>
              <div className="text-xs font-medium text-slate-700 mt-2">
                Under time limit
              </div>
            </div>
          </div>

          {/* Category Breakdown */}
          {examResult.category_breakdown && (
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Sectional Performance</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {Object.entries(examResult.category_breakdown).map(([cat, val]: [string, any]) => (
                  <div key={cat} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50">
                    <div className="text-xs font-bold text-slate-800 truncate">{cat}</div>
                    <div className="flex items-center justify-between mt-2 text-xs">
                      <span className="text-slate-500">Correct:</span>
                      <span className="font-bold text-slate-900">{val.correct} / {val.total}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Question Review List */}
          <div className="space-y-4 pt-4 border-t border-slate-200">
            <h4 className="text-sm font-bold text-slate-900">Comprehensive Solutions & Error Analysis</h4>
            <div className="space-y-3">
              {examResult.question_results.map((qr: any, idx: number) => (
                <div
                  key={idx}
                  className={`p-4 rounded-xl border text-xs space-y-2 ${
                    qr.is_correct ? 'border-emerald-200 bg-emerald-50/50' : 'border-rose-200 bg-rose-50/50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-800">Q{idx + 1}: {qr.category}</span>
                    <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
                      qr.is_correct ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                    }`}>
                      {qr.is_correct ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>
                  <p className="font-semibold text-slate-900">{qr.question_text}</p>
                  <div className="flex items-center gap-4 font-mono">
                    <span className="text-slate-700">Submitted: <strong>{qr.submitted_answer || '(None)'}</strong></span>
                    <span className="text-emerald-700">Correct: <strong>{qr.correct_answer}</strong></span>
                  </div>
                  <div className="p-3 bg-white rounded-lg border border-slate-200 font-mono whitespace-pre-line text-slate-700">
                    {qr.reference_solution}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Active Exam Test Room
  if (isExamActive && currentQ) {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const isMarked = !!markedForReview[currentQ.id];
    const currentAnswer = answers[currentQ.id] || '';

    return (
      <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
        {/* Exam Header */}
        <div className="bg-slate-900 text-white p-4 rounded-2xl flex items-center justify-between shadow-md">
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded-md bg-blue-600 text-xs font-bold uppercase">
              {examTitle}
            </span>
            <span className="text-xs text-slate-300 hidden sm:inline">
              Section: {currentQ.category}
            </span>
          </div>

          <div className="flex items-center gap-4">
            <div className={`px-3 py-1 rounded-lg font-mono text-xs sm:text-sm font-bold flex items-center gap-1.5 ${
              timeRemaining < 300 ? 'bg-rose-600 text-white animate-pulse' : 'bg-slate-800 text-amber-400'
            }`}>
              <Clock className="w-4 h-4" />
              <span>{minutes}:{seconds.toString().padStart(2, '0')}</span>
            </div>

            <button
              onClick={handleSubmitExam}
              className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold transition-colors cursor-pointer"
            >
              Submit Exam
            </button>
          </div>
        </div>

        {/* 2-Column: Question View (8) & Question Palette (4) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div className="lg:col-span-8 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-5">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <span className="text-xs font-bold text-slate-700">
                Question {currentIndex + 1} of {questions.length}
              </span>
              <button
                type="button"
                onClick={toggleMarkForReview}
                className={`px-3 py-1 rounded-lg text-xs font-semibold border flex items-center gap-1.5 transition-colors cursor-pointer ${
                  isMarked
                    ? 'bg-amber-50 border-amber-300 text-amber-700 font-bold'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Bookmark className="w-3.5 h-3.5" />
                <span>{isMarked ? 'Marked for Review' : 'Mark for Review'}</span>
              </button>
            </div>

            {/* Stimulus Context if table/passage */}
            {currentQ.stimulus_context && (
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs font-mono whitespace-pre-wrap">
                {currentQ.stimulus_context}
              </div>
            )}

            <p className="text-sm sm:text-base font-semibold text-slate-900 leading-relaxed">
              {currentQ.question_text}
            </p>

            {/* Answer Selection */}
            {currentQ.options && currentQ.options.length > 0 ? (
              <div className="space-y-2 pt-2">
                {currentQ.options.map((opt: string, i: number) => {
                  const isChecked = currentAnswer === opt || currentAnswer === opt.slice(0, 1);
                  return (
                    <label
                      key={i}
                      className={`p-3.5 rounded-xl border text-xs sm:text-sm font-medium flex items-center gap-3 cursor-pointer transition-colors ${
                        isChecked
                          ? 'border-blue-600 bg-blue-50/70 text-blue-950 font-bold'
                          : 'border-slate-200 bg-white hover:border-slate-300 text-slate-800'
                      }`}
                    >
                      <input
                        type="radio"
                        name="exam_option"
                        value={opt}
                        checked={isChecked}
                        onChange={() => handleSelectAnswer(opt)}
                        className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                      />
                      <span>{opt}</span>
                    </label>
                  );
                })}
              </div>
            ) : (
              <div className="space-y-1.5 pt-2">
                <label className="text-xs font-bold text-slate-700">Enter your numeric or text answer:</label>
                <input
                  type="text"
                  value={currentAnswer}
                  onChange={(e) => handleSelectAnswer(e.target.value)}
                  placeholder="Type answer here..."
                  className="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm font-mono text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}

            {/* Navigation buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-100">
              <button
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex((prev) => prev - 1)}
                className="px-4 py-2 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40 flex items-center gap-1.5 cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Previous</span>
              </button>

              <button
                disabled={currentIndex >= questions.length - 1}
                onClick={() => setCurrentIndex((prev) => prev + 1)}
                className="px-4 py-2 rounded-lg bg-blue-600 text-white text-xs font-bold hover:bg-blue-700 disabled:opacity-40 flex items-center gap-1.5 cursor-pointer"
              >
                <span>Save & Next</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Right Palette */}
          <div className="lg:col-span-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Question Palette</h4>
            <div className="grid grid-cols-5 gap-2">
              {questions.map((q, idx) => {
                const isAnswered = !!answers[q.id];
                const isMarkedQ = !!markedForReview[q.id];
                const isCurrent = idx === currentIndex;

                return (
                  <button
                    key={q.id}
                    onClick={() => setCurrentIndex(idx)}
                    className={`h-9 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                      isCurrent
                        ? 'ring-2 ring-blue-600 font-black'
                        : ''
                    } ${
                      isMarkedQ
                        ? 'bg-amber-400 text-slate-950'
                        : isAnswered
                        ? 'bg-emerald-600 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>

            <div className="pt-3 border-t border-slate-100 space-y-2 text-[11px] text-slate-600 font-medium">
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded bg-emerald-600" />
                <span>Answered</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded bg-amber-400" />
                <span>Marked for Review</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded bg-slate-100 border border-slate-300" />
                <span>Not Attempted</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Exam Selection Lobby
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Placement Exam Simulator</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Simulate full-length placement assessment conditions under strict timers with automated post-test analysis.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.entries(profiles).map(([key, prof]: [string, any]) => (
          <div
            key={key}
            className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-4 flex flex-col justify-between hover:border-blue-400 transition-all"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="font-extrabold text-base text-slate-900">{prof.name}</h3>
              <p className="text-xs text-slate-600 leading-relaxed font-medium">{prof.description}</p>

              <div className="space-y-1.5 pt-2 border-t border-slate-100 text-xs text-slate-700 font-medium">
                <div className="flex justify-between">
                  <span className="text-slate-500">Total Questions:</span>
                  <span className="font-bold text-slate-900">{prof.question_count} Qs</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Time Limit:</span>
                  <span className="font-bold text-slate-900">{prof.time_limit_minutes} Minutes</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Difficulty:</span>
                  <span className="font-bold text-slate-900">Mixed Placement Level</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => handleStartExam(key)}
              disabled={loading}
              className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm shadow-sm transition-colors cursor-pointer flex items-center justify-center gap-2"
            >
              <span>Start Assessment</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
