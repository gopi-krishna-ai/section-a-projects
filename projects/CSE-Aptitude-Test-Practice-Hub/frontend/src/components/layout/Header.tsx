import React from 'react';
import { Menu, Target, CheckCircle2, Users } from 'lucide-react';
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
    <header className="h-16 bg-white border-b border-slate-200 px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobileNav}
          className="p-2 -ml-2 rounded-lg text-slate-600 hover:bg-slate-100 md:hidden focus:outline-none"
          aria-label="Open navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 leading-tight">{title}</h2>
          {subtitle && <p className="text-xs text-slate-500 leading-tight hidden sm:block">{subtitle}</p>}
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Placement target badge */}
        <div className="hidden lg:flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-xs font-semibold text-blue-700">
          <Target className="w-3.5 h-3.5" />
          <span>{currentUser?.target_company || 'Placement Exam Ready'}</span>
        </div>

        {/* 1,800 Verified Questions badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-700">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>1,800 Questions</span>
        </div>

        {/* User Account Pill / Switcher */}
        <button
          onClick={onOpenAuth}
          className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-200 hover:border-blue-400 bg-slate-50 hover:bg-blue-50 transition-colors cursor-pointer text-xs font-semibold text-slate-800"
        >
          <div className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px] font-bold">
            {currentUser?.avatar || currentUser?.username.slice(0, 2).toUpperCase() || 'U'}
          </div>
          <span className="hidden sm:inline font-bold text-slate-900">
            {currentUser?.full_name?.split(' ')[0] || currentUser?.username || 'Learner'}
          </span>
          <Users className="w-3.5 h-3.5 text-slate-500" />
        </button>
      </div>
    </header>
  );
};
