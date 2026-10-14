import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { AuthModal } from './components/auth/AuthModal';
import { api } from './api/client';

// Pages
import { Dashboard } from './pages/Dashboard';
import { PythonAcademy } from './pages/PythonAcademy';
import { DSARoadmap } from './pages/DSARoadmap';
import { Problems } from './pages/Problems';
import { Workspace } from './pages/Workspace';
import { LogicGym } from './pages/LogicGym';
import { DebugLab } from './pages/DebugLab';
import { MistakeNotebook } from './pages/MistakeNotebook';
import { RevisionCenter } from './pages/RevisionCenter';
import { Playground } from './pages/Playground';
import { Settings } from './pages/Settings';

const AppLayout: React.FC = () => {
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [dueRevisionsCount, setDueRevisionsCount] = useState(0);
  const location = useLocation();
  const { currentUser } = useAuth();

  useEffect(() => {
    async function fetchRevisions() {
      try {
        const revs = await api.getDueRevisions();
        setDueRevisionsCount(revs.length);
      } catch (err) {
        // Silently fail if unauthenticated
      }
    }
    fetchRevisions();
  }, [currentUser, location.pathname]);

  // Determine current page title
  const getPageInfo = () => {
    const path = location.pathname;
    if (path === '/') return { title: 'Mastery Dashboard', subtitle: 'Real-time performance, independent vs assisted metrics' };
    if (path === '/python') return { title: 'Python Academy', subtitle: 'Intermediate to advanced Python mental models' };
    if (path === '/logic') return { title: 'Logic & Reasoning Gym', subtitle: '15 reasoning patterns & mental deduction puzzles' };
    if (path === '/dsa') return { title: 'DSA 13-Stage Roadmap', subtitle: 'Data structures & algorithm patterns from scratch' };
    if (path === '/problems') return { title: 'Problem Library', subtitle: 'Interview challenges with automated test execution' };
    if (path.startsWith('/workspace/')) return { title: '12-Step Problem Workspace', subtitle: 'Structure, plan, code, and diagnose errors' };
    if (path === '/playground') return { title: 'Coding Playground', subtitle: 'Freeform Python 3.12 sandbox & runtime' };
    if (path === '/debug-lab') return { title: 'Debugging Laboratory', subtitle: 'Trace silent failures and fix root causes' };
    if (path === '/mistakes') return { title: 'Mistake Notebook', subtitle: '22-pattern taxonomy & retest verification' };
    if (path === '/revision') return { title: 'Spaced Revision Center', subtitle: 'SM-2 memory retention & interval reviews' };
    if (path === '/settings') return { title: 'Settings & Profiles', subtitle: 'Manage goals & switch multi-user demo accounts' };
    return { title: 'Python & DSA Mastery', subtitle: 'Learn how to think, not just what code to write' };
  };

  const { title, subtitle } = getPageInfo();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col md:flex-row font-sans selection:bg-sky-500/30 selection:text-white">
      {/* Sidebar Navigation */}
      <Sidebar
        dueRevisionsCount={dueRevisionsCount}
        isOpenMobile={mobileNavOpen}
        onCloseMobile={() => setMobileNavOpen(false)}
        onOpenAuth={() => setAuthModalOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col md:pl-64 min-w-0">
        <Header
          title={title}
          subtitle={subtitle}
          onOpenMobileNav={() => setMobileNavOpen(true)}
          onOpenAuth={() => setAuthModalOpen(true)}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/python" element={<PythonAcademy />} />
            <Route path="/logic" element={<LogicGym />} />
            <Route path="/dsa" element={<DSARoadmap />} />
            <Route path="/problems" element={<Problems />} />
            <Route path="/workspace/:problemId" element={<Workspace />} />
            <Route path="/playground" element={<Playground />} />
            <Route path="/debug-lab" element={<DebugLab />} />
            <Route path="/mistakes" element={<MistakeNotebook />} />
            <Route path="/revision" element={<RevisionCenter />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Dashboard />} />
          </Routes>
        </main>
      </div>

      {/* Auth & Profile Switcher Modal */}
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
      />
    </div>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppLayout />
      </AuthProvider>
    </BrowserRouter>
  );
}
