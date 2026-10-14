import React, { useState } from 'react';
import { Sparkles, X, HelpCircle, Send, CheckCircle2, AlertCircle } from 'lucide-react';
import { api } from '../../api/client';

interface SocraticModalProps {
  isOpen: boolean;
  onClose: () => void;
  problemId: string;
  problemTitle: string;
  userCode: string;
  currentHintLevel: number;
  onHintUnlocked: (level: number) => void;
}

export const SocraticModal: React.FC<SocraticModalProps> = ({
  isOpen,
  onClose,
  problemId,
  problemTitle,
  userCode,
  currentHintLevel,
  onHintUnlocked
}) => {
  const [hints, setHints] = useState<Array<{ level: number; title: string; content: string; is_full_solution: boolean }>>([]);
  const [loadingHint, setLoadingHint] = useState(false);
  const [query, setQuery] = useState('');
  const [mentorChat, setMentorChat] = useState<Array<{ sender: 'user' | 'mentor'; text: string }>>([]);
  const [mentorLoading, setMentorLoading] = useState(false);

  if (!isOpen) return null;

  const handleFetchNextHint = async () => {
    const nextLevel = Math.min(6, (hints.length > 0 ? hints[hints.length - 1].level + 1 : 1));
    setLoadingHint(true);
    try {
      const res = await api.fetchHint(problemId, nextLevel);
      setHints((prev) => [...prev, res]);
      onHintUnlocked(nextLevel);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingHint(false);
    }
  };

  const handleAskMentor = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userText = query.trim();
    setMentorChat((p) => [...p, { sender: 'user', text: userText }]);
    setQuery('');
    setMentorLoading(true);

    try {
      const res = await api.askMentor(problemId, {
        code: userCode,
        query: userText
      });
      setMentorChat((p) => [...p, { sender: 'mentor', text: res.response }]);
    } catch (err: any) {
      setMentorChat((p) => [...p, { sender: 'mentor', text: 'Mentor temporarily unavailable.' }]);
    } finally {
      setMentorLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 p-4 backdrop-blur-xs">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl max-h-[85vh] shadow-2xl flex flex-col text-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center border border-sky-500/30">
              <Sparkles className="w-4 h-4 text-sky-400" />
            </div>
            <div>
              <h3 className="font-bold text-sm sm:text-base text-white">Socratic AI Coding Mentor</h3>
              <p className="text-xs text-slate-400">{problemTitle}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Container */}
        <div className="flex-1 p-6 overflow-y-auto space-y-5">
          {/* Progressive Hints Section */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Progressive Socratic Hints ({hints.length}/6)
              </span>
              <button
                type="button"
                disabled={loadingHint || hints.length >= 6}
                onClick={handleFetchNextHint}
                className="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all disabled:opacity-40 cursor-pointer"
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>
                  {hints.length === 0 ? 'Request Level 1 Hint' : `Request Hint ${hints.length + 1}`}
                </span>
              </button>
            </div>

            {hints.length === 0 ? (
              <div className="p-4 rounded-xl border border-dashed border-slate-800 text-center text-xs text-slate-400">
                No hints unlocked yet. Attempt the problem independently first, or request Level 1 for a clarifying nudge!
              </div>
            ) : (
              <div className="space-y-2.5">
                {hints.map((h) => (
                  <div
                    key={h.level}
                    className="p-3.5 rounded-xl border border-slate-800 bg-slate-950/70 space-y-1.5"
                  >
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded-md bg-sky-500/20 text-sky-400 text-[10px] font-bold">
                        Hint {h.level}
                      </span>
                      <span className="text-xs font-bold text-white">{h.title}</span>
                    </div>
                    <p className="text-xs text-slate-300 whitespace-pre-wrap leading-relaxed font-mono">
                      {h.content}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Interactive Mentor Q&A */}
          <div className="pt-4 border-t border-slate-800 space-y-3">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
              Ask Mentor a Conceptual Question
            </span>

            {/* Chat history */}
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {mentorChat.map((msg, i) => (
                <div
                  key={i}
                  className={`p-3 rounded-xl text-xs leading-relaxed ${
                    msg.sender === 'user'
                      ? 'bg-sky-950/50 border border-sky-800/40 text-sky-200 ml-8'
                      : 'bg-slate-950 border border-slate-800 text-slate-300 mr-8 whitespace-pre-wrap font-mono'
                  }`}
                >
                  <span className="text-[10px] font-bold uppercase block text-slate-400 mb-1">
                    {msg.sender === 'user' ? 'You' : 'Socratic Mentor'}
                  </span>
                  {msg.text}
                </div>
              ))}
              {mentorLoading && (
                <div className="text-xs text-slate-400 italic">Mentor is reasoning...</div>
              )}
            </div>

            {/* Form */}
            <form onSubmit={handleAskMentor} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask e.g.: Why is my sliding window left pointer jumping backwards?"
                className="flex-1 px-3.5 py-2.5 rounded-xl border border-slate-800 bg-slate-950 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
              <button
                type="submit"
                disabled={mentorLoading || !query.trim()}
                className="px-4 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs flex items-center gap-1.5 transition-all disabled:opacity-40 cursor-pointer shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Ask</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
