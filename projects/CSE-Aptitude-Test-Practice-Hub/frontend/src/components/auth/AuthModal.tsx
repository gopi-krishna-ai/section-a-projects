import React, { useState } from 'react';
import { X, User, Lock, Mail, Target, CheckCircle2, ArrowRight, UserPlus, LogIn } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose }) => {
  const { currentUser, demoUsers, login, register, switchDemoUser } = useAuth();
  const [tab, setTab] = useState<'demo' | 'login' | 'register'>('demo');

  // Form states
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [targetCompany, setTargetCompany] = useState('TCS / Infosys');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleDemoSwitch = async (uname: string) => {
    setLoading(true);
    setError(null);
    try {
      await switchDemoUser(uname);
      onClose();
      // Reload page to refresh all active user states
      window.location.reload();
    } catch (err: any) {
      setError(err.message || 'Failed to switch user');
    } finally {
      setLoading(false);
    }
  };

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(username, password);
      onClose();
      window.location.reload();
    } catch (err: any) {
      setError(err.message || 'Invalid login credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register({
        username,
        password,
        email,
        full_name: fullName,
        target_company: targetCompany,
      });
      onClose();
      window.location.reload();
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div>
            <h3 className="font-bold text-slate-900 text-base">User Accounts & Profiles</h3>
            <p className="text-xs text-slate-500">Switch learners or create your personal account</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Current User Pill */}
        {currentUser && (
          <div className="px-5 py-2.5 bg-blue-50/80 border-b border-blue-100 flex items-center justify-between text-xs">
            <span className="text-blue-900">
              Active Learner: <strong className="font-bold">{currentUser.full_name || currentUser.username}</strong> (@{currentUser.username})
            </span>
            <span className="text-[11px] font-semibold text-blue-700 bg-blue-100 px-2 py-0.5 rounded-full">
              {currentUser.target_company}
            </span>
          </div>
        )}

        {/* Tab Switcher */}
        <div className="flex border-b border-slate-200 bg-slate-100/70 text-xs font-semibold">
          <button
            onClick={() => { setTab('demo'); setError(null); }}
            className={`flex-1 py-2.5 text-center transition-colors border-b-2 cursor-pointer ${
              tab === 'demo' ? 'border-blue-600 text-blue-600 bg-white font-bold' : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            ⚡ 1-Click Demo Users
          </button>
          <button
            onClick={() => { setTab('login'); setError(null); }}
            className={`flex-1 py-2.5 text-center transition-colors border-b-2 cursor-pointer ${
              tab === 'login' ? 'border-blue-600 text-blue-600 bg-white font-bold' : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => { setTab('register'); setError(null); }}
            className={`flex-1 py-2.5 text-center transition-colors border-b-2 cursor-pointer ${
              tab === 'register' ? 'border-blue-600 text-blue-600 bg-white font-bold' : 'border-transparent text-slate-500 hover:text-slate-900'
            }`}
          >
            New Account
          </button>
        </div>

        {/* Body */}
        <div className="p-5 overflow-y-auto space-y-4">
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 text-xs rounded-xl font-medium">
              {error}
            </div>
          )}

          {/* TAB 1: 1-Click Demo Profiles */}
          {tab === 'demo' && (
            <div className="space-y-3">
              <p className="text-xs text-slate-500">
                Select any test student profile below. Each learner maintains their own independent mastery scores, mistake notebooks, and revision schedules:
              </p>

              <div className="space-y-2.5">
                {demoUsers.map((u) => {
                  const isActive = currentUser?.username === u.username;
                  return (
                    <div
                      key={u.id}
                      onClick={() => handleDemoSwitch(u.username)}
                      className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        isActive
                          ? 'border-blue-600 bg-blue-50/70 shadow-xs ring-1 ring-blue-600'
                          : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/60'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold shrink-0">
                          {u.avatar || u.username.slice(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <div className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                            <span>{u.full_name || u.username}</span>
                            {isActive && <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />}
                          </div>
                          <div className="text-[11px] text-slate-500">
                            Target: <span className="font-semibold text-slate-700">{u.target_company}</span>
                          </div>
                        </div>
                      </div>

                      <button
                        type="button"
                        className={`px-3 py-1 text-xs font-bold rounded-lg transition-colors cursor-pointer ${
                          isActive
                            ? 'bg-blue-600 text-white'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        }`}
                      >
                        {isActive ? 'Current' : 'Switch'}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 2: Custom Sign In */}
          {tab === 'login' && (
            <form onSubmit={handleLoginSubmit} className="space-y-3.5">
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Username</label>
                <div className="relative">
                  <User className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. rohan or your_username"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-colors flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
              >
                <LogIn className="w-4 h-4" />
                <span>{loading ? 'Authenticating...' : 'Sign In to Account'}</span>
              </button>
            </form>
          )}

          {/* TAB 3: New Account Registration */}
          {tab === 'register' && (
            <form onSubmit={handleRegisterSubmit} className="space-y-3">
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Full Name</label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. John Doe"
                  className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Username</label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. johndoe24"
                  className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Target Placement Assessment</label>
                <select
                  value={targetCompany}
                  onChange={(e) => setTargetCompany(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-800"
                >
                  <option value="TCS / Infosys">TCS NQT & Infosys Specialist</option>
                  <option value="Accenture Cognitive">Accenture Cognitive Assessment</option>
                  <option value="Wipro / Cognizant">Wipro Elite & Cognizant GenC</option>
                  <option value="General Placements">General Engineering Placements</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700">Password</label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-colors flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
              >
                <UserPlus className="w-4 h-4" />
                <span>{loading ? 'Creating Profile...' : 'Create Account & Start Learning'}</span>
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
