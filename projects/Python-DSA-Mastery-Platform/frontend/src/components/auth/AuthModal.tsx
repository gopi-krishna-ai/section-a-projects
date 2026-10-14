import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { X, UserCheck, KeyRound, Sparkles, LogIn, UserPlus } from 'lucide-react';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const { demoUsers, switchDemoUser, login, register } = useAuth();
  const [tab, setTab] = useState<'demo' | 'login' | 'register'>('demo');

  // Form states
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [targetGoal, setTargetGoal] = useState('FAANG & Competitive DSA');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleDemoSelect = async (uname: string) => {
    setLoading(true);
    setError(null);
    try {
      await switchDemoUser(uname);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to switch demo user');
    } finally {
      setLoading(false);
    }
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) return;
    setLoading(true);
    setError(null);
    try {
      await login(username, password);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) return;
    setLoading(true);
    setError(null);
    try {
      await register({
        username,
        password,
        full_name: fullName,
        email,
        target_goal: targetGoal,
      });
      onClose();
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 p-4 backdrop-blur-xs">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden flex flex-col text-slate-100 animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center border border-sky-500/30">
              <KeyRound className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-sm sm:text-base text-white">Select Learner Profile</h3>
              <p className="text-xs text-slate-400">Independent tracking for multiple developers</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex border-b border-slate-800 bg-slate-950/30 p-1">
          <button
            type="button"
            onClick={() => setTab('demo')}
            className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
              tab === 'demo' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>1-Click Demo Profiles</span>
          </button>
          <button
            type="button"
            onClick={() => setTab('login')}
            className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
              tab === 'login' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>
          <button
            type="button"
            onClick={() => setTab('register')}
            className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-colors cursor-pointer flex items-center justify-center gap-1.5 ${
              tab === 'register' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Create Account</span>
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mx-6 mt-4 p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs font-medium">
            {error}
          </div>
        )}

        {/* Body */}
        <div className="p-6">
          {tab === 'demo' && (
            <div className="space-y-3">
              <p className="text-xs text-slate-400 mb-2">
                Switch profiles to explore independent mastery, mistake notebooks, and spaced revision queues:
              </p>
              <div className="grid grid-cols-1 gap-2.5">
                {demoUsers.map((user) => (
                  <button
                    key={user.id}
                    type="button"
                    disabled={loading}
                    onClick={() => handleDemoSelect(user.username)}
                    className="p-3.5 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800/80 hover:border-sky-500/50 transition-all text-left flex items-center justify-between group cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-lg bg-sky-600/30 text-sky-400 border border-sky-500/30 flex items-center justify-center font-bold text-xs">
                        {user.avatar || user.username.slice(0, 2).toUpperCase()}
                      </div>
                      <div>
                        <div className="text-xs sm:text-sm font-bold text-white group-hover:text-sky-300 transition-colors">
                          {user.full_name || user.username}
                        </div>
                        <div className="text-[11px] text-slate-400 flex items-center gap-2">
                          <span className="font-mono text-sky-400">@{user.username}</span>
                          <span>&bull;</span>
                          <span className="text-amber-300">{user.target_goal}</span>
                        </div>
                      </div>
                    </div>
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 group-hover:bg-sky-600 group-hover:text-white transition-colors">
                      Switch
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {tab === 'login' && (
            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. py_ninja or custom username"
                  className="w-full px-3.5 py-2.5 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2.5 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-lg bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white shadow-lg transition-all cursor-pointer"
              >
                {loading ? 'Authenticating...' : 'Sign In to Learning Environment'}
              </button>
            </form>
          )}

          {tab === 'register' && (
            <form onSubmit={handleRegisterSubmit} className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="developer_handle"
                  className="w-full px-3.5 py-2 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Full Name</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Your Name"
                  className="w-full px-3.5 py-2 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Primary Learning Goal</label>
                <select
                  value={targetGoal}
                  onChange={(e) => setTargetGoal(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="FAANG & Competitive DSA">FAANG & Competitive Coding</option>
                  <option value="Senior Python Backend Architecture">Senior Python Backend Architecture</option>
                  <option value="Algorithmic Problem-Solving Intuition">Algorithmic Problem-Solving Intuition</option>
                  <option value="Technical Interview Readiness">Technical Interview Readiness</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-3.5 py-2 text-xs rounded-lg border border-slate-800 bg-slate-950 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  required
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-lg bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white shadow-lg transition-all cursor-pointer mt-2"
              >
                {loading ? 'Creating Account...' : 'Initialize Personal Platform'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
