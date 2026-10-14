import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Settings as SettingsIcon, 
  User, 
  Users, 
  Target, 
  Terminal, 
  ShieldCheck, 
  CheckCircle2, 
  Sparkles, 
  Cpu, 
  LogOut,
  RefreshCw
} from 'lucide-react';

export const Settings: React.FC = () => {
  const { currentUser, demoUsers, switchDemoUser, logout } = useAuth();
  const [switching, setSwitching] = useState<string | null>(null);

  const handleSwitch = async (username: string) => {
    try {
      setSwitching(username);
      await switchDemoUser(username);
    } catch (err) {
      console.error('Failed to switch user', err);
    } finally {
      setSwitching(null);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-slate-950 to-slate-900 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 text-slate-300 text-xs font-bold mb-3 border border-slate-700">
            <SettingsIcon className="w-3.5 h-3.5" />
            <span>Account & Learning Preferences</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Profile & Platform Settings
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Manage your personal learning goals, target career benchmark, or switch between pre-seeded learner profiles to preview different skill trajectories.
          </p>
        </div>

        <button
          onClick={logout}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-rose-950/40 hover:border-rose-500/50 hover:text-rose-300 border border-slate-700 text-slate-300 text-xs font-bold transition-all flex items-center gap-2 self-start md:self-center shrink-0 cursor-pointer"
        >
          <LogOut className="w-4 h-4" />
          Log Out
        </button>
      </div>

      {/* User Information Card */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div className="flex items-center gap-4 pb-6 border-b border-slate-800">
          <div className="w-16 h-16 rounded-2xl bg-sky-600/20 text-sky-400 border border-sky-500/30 flex items-center justify-center text-xl font-black">
            {currentUser?.avatar || 'PY'}
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">
              {currentUser?.full_name || currentUser?.username}
            </h2>
            <p className="text-xs text-slate-400">@{currentUser?.username} • Member</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold text-slate-400 uppercase flex items-center gap-1.5">
              <Terminal className="w-3.5 h-3.5 text-sky-400" />
              Skill Level
            </div>
            <div className="text-sm font-bold text-white mt-1 capitalize">
              {currentUser?.skill_level || 'Intermediate'} Python
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold text-slate-400 uppercase flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-emerald-400" />
              Target Goal
            </div>
            <div className="text-sm font-bold text-white mt-1">
              {currentUser?.target_goal || 'FAANG & Competitive DSA'}
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800">
            <div className="text-[11px] font-bold text-slate-400 uppercase flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
              Environment
            </div>
            <div className="text-sm font-bold text-white mt-1">
              Python 3.12 Sandboxed
            </div>
          </div>
        </div>
      </div>

      {/* 1-Click Multi-User Profile Switcher */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Users className="w-4 h-4 text-sky-400" />
            Switch Learner Profile (Multi-User Demo)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Experience the platform from different perspectives with pre-seeded progress data, solved problems, and revision schedules.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          {demoUsers.map((user) => {
            const isCurrent = currentUser?.username === user.username;
            return (
              <div
                key={user.id}
                className={`p-4 rounded-xl border transition-all flex items-center justify-between gap-4 ${
                  isCurrent
                    ? 'bg-sky-950/30 border-sky-500/60 shadow-md'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                    isCurrent ? 'bg-sky-500 text-white' : 'bg-slate-800 text-slate-400'
                  }`}>
                    {user.avatar || 'PY'}
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs font-bold text-white flex items-center gap-1.5 truncate">
                      {user.full_name}
                      {isCurrent && (
                        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-sky-500/20 text-sky-400 border border-sky-500/30">
                          Active
                        </span>
                      )}
                    </div>
                    <div className="text-[11px] text-slate-400 truncate mt-0.5">
                      {user.target_goal} • <span className="capitalize">{user.skill_level}</span>
                    </div>
                  </div>
                </div>

                {!isCurrent && (
                  <button
                    disabled={switching === user.username}
                    onClick={() => handleSwitch(user.username)}
                    className="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white text-xs font-bold transition-all shrink-0 cursor-pointer"
                  >
                    {switching === user.username ? 'Switching...' : 'Switch'}
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* System Architecture Specifications */}
      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h2 className="text-base font-bold text-white flex items-center gap-2">
          <Cpu className="w-4 h-4 text-emerald-400" />
          Platform Architecture & AI Systems
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-sky-400">Execution Sandbox:</div>
            <p className="text-slate-400 leading-relaxed">
              Subprocess isolation with a 4.0-second timeout ceiling, 100KB output buffer limit, memory tracking, and automated JSON test harness evaluation.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-emerald-400">SM-2 Spaced Repetition:</div>
            <p className="text-slate-400 leading-relaxed">
              SuperMemo-2 interval formula (\(I = I \times EF\)) with dynamic ease adjustment and minimum 1.3 EF bounds for long-term memory consolidation.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-purple-400">6-Stage Socratic Guidance:</div>
            <p className="text-slate-400 leading-relaxed">
              Problem Restatement → Structural Clue → Pattern Identification → Pseudocode Scaffold → Edge Case Alert → Code Walkthrough.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1.5">
            <div className="font-bold text-rose-400">22 Mistake Taxonomy:</div>
            <p className="text-slate-400 leading-relaxed">
              Automated regex and trace analysis diagnosing off-by-one errors, shared state mutations, missing base cases, and time complexity failures.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
