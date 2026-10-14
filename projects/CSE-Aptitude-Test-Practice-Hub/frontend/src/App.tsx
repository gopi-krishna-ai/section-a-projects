import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AuthModal } from './components/auth/AuthModal';
import { Sidebar } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import { Dashboard } from './pages/Dashboard';
import { Learn } from './pages/Learn';
import { Practice } from './pages/Practice';
import { Workspace } from './pages/Workspace';
import { MistakeNotebook } from './pages/MistakeNotebook';
import { Revision } from './pages/Revision';
import { MockTests } from './pages/MockTests';
import { Analytics } from './pages/Analytics';
import { QuestionLibrary } from './pages/QuestionLibrary';
import { Settings } from './pages/Settings';
import { api } from './api/client';

const PAGE_TITLES: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Personalized Learning Dashboard', subtitle: 'Real-time mastery tracking & placement diagnostics' },
  '/learn': { title: 'Concept Teaching & Syllabus', subtitle: 'Understand how methods work and why before applying' },
  '/practice': { title: 'Adaptive Practice Engine', subtitle: 'Targeted topic, guided, independent, and speed modes' },
  '/workspace': { title: 'Question Solving Workspace', subtitle: 'Interactive solver with hints, scratchpad, and AI tutor' },
  '/mistakes': { title: 'Searchable Mistake Notebook', subtitle: 'Root cause diagnoses and retesting workflows' },
  '/revision': { title: 'Spaced Repetition Schedule', subtitle: 'Retrieve concepts at optimal retention intervals' },
  '/mock-tests': { title: 'Placement Mock Test Simulator', subtitle: 'Timed exam mode with sectional scorecards' },
  '/analytics': { title: 'Progress & Analytics', subtitle: 'Mastery estimates, accuracy trends, and error taxonomies' },
  '/library': { title: 'Original Question Bank', subtitle: '1,800 verified questions from repository' },
  '/settings': { title: 'Application Settings', subtitle: 'Preferences, goals, and AI service layer' }
};

const AppContent: React.FC = () => {
  const location = useLocation();
  const { currentUser } = useAuth();
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [dueRevisionsCount, setDueRevisionsCount] = useState(0);

  useEffect(() => {
    api.getDashboard()
      .then((d) => setDueRevisionsCount(d.due_revisions_count))
      .catch(() => {});
  }, [location.pathname, currentUser]);

  const currentMeta = PAGE_TITLES[location.pathname] || {
    title: 'AI Aptitude Mastery Coach',
    subtitle: 'Placement Preparation Platform'
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Persistent Sidebar */}
      <Sidebar
        dueRevisionsCount={dueRevisionsCount}
        isOpenMobile={isMobileNavOpen}
        onCloseMobile={() => setIsMobileNavOpen(false)}
        onOpenAuth={() => setIsAuthModalOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 md:pl-64 flex flex-col min-w-0">
        <Header
          title={currentMeta.title}
          subtitle={currentMeta.subtitle}
          onOpenMobileNav={() => setIsMobileNavOpen(true)}
          onOpenAuth={() => setIsAuthModalOpen(true)}
        />

        <main className="flex-1 pb-16">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/learn" element={<Learn />} />
            <Route path="/practice" element={<Practice />} />
            <Route path="/workspace" element={<Workspace />} />
            <Route path="/mistakes" element={<MistakeNotebook />} />
            <Route path="/revision" element={<Revision />} />
            <Route path="/mock-tests" element={<MockTests />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/library" element={<QuestionLibrary />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>

      {/* User Login & Switcher Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />
    </div>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}
