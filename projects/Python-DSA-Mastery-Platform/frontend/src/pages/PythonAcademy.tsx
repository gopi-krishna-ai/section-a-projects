import React, { useEffect, useState } from 'react';
import { Terminal, BookOpen, Play, CheckCircle2, Cpu, Boxes, ArrowRight } from 'lucide-react';
import { api } from '../api/client';
import { Topic, Lesson } from '../types';

export const PythonAcademy: React.FC = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<string>('py_intermediate');
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);

  // Playground snippet execution inside lesson
  const [executingSnippetIdx, setExecutingSnippetIdx] = useState<number | null>(null);
  const [snippetOutputs, setSnippetOutputs] = useState<Record<number, string>>({});

  useEffect(() => {
    loadTopics();
  }, []);

  const loadTopics = async () => {
    try {
      setLoading(true);
      const res = await api.getTopics('python');
      setTopics(res);
      if (res.length > 0) {
        setSelectedTopicId(res[0].id);
        loadLessons(res[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadLessons = async (topicId: string) => {
    try {
      const res = await api.getTopicLessons(topicId);
      setLessons(res);
      if (res.length > 0) {
        setSelectedLesson(res[0]);
      } else {
        setSelectedLesson(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelectTopic = (topicId: string) => {
    setSelectedTopicId(topicId);
    setSnippetOutputs({});
    loadLessons(topicId);
  };

  const handleRunSnippet = async (idx: number, code: string) => {
    setExecutingSnippetIdx(idx);
    try {
      const res = await api.runCode(code);
      setSnippetOutputs((prev) => ({
        ...prev,
        [idx]: res.stdout || res.stderr || 'Executed successfully with no output.'
      }));
    } catch (err: any) {
      setSnippetOutputs((prev) => ({
        ...prev,
        [idx]: `Error: ${err.message}`
      }));
    } finally {
      setExecutingSnippetIdx(null);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex flex-col items-center justify-center min-h-[50vh] text-slate-400 gap-3">
        <div className="w-8 h-8 border-3 border-sky-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-xs font-mono">Loading Python curriculum...</p>
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto space-y-6 text-slate-100">
      {/* Header */}
      <div>
        <h1 className="text-xl sm:text-2xl font-black text-white">Python Mastery Academy</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          From Intermediate mechanics to Advanced data models and Production Engineering.
        </p>
      </div>

      {/* Level Selector Pills */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {topics.map((t) => {
          const isSelected = t.id === selectedTopicId;
          return (
            <button
              key={t.id}
              onClick={() => handleSelectTopic(t.id)}
              className={`p-4 rounded-2xl border text-left transition-all cursor-pointer space-y-1.5 ${
                isSelected
                  ? 'bg-sky-950/60 border-sky-500 ring-1 ring-sky-500 shadow-md shadow-sky-950'
                  : 'bg-slate-900 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400">
                  {t.level}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                  {t.mastery_score}% mastery
                </span>
              </div>
              <h3 className="font-bold text-xs sm:text-sm text-white">{t.title}</h3>
              <p className="text-[11px] text-slate-400 line-clamp-2">{t.description}</p>
            </button>
          );
        })}
      </div>

      {/* Main Lesson Viewer */}
      {selectedLesson ? (
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <span className="text-[10px] font-bold text-sky-400 uppercase tracking-wider">Concept Lesson</span>
            <h2 className="text-lg sm:text-2xl font-black text-white mt-1">{selectedLesson.title}</h2>
          </div>

          {/* Lesson Content Markdown */}
          <div className="prose prose-invert max-w-none text-xs sm:text-sm leading-relaxed text-slate-300 whitespace-pre-wrap font-sans">
            {selectedLesson.content}
          </div>

          {/* Runnable Code Snippets */}
          {selectedLesson.runnable_snippets && selectedLesson.runnable_snippets.length > 0 && (
            <div className="space-y-4 pt-4 border-t border-slate-800">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Terminal className="w-4 h-4 text-amber-400" />
                <span>Runnable Interactive Code Examples</span>
              </h3>

              <div className="space-y-4">
                {selectedLesson.runnable_snippets.map((snip, idx) => (
                  <div key={idx} className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-sm">
                    <div className="flex items-center justify-between px-4 py-2.5 bg-slate-900/80 border-b border-slate-800 text-xs">
                      <span className="font-bold text-slate-200">{snip.title}</span>
                      <button
                        type="button"
                        disabled={executingSnippetIdx === idx}
                        onClick={() => handleRunSnippet(idx, snip.code)}
                        className="px-3 py-1 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-[11px] flex items-center gap-1.5 transition-colors cursor-pointer disabled:opacity-40"
                      >
                        <Play className="w-3 h-3 fill-white" />
                        <span>{executingSnippetIdx === idx ? 'Executing...' : 'Run Snippet'}</span>
                      </button>
                    </div>

                    <pre className="p-4 text-xs font-mono text-sky-200 bg-slate-950 overflow-x-auto leading-relaxed">
                      {snip.code}
                    </pre>

                    {snippetOutputs[idx] && (
                      <div className="px-4 py-3 bg-slate-900/60 border-t border-slate-800 font-mono text-xs text-amber-300 whitespace-pre-wrap">
                        <span className="text-[10px] uppercase text-slate-500 font-bold block mb-1">Execution Output:</span>
                        {snippetOutputs[idx]}
                      </div>
                    )}

                    <div className="px-4 py-2 bg-slate-900/40 text-[11px] text-slate-400 border-t border-slate-800/80">
                      💡 {snip.explanation}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Key Takeaways */}
          {selectedLesson.key_takeaways && selectedLesson.key_takeaways.length > 0 && (
            <div className="p-4 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 space-y-2">
              <div className="text-xs font-bold text-emerald-400">Key Engineering Takeaways</div>
              <ul className="list-disc pl-4 space-y-1 text-xs text-slate-300">
                {selectedLesson.key_takeaways.map((point, i) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ) : (
        <div className="p-12 text-center text-slate-500 text-xs bg-slate-900 border border-slate-800 rounded-3xl">
          Select a topic to read lessons and run code snippets.
        </div>
      )}
    </div>
  );
};
