import React from 'react';
import { Menu, Terminal, Users, Sparkles, Target } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface HeaderProps {
  title: string;
  subtitle?: string;
  onOpenMobileNav: () => void;
  onOpenAuth?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ title, subtitle, onOpenMobileNav, onOpenAuth }) => {
  const { currentUser } = useAuth();

  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobileNav}
          className="p-2 -ml-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 md:hidden focus:outline-none"
          aria-label="Open navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div>
          <h2 className="text-sm sm:text-base font-extrabold text-white leading-tight">{title}</h2>
          {subtitle && <p className="text-[11px] text-slate-400 leading-tight hidden sm:block">{subtitle}</p>}
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Target Goal Pill */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/20 text-xs font-semibold text-sky-400">
          <Target className="w-3.5 h-3.5" />
          <span>{currentUser?.target_goal || 'FAANG & Competitive DSA'}</span>
        </div>

        {/* Skill level indicator */}
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-semibold text-emerald-400">
          <Terminal className="w-3.5 h-3.5" />
          <span className="capitalize">{currentUser?.skill_level || 'Intermediate'} Python</span>
        </div>

        {/* Profile Switcher Button */}
        <button
          onClick={onOpenAuth}
          className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-700 hover:border-sky-500/50 bg-slate-800/80 hover:bg-slate-800 transition-colors cursor-pointer text-xs font-semibold text-slate-200"
        >
          <div className="w-5 h-5 rounded-full bg-sky-600 text-white flex items-center justify-center text-[10px] font-bold">
            {currentUser?.avatar || 'PY'}
          </div>
          <span className="hidden sm:inline font-bold text-white">
            {currentUser?.full_name?.split(' ')[0] || currentUser?.username || 'User'}
          </span>
          <Users className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>
    </header>
  );
};
