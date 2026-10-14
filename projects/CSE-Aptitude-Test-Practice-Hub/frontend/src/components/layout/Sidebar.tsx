import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  BookOpen,
  Zap,
  PenTool,
  BookX,
  RotateCcw,
  FileCheck,
  BarChart3,
  Library,
  Settings,
  GraduationCap,
  Users
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
    { to: '/learn', label: 'Learn & Syllabus', icon: BookOpen },
    { to: '/practice', label: 'Practice Modes', icon: Zap },
    { to: '/workspace', label: 'Solver Workspace', icon: PenTool },
    { to: '/mistakes', label: 'Mistake Notebook', icon: BookX },
    {
      to: '/revision',
      label: 'Spaced Revision',
      icon: RotateCcw,
      badge: dueRevisionsCount > 0 ? dueRevisionsCount : undefined
    },
    { to: '/mock-tests', label: 'Placement Exams', icon: FileCheck },
    { to: '/analytics', label: 'Progress & Analytics', icon: BarChart3 },
    { to: '/library', label: 'Question Bank (1800)', icon: Library },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 bg-slate-900/50 z-40 md:hidden"
          onClick={onCloseMobile}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-900 text-slate-100 flex flex-col border-r border-slate-800 transition-transform duration-200 ease-in-out md:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-6 border-b border-slate-800 bg-slate-950/60">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-sm tracking-wide text-white uppercase">Aptitude Coach</h1>
            <p className="text-xs text-blue-400 font-medium">Placement AI Platform</p>
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
                `flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/80'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <item.icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && (
                <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-amber-500 text-slate-950">
                  {item.badge}
                </span>
              )}
            </NavLink>
          ))}
        </nav>

        {/* Interactive User Switcher Card */}
        <div className="p-3 border-t border-slate-800 bg-slate-950/40">
          <div
            onClick={onOpenAuth}
            className="flex items-center gap-3 p-2 rounded-xl bg-slate-800/60 hover:bg-slate-800 transition-colors cursor-pointer border border-slate-700/60"
            title="Click to switch learner or sign in"
          >
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-xs font-bold text-white shrink-0">
              {currentUser?.avatar || currentUser?.username.slice(0, 2).toUpperCase() || 'DL'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">
                {currentUser?.full_name || currentUser?.username || 'Demo Learner'}
              </p>
              <p className="text-[11px] text-emerald-400 font-medium truncate">
                {currentUser?.target_company || 'TCS / Infosys'}
              </p>
            </div>
            <Users className="w-3.5 h-3.5 text-slate-400 hover:text-white" />
          </div>
        </div>
      </aside>
    </>
  );
};
