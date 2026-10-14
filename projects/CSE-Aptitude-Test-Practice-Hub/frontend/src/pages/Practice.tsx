import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Zap, Compass, ShieldAlert, Shuffle, Clock, Trophy,
  RotateCcw, FileCheck, CheckCircle2, ArrowRight
} from 'lucide-react';
import { api } from '../api/client';
import { Topic } from '../types';

export const Practice: React.FC = () => {
  const navigate = useNavigate();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>('');
  const [selectedMode, setSelectedMode] = useState<string>('topic');
  const [sessionLength, setSessionLength] = useState<number>(10);
  const [difficulty, setDifficulty] = useState<string>('All');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.getTopics().then((res) => {
      setTopics(res);
      if (res.length > 0) setSelectedTopic(res[0].id);
    });
  }, []);

  const MODES = [
    {
      id: 'topic',
      title: 'Topic Practice',
      desc: 'Target a specific syllabus area to strengthen core mechanics.',
      icon: Zap,
      color: 'blue'
    },
    {
      id: 'guided',
      title: 'Guided Practice',
      desc: 'Receive progressive hints and step-by-step coach guidance on every problem.',
      icon: Compass,
      color: 'indigo'
    },
    {
      id: 'independent',
      title: 'Independent Practice',
      desc: 'Test your self-reliance without hints or explanations until final submission.',
      icon: CheckCircle2,
      color: 'emerald'
    },
    {
      id: 'weakness',
      title: 'Weakness Practice',
      desc: 'Prioritizes concepts with recorded errors in your Mistake Notebook.',
      icon: ShieldAlert,
      color: 'rose'
    },
    {
      id: 'mixed',
      title: 'Mixed Category Practice',
      desc: 'Cross-topic questions to practice rapid context switching.',
      icon: Shuffle,
      color: 'purple'
    },
    {
      id: 'timed',
      title: 'Timed Speed Practice',
      desc: 'Solve against the clock to build placement-level speed (60s/question).',
      icon: Clock,
      color: 'amber'
    },
    {
      id: 'challenge',
      title: 'Placement Challenge',
      desc: 'High-difficulty Intermediate and Advanced problems testing edge cases.',
      icon: Trophy,
      color: 'orange'
    },
    {
      id: 'revision',
      title: 'Spaced Revision',
      desc: 'Questions scheduled by the spaced repetition retention engine.',
      icon: RotateCcw,
      color: 'teal'
    }
  ];

  const handleStartPractice = async () => {
    setLoading(true);
    try {
      const res = await api.startSession({
        mode: selectedMode,
        topic_id: selectedMode === 'topic' || selectedMode === 'guided' ? selectedTopic : undefined,
        num_questions: sessionLength,
        level: difficulty !== 'All' ? difficulty : undefined
      });

      if (res.questions.length > 0) {
        navigate(`/workspace?qid=${res.questions[0].id}`);
      } else {
        alert('No questions matched your exact filters. Adjust criteria and retry.');
      }
    } catch (err: any) {
      alert(err.message || 'Failed to start session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Adaptive Practice Engine</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Select your training mode and parameters to build independent placement competence.
        </p>
      </div>

      {/* Mode Selection Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {MODES.map((m) => {
          const isSelected = selectedMode === m.id;
          return (
            <div
              key={m.id}
              onClick={() => setSelectedMode(m.id)}
              className={`p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'border-blue-600 bg-blue-50/70 shadow-sm ring-1 ring-blue-600'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              }`}
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    isSelected ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600'
                  }`}>
                    <m.icon className="w-4 h-4" />
                  </div>
                  {isSelected && (
                    <span className="text-[10px] font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded-full">
                      Selected
                    </span>
                  )}
                </div>
                <h3 className="text-xs sm:text-sm font-bold text-slate-900">{m.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed font-medium">{m.desc}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Configuration Controls */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-5">
        <h3 className="text-sm font-bold text-slate-900">Session Configuration</h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
          {/* Topic Select (if applicable) */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700">Topic Focus</label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              disabled={selectedMode === 'mixed' || selectedMode === 'weakness' || selectedMode === 'revision'}
              className="w-full px-3 py-2 text-xs font-medium rounded-lg border border-slate-300 bg-white text-slate-800 disabled:bg-slate-100 disabled:text-slate-400"
            >
              {topics.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.category})
                </option>
              ))}
            </select>
          </div>

          {/* Question Count */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700">Question Set Size</label>
            <div className="flex gap-2">
              {[5, 10, 20].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setSessionLength(num)}
                  className={`flex-1 py-2 text-xs font-bold rounded-lg border transition-colors cursor-pointer ${
                    sessionLength === num
                      ? 'bg-blue-600 border-blue-600 text-white'
                      : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {num} Qs
                </button>
              ))}
            </div>
          </div>

          {/* Difficulty Level */}
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-700">Difficulty Threshold</label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full px-3 py-2 text-xs font-medium rounded-lg border border-slate-300 bg-white text-slate-800"
            >
              <option value="All">All Levels (Progressive)</option>
              <option value="Basic">Foundational (Basic)</option>
              <option value="Intermediate">Multi-step (Intermediate)</option>
              <option value="Advanced">Placement Pressure (Advanced)</option>
            </select>
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={handleStartPractice}
            disabled={loading}
            className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 font-bold text-xs sm:text-sm text-white shadow-md shadow-blue-500/20 flex items-center gap-2 transition-all cursor-pointer"
          >
            {loading ? (
              <span>Preparing Session...</span>
            ) : (
              <>
                <span>Launch Practice Session</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
