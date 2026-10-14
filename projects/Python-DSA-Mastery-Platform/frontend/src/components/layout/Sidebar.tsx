import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Terminal,
  Brain,
  Binary,
  Code2,
  Bug,
  BookX,
  RotateCcw,
  PlaySquare,
  Settings,
  Cpu,
  UserCheck
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface SidebarProps {
  dueRevisionsCount?: number;
  isOpenMobile?: boolean;
  onCloseMobile?: () => void;
  onOpenAuth?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  dueRevisionsCount = 0,
  isOpenMobile = false,
  onCloseMobile,
  onOpenAuth
}) => {
  const { currentUser } = useAuth();

  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/python', label: 'Python Academy', icon: Terminal },
    { to: '/logic', label: 'Logic Gym', icon: Brain },
    { to: '/dsa', label: 'DSA Roadmap', icon: Binary },
    { to: '/problems', label: 'Problem Library', icon: Code2 },
    { to: '/playground', label: 'Coding Playground', icon: PlaySquare },
    { to: '/debug-lab', label: 'Debugging Lab', icon: Bug },
    { to: '/mistakes', label: 'Mistake Notebook', icon: BookX },
    {
      to: '/revision',
      label: 'Spaced Revision',
      icon: RotateCcw,
      badge: dueRevisionsCount > 0 ? dueRevisionsCount : undefined
    },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 bg-slate-950/70 z-40 md:hidden backdrop-blur-xs"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-950 text-slate-100 flex flex-col border-r border-slate-800/80 transition-transform duration-200 ease-in-out md:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-5 border-b border-slate-800/80 bg-slate-900/40">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-extrabold text-sm tracking-wide text-white">PYTHON & DSA</h1>
            <p className="text-[11px] text-sky-400 font-semibold tracking-wider uppercase">Mastery Platform</p>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onCloseMobile}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/80'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <item.icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && (
                <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-amber-500 text-slate-950 shadow-xs">
                  {item.badge}
                </span>
              )}
            </NavLink>
          ))}
        </nav>

        {/* User Profile Footer */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-900/30">
          <button
            type="button"
            onClick={onOpenAuth}
            className="w-full p-2.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800/80 transition-colors flex items-center justify-between text-left cursor-pointer"
          >
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-500/30 flex items-center justify-center text-xs font-bold shrink-0">
                {currentUser?.avatar || 'PY'}
              </div>
              <div className="min-w-0">
                <div className="text-xs font-bold text-white truncate">
                  {currentUser?.full_name || currentUser?.username || 'Learner'}
                </div>
                <div className="text-[10px] text-slate-400 truncate">
                  {currentUser?.target_goal || 'DSA Mastery'}
                </div>
              </div>
            </div>
            <UserCheck className="w-4 h-4 text-sky-400 shrink-0" />
          </button>
        </div>
      </aside>
    </>
  );
};
