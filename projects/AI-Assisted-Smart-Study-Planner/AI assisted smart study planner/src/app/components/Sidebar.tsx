import { NavLink, useLocation } from "react-router";
import {
  LayoutDashboard, BookOpen, CheckSquare, BarChart3,
  Settings, Brain, Zap, LogOut, Flame, Calendar, FileText, Timer, GraduationCap
} from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";
import { useStudyData } from "../context/StudyDataContext";

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/app/dashboard" },
  { icon: BookOpen, label: "Planner", path: "/app/planner" },
  { icon: CheckSquare, label: "Tasks", path: "/app/tasks" },
  { icon: Calendar, label: "Calendar", path: "/app/calendar" },
  { icon: FileText, label: "Notes", path: "/app/notes" },
  { icon: Timer, label: "Pomodoro", path: "/app/pomodoro" },
  { icon: GraduationCap, label: "AI Quiz", path: "/app/quiz" },
  { icon: Brain, label: "AI Assistant", path: "/app/ai-assistant" },
  { icon: BarChart3, label: "Analytics", path: "/app/analytics" },
  { icon: Settings, label: "Settings", path: "/app/settings" },
];

export function Sidebar() {
  const location = useLocation();
  const { colors } = useTheme();
  const { user, logout } = useAuth();
  const { tasks } = useStudyData();
  const pendingCount = tasks.filter(t => !t.completed).length;

  return (
    <aside className="fixed left-0 top-0 h-full w-64 z-40 flex flex-col" style={{ background: colors.navBg, transition: "background 0.3s ease" }}>
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-white/10">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0" style={{ background: colors.gradient }}>
          <Brain className="w-5 h-5 text-white" />
        </div>
        <div>
          <p className="text-white" style={{ fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: "0.95rem" }}>StudyAI</p>
          <p style={{ color: "#64748b", fontFamily: "Inter, sans-serif", fontSize: "0.7rem" }}>Smart Planner</p>
        </div>
      </div>

      {/* User pill */}
      {user && (
        <div className="mx-4 mt-3 px-3 py-2.5 rounded-xl flex items-center gap-2.5" style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}>
          <div className="w-7 h-7 rounded-full flex items-center justify-center text-white flex-shrink-0" style={{ background: colors.gradient, fontSize: "0.7rem", fontWeight: 700 }}>
            {user.name.charAt(0).toUpperCase()}
          </div>
          <div className="min-w-0">
            <p style={{ color: "#f1f5f9", fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.78rem", lineHeight: 1.2, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{user.name}</p>
            <p style={{ color: "#64748b", fontFamily: "Inter, sans-serif", fontSize: "0.65rem", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{user.email}</p>
          </div>
        </div>
      )}

      {/* Streak */}
      <div className="mx-4 mt-3 mb-1 rounded-xl px-3 py-2.5 flex items-center gap-2.5" style={{ background: "linear-gradient(135deg, rgba(251,146,60,0.15), rgba(251,146,60,0.05))", border: "1px solid rgba(251,146,60,0.25)" }}>
        <Flame className="w-4 h-4 flex-shrink-0" style={{ color: "#fb923c" }} />
        <div>
          <p style={{ color: "#fb923c", fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.75rem" }}>5-Day Streak 🔥</p>
          <p style={{ color: "#64748b", fontFamily: "Inter, sans-serif", fontSize: "0.65rem" }}>Keep it going!</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-3 space-y-0.5 overflow-y-auto">
        {navItems.map(({ icon: Icon, label, path }) => {
          const isActive = location.pathname === path || (path === "/app/dashboard" && location.pathname === "/app");
          const isTasks = path === "/app/tasks";
          return (
            <NavLink
              key={path}
              to={path}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-150 group"
              style={{ background: isActive ? colors.gradient : "transparent", color: isActive ? "#fff" : "#64748b" }}
              onMouseEnter={(e) => { if (!isActive) { (e.currentTarget as HTMLElement).style.background = "rgba(255,255,255,0.06)"; (e.currentTarget as HTMLElement).style.color = "#cbd5e1"; } }}
              onMouseLeave={(e) => { if (!isActive) { (e.currentTarget as HTMLElement).style.background = "transparent"; (e.currentTarget as HTMLElement).style.color = "#64748b"; } }}
            >
              <Icon className="w-4.5 h-4.5 flex-shrink-0 w-[18px] h-[18px]" />
              <span style={{ fontFamily: "Inter, sans-serif", fontWeight: isActive ? 600 : 400, fontSize: "0.85rem", flex: 1 }}>{label}</span>
              {isTasks && pendingCount > 0 && (
                <span className="flex-shrink-0 min-w-[18px] h-[18px] rounded-full flex items-center justify-center px-1" style={{ background: isActive ? "rgba(255,255,255,0.3)" : `${colors.primary}30`, color: isActive ? "#fff" : colors.primary, fontSize: "0.6rem", fontWeight: 700 }}>
                  {pendingCount}
                </span>
              )}
              {isActive && !isTasks && <div className="w-1.5 h-1.5 rounded-full bg-white flex-shrink-0" />}
            </NavLink>
          );
        })}
      </nav>

      {/* AI tip */}
      <div className="mx-3 mb-3 rounded-xl px-3 py-3" style={{ background: `linear-gradient(135deg, ${colors.primary}18, ${colors.secondary}18)`, border: `1px solid ${colors.primary}28` }}>
        <div className="flex items-center gap-1.5 mb-1">
          <Zap className="w-3.5 h-3.5" style={{ color: colors.primary }} />
          <span style={{ color: colors.primary, fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.7rem" }}>AI Insight</span>
        </div>
        <p style={{ color: "#94a3b8", fontFamily: "Inter, sans-serif", fontSize: "0.66rem", lineHeight: 1.5 }}>
          Peak focus: <span style={{ color: colors.secondary, fontWeight: 600 }}>6–9 PM</span> today.
        </p>
      </div>

      {/* Logout */}
      <div className="px-3 pb-4 border-t border-white/10 pt-3">
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-150"
          style={{ color: "#64748b" }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "rgba(239,68,68,0.1)"; (e.currentTarget as HTMLElement).style.color = "#ef4444"; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; (e.currentTarget as HTMLElement).style.color = "#64748b"; }}
        >
          <LogOut className="w-[18px] h-[18px]" />
          <span style={{ fontFamily: "Inter, sans-serif", fontSize: "0.85rem" }}>Log out</span>
        </button>
      </div>
    </aside>
  );
}
