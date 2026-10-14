import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Library, Search, Filter, ArrowRight, Bookmark, CheckCircle2 } from 'lucide-react';
import { api } from '../api/client';
import { Question } from '../types';

export const QuestionLibrary: React.FC = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [level, setLevel] = useState('All');
  const [type, setType] = useState('All');
  const [page, setPage] = useState(0);
  const PAGE_SIZE = 25;

  useEffect(() => {
    loadQuestions();
  }, [category, level, type, page]);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const res = await api.getQuestions({
        category: category !== 'All' ? category : undefined,
        level: level !== 'All' ? level : undefined,
        question_type: type !== 'All' ? type : undefined,
        search: search || undefined,
        skip: page * PAGE_SIZE,
        limit: PAGE_SIZE
      });
      setQuestions(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(0);
    loadQuestions();
  };

  const CATEGORIES = [
    'All',
    'Quantitative Aptitude',
    'Logical Reasoning',
    'Verbal Ability',
    'Data Interpretation and Analysis',
    'Abstract Reasoning',
    'Technical Aptitude'
  ];

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Question Library (1,800 Bank)</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Full index of original verified practice problems from the CSE Aptitude Test Practice Hub.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by keywords (e.g. profit, series, python, speed)..."
              className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            <select
              value={category}
              onChange={(e) => { setCategory(e.target.value); setPage(0); }}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              {CATEGORIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>

            <select
              value={level}
              onChange={(e) => { setLevel(e.target.value); setPage(0); }}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              <option value="All">All Levels</option>
              <option value="Basic">Basic</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>

            <select
              value={type}
              onChange={(e) => { setType(e.target.value); setPage(0); }}
              className="px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-700"
            >
              <option value="All">All Types</option>
              <option value="numeric">Numeric</option>
              <option value="mcq">Multiple Choice</option>
              <option value="text_correction">Sentence Correction</option>
              <option value="short_answer">Short Answer</option>
            </select>

            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold transition-colors cursor-pointer"
            >
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Questions List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center text-slate-400 gap-2">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs">Loading question catalog...</p>
        </div>
      ) : questions.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
          <p className="text-sm text-slate-500">No questions matched your search query.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {questions.map((q, idx) => (
            <div
              key={q.id}
              className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs hover:border-slate-300 transition-colors flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded">
                    {q.category}
                  </span>
                  <span className="text-[11px] font-semibold text-slate-600">
                    {q.subtopic_name}
                  </span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    q.level === 'Basic' ? 'bg-emerald-100 text-emerald-800' :
                    q.level === 'Intermediate' ? 'bg-amber-100 text-amber-800' :
                    'bg-rose-100 text-rose-800'
                  }`}>
                    {q.level}
                  </span>
                  <span className="text-[10px] text-slate-400 font-mono">
                    ID: {q.source_id}
                  </span>
                </div>
                <p className="text-xs sm:text-sm font-semibold text-slate-900 line-clamp-2">
                  {q.question_text}
                </p>
              </div>

              <button
                onClick={() => navigate(`/workspace?qid=${q.id}`)}
                className="px-3.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer shrink-0"
              >
                <span>Solve Question</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}

          {/* Pagination */}
          <div className="flex items-center justify-between pt-4">
            <button
              disabled={page === 0}
              onClick={() => setPage((prev) => Math.max(0, prev - 1))}
              className="px-3.5 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 disabled:opacity-40"
            >
              Previous Page
            </button>
            <span className="text-xs text-slate-500 font-medium">Page {page + 1}</span>
            <button
              disabled={questions.length < PAGE_SIZE}
              onClick={() => setPage((prev) => prev + 1)}
              className="px-3.5 py-1.5 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 disabled:opacity-40"
            >
              Next Page
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
