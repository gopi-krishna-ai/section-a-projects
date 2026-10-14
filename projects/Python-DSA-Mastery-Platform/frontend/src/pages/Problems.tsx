import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { ProblemSummary, Topic } from '../types';
import { 
  Code2, 
  Search, 
  Filter, 
  CheckCircle2, 
  Clock, 
  ArrowRight, 
  Zap, 
  Check, 
  Tag, 
  Sparkles 
} from 'lucide-react';

export const Problems: React.FC = () => {
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedTrack, setSelectedTrack] = useState<string>('all');
  const [selectedTopic, setSelectedTopic] = useState<string>('all');

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [probList, topicList] = await Promise.all([
          api.getProblems(),
          api.getTopics()
        ]);
        setProblems(probList);
        setTopics(topicList);
      } catch (err) {
        console.error('Failed to load problems', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredProblems = problems.filter((p) => {
    if (search && !p.title.toLowerCase().includes(search.toLowerCase()) && !p.slug.includes(search.toLowerCase())) {
      return false;
    }
    if (selectedDifficulty !== 'all' && p.difficulty.toLowerCase() !== selectedDifficulty.toLowerCase()) {
      return false;
    }
    if (selectedTrack !== 'all' && p.track !== selectedTrack) {
      return false;
    }
    if (selectedTopic !== 'all' && p.topic_id !== selectedTopic) {
      return false;
    }
    return true;
  });

  const solvedCount = problems.filter(p => p.is_solved).length;

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 border border-sky-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 text-xs font-bold mb-3 border border-sky-500/30">
            <Code2 className="w-3.5 h-3.5" />
            <span>Problem Library & Algorithmic Challenges</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Independent Coding Problem Library
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Practice essential coding interview problems with real automated unit testing, Socratic guidance, dry-run tracking, and root-cause mistake diagnosis.
          </p>
        </div>

        <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800 flex items-center gap-6 shrink-0">
          <div>
            <div className="text-[11px] font-bold text-slate-400 uppercase">Solved</div>
            <div className="text-2xl font-black text-emerald-400">
              {solvedCount} / {problems.length}
            </div>
          </div>
          <div className="w-12 h-12 rounded-full border-4 border-slate-800 border-t-emerald-500 flex items-center justify-center font-bold text-xs text-white">
            {problems.length > 0 ? Math.round((solvedCount / problems.length) * 100) : 0}%
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-slate-900/70 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search problems, patterns..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {/* Track Filter */}
          <select
            value={selectedTrack}
            onChange={(e) => setSelectedTrack(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-sky-500"
          >
            <option value="all">All Tracks</option>
            <option value="python">Python Mastery</option>
            <option value="dsa">DSA Foundations</option>
          </select>

          {/* Difficulty Filter */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-sky-500"
          >
            <option value="all">All Difficulties</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          {/* Topic Filter */}
          <select
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-sky-500 max-w-[200px]"
          >
            <option value="all">All Topics</option>
            {topics.map(t => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Problems Table / List */}
      {loading ? (
        <div className="flex items-center justify-center min-h-[300px]">
          <div className="w-8 h-8 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : filteredProblems.length === 0 ? (
        <div className="p-12 text-center bg-slate-900/50 rounded-2xl border border-slate-800">
          <Code2 className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white">No problems found</h3>
          <p className="text-xs text-slate-400 mt-1">Try adjusting your filters or search keywords.</p>
        </div>
      ) : (
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
          <div className="divide-y divide-slate-800">
            {filteredProblems.map((prob) => (
              <div
                key={prob.id}
                className="p-4 sm:p-5 hover:bg-slate-800/40 transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4"
              >
                <div className="flex items-start sm:items-center gap-3.5 min-w-0">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5 sm:mt-0 ${
                    prob.is_solved 
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' 
                      : 'bg-slate-800 text-slate-500'
                  }`}>
                    {prob.is_solved ? <Check className="w-4 h-4" /> : <Code2 className="w-4 h-4" />}
                  </div>

                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <Link
                        to={`/workspace/${prob.id}`}
                        className="text-sm font-bold text-white hover:text-sky-400 transition-colors truncate"
                      >
                        {prob.title}
                      </Link>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        prob.difficulty.toLowerCase() === 'easy'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : prob.difficulty.toLowerCase() === 'medium'
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}>
                        {prob.difficulty}
                      </span>
                    </div>

                    <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 mt-1">
                      <span>Time: <strong className="text-slate-300">{prob.time_complexity || 'O(N)'}</strong></span>
                      <span>•</span>
                      <span>Space: <strong className="text-slate-300">{prob.space_complexity || 'O(1)'}</strong></span>
                      {prob.tags && prob.tags.length > 0 && (
                        <>
                          <span>•</span>
                          <span className="flex items-center gap-1 text-[11px] text-slate-400">
                            <Tag className="w-3 h-3 text-slate-500" />
                            {prob.tags.slice(0, 3).join(', ')}
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0 self-end sm:self-center">
                  <Link
                    to={`/workspace/${prob.id}`}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition-all shadow-md shadow-sky-600/20"
                  >
                    {prob.is_solved ? 'Practice Again' : 'Solve Challenge'}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
