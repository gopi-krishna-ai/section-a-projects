import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import { Topic, ProblemSummary } from '../types';
import { 
  Binary, 
  CheckCircle2, 
  Circle, 
  Clock, 
  ArrowRight, 
  Sparkles, 
  BookOpen,
  Code2,
  ChevronRight,
  TrendingUp,
  Award
} from 'lucide-react';

export const DSARoadmap: React.FC = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [problems, setProblems] = useState<ProblemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeStage, setActiveStage] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [topicList, probList] = await Promise.all([
          api.getTopics('dsa'),
          api.getProblems({ track: 'dsa' })
        ]);
        setTopics(topicList);
        setProblems(probList);
        if (topicList.length > 0) {
          setActiveStage(topicList[0].id);
        }
      } catch (err) {
        console.error('Failed to load DSA data', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const dsaStages = [
    { num: 1, name: 'Stage 1: Complexity & Algorithmic Analysis', description: 'Big-O, Omega, Theta, space limits, and recursion trees.' },
    { num: 2, name: 'Stage 2: Arrays & Dynamic Lists', description: 'Contiguous memory, 2-pointer patterns, sliding window, prefix sums.' },
    { num: 3, name: 'Stage 3: Strings & Pattern Matching', description: 'Two pointers, anagram frequency hashing, palindromes, KMP.' },
    { num: 4, name: 'Stage 4: Hash Tables & Hash Sets', description: 'O(1) lookups, collision resolution, frequency counting, memo keys.' },
    { num: 5, name: 'Stage 5: Linked Lists', description: 'Singly, doubly, fast/slow pointers, cycle detection, list reversal.' },
    { num: 6, name: 'Stage 6: Stacks & Queues', description: 'LIFO, FIFO, monotonic stack next-greater element, BFS queues, deques.' },
    { num: 7, name: 'Stage 7: Binary Trees & Tree Traversals', description: 'DFS (pre/in/post-order), BFS level order, height, max depth.' },
    { num: 8, name: 'Stage 8: Binary Search Trees & Heaps', description: 'BST invariant, insertion, min/max heap, PriorityQueue, top K.' },
    { num: 9, name: 'Stage 9: Binary Search & Search Space Reduction', description: 'Search on answer, monotonic predicate, lower/upper bounds.' },
    { num: 10, name: 'Stage 10: Recursion, Backtracking & Branching', description: 'Decision trees, subsets, permutations, N-Queens, pruning.' },
    { num: 11, name: 'Stage 11: Dynamic Programming Mastery', description: 'Overlapping subproblems, optimal substructure, 1D/2D state, tabulation.' },
    { num: 12, name: 'Stage 12: Graphs: BFS, DFS, Shortest Paths', description: 'Adjacency list, cycle detection, topological sort, Dijkstra, Union-Find.' },
    { num: 13, name: 'Stage 13: Greedy Algorithms & Bit Manipulation', description: 'Interval scheduling, Huffman coding, bitwise XOR single number, bitmasks.' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="w-8 h-8 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border border-indigo-500/30 relative overflow-hidden shadow-xl">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-indigo-500/10 to-transparent pointer-events-none" />
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold mb-3 border border-indigo-500/30">
            <Binary className="w-3.5 h-3.5" />
            <span>13-Stage Comprehensive DSA Curriculum</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            DSA Problem Solving Roadmap
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed mb-4">
            Master computer science data structures and algorithmic patterns step-by-step. Each stage bridges theoretical principles with LeetCode-style interview challenges.
          </p>
          <div className="flex flex-wrap gap-4 text-xs font-semibold text-slate-300">
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              <Award className="w-4 h-4 text-amber-400" />
              13 Progressive Stages
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              <Code2 className="w-4 h-4 text-sky-400" />
              {problems.length} Practice Problems
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              Independent Mastery Tracking
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid: Stages list + Active Stage details & problems */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stages Sidebar */}
        <div className="lg:col-span-1 space-y-3">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 px-1">
            Curriculum Stages
          </h2>
          <div className="space-y-2">
            {dsaStages.map((stage) => {
              const matchedTopic = topics.find(t => 
                t.title.toLowerCase().includes(stage.name.toLowerCase().split(':')[1]?.trim()?.toLowerCase() || '') ||
                stage.name.toLowerCase().includes(t.title.toLowerCase())
              );
              const isActive = (matchedTopic && activeStage === matchedTopic.id) || (!matchedTopic && activeStage === `stage-${stage.num}`);

              return (
                <button
                  key={stage.num}
                  onClick={() => setActiveStage(matchedTopic ? matchedTopic.id : `stage-${stage.num}`)}
                  className={`w-full text-left p-3.5 rounded-xl border transition-all cursor-pointer flex items-start gap-3 ${
                    isActive
                      ? 'bg-indigo-600/20 border-indigo-500/50 text-white shadow-md'
                      : 'bg-slate-900/60 border-slate-800/80 text-slate-300 hover:bg-slate-800/60 hover:border-slate-700'
                  }`}
                >
                  <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 ${
                    isActive ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {stage.num}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold truncate">
                      {stage.name.split(':')[1] || stage.name}
                    </div>
                    <div className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                      {stage.description}
                    </div>
                  </div>
                  <ChevronRight className={`w-4 h-4 shrink-0 mt-1 transition-transform ${isActive ? 'rotate-90 text-indigo-400' : 'text-slate-600'}`} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Selected Stage Detail & Problems */}
        <div className="lg:col-span-2 space-y-6">
          {(() => {
            const currentTopic = topics.find(t => t.id === activeStage);
            const currentStageNum = dsaStages.find(s => 
              (currentTopic && (s.name.toLowerCase().includes(currentTopic.title.toLowerCase()) || currentTopic.title.toLowerCase().includes(s.name.split(':')[1]?.trim()?.toLowerCase() || ''))) ||
              `stage-${s.num}` === activeStage
            ) || dsaStages[0];

            // Associated problems
            const stageProblems = problems.filter(p => 
              (currentTopic && p.topic_id === currentTopic.id) ||
              p.title.toLowerCase().includes(currentStageNum.name.split(':')[1]?.toLowerCase()?.trim() || 'xyz')
            );

            return (
              <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 sm:p-8 space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                  <div>
                    <span className="text-xs font-bold text-indigo-400 uppercase tracking-widest">
                      Stage Focus
                    </span>
                    <h2 className="text-xl font-bold text-white mt-1">
                      {currentStageNum.name}
                    </h2>
                    <p className="text-sm text-slate-300 mt-2 leading-relaxed">
                      {currentStageNum.description}
                    </p>
                  </div>
                  {currentTopic && (
                    <div className="text-right shrink-0 bg-slate-800/80 px-4 py-2.5 rounded-xl border border-slate-700/80">
                      <div className="text-[11px] font-semibold text-slate-400 uppercase">Mastery</div>
                      <div className="text-lg font-black text-emerald-400">
                        {Math.round(currentTopic.mastery_score || 0)}%
                      </div>
                    </div>
                  )}
                </div>

                {/* Key Theoretical Patterns */}
                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/80">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                    Essential Pattern Heuristics
                  </h3>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Always analyze the problem constraints before picking an algorithm: For N ≤ 10⁵, target O(N) or O(N log N). For N ≤ 1000, O(N²) may pass. For N ≤ 20, consider backtracking or bitmask dynamic programming.
                  </p>
                </div>

                {/* Problems in this stage */}
                <div>
                  <h3 className="text-sm font-bold text-white mb-3 flex items-center justify-between">
                    <span>Practice Problems for this Stage</span>
                    <span className="text-xs text-slate-400 font-normal">
                      {stageProblems.length > 0 ? `${stageProblems.length} available` : 'Curated Challenges'}
                    </span>
                  </h3>

                  {stageProblems.length === 0 ? (
                    <div className="p-8 rounded-xl border border-dashed border-slate-800 text-center bg-slate-950/30">
                      <Code2 className="w-8 h-8 text-slate-600 mx-auto mb-2" />
                      <p className="text-sm font-semibold text-slate-300">Curated Practice Available in Catalog</p>
                      <p className="text-xs text-slate-500 mt-1">
                        Explore our complete library of interview problems or open the freeform playground.
                      </p>
                      <Link
                        to="/problems"
                        className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold transition-colors"
                      >
                        Browse All Problems
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {stageProblems.map((prob) => (
                        <div
                          key={prob.id}
                          className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 flex items-center justify-between gap-4 transition-all"
                        >
                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <h4 className="text-sm font-bold text-white truncate">
                                {prob.title}
                              </h4>
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
                            <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                              <span>Optimal: {prob.time_complexity || 'O(N)'}</span>
                              <span>•</span>
                              <span>Space: {prob.space_complexity || 'O(1)'}</span>
                            </div>
                          </div>

                          <Link
                            to={`/workspace/${prob.id}`}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shrink-0 transition-colors"
                          >
                            Solve Problem
                            <ArrowRight className="w-3.5 h-3.5" />
                          </Link>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })()}
        </div>
      </div>
    </div>
  );
};
