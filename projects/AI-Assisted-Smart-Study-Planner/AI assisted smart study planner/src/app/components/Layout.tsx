import { Outlet, useLocation } from "react-router";
import { Sidebar } from "./Sidebar";
import { TopNav } from "./TopNav";
import { useTheme } from "../context/ThemeContext";

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  "/app": { title: "Dashboard", subtitle: "Welcome back! Let's crush your goals today." },
  "/app/dashboard": { title: "Dashboard", subtitle: "Welcome back! Let's crush your goals today." },
  "/app/planner": { title: "Study Planner", subtitle: "Manage your subjects and study plans." },
  "/app/tasks": { title: "Task Tracker", subtitle: "Track your tasks and stay on top of deadlines." },
  "/app/calendar": { title: "Calendar", subtitle: "View your schedule, exams, and deadlines." },
  "/app/notes": { title: "Notes", subtitle: "Capture and organize your study notes." },
  "/app/pomodoro": { title: "Focus Timer", subtitle: "Boost productivity with timed study sessions." },
  "/app/analytics": { title: "Analytics", subtitle: "Deep dive into your study performance." },
  "/app/settings": { title: "Settings", subtitle: "Customize your study experience." },
};

export function Layout() {
  const location = useLocation();
  const page = pageTitles[location.pathname] || { title: "StudyAI", subtitle: "" };
  const { colors } = useTheme();

  return (
    <div className="min-h-screen" style={{ background: colors.pageBg, fontFamily: "Poppins, sans-serif", transition: "background 0.3s ease" }}>
      <Sidebar />
      <TopNav title={page.title} subtitle={page.subtitle} />
      <main className="pt-16" style={{ marginLeft: 256 }}>
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
