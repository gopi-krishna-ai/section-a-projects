import { useState } from "react";
import { Bell, Moon, Sun, Search, User } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useProfile } from "../context/ProfileContext";
import { useAuth } from "../context/AuthContext";

interface TopNavProps {
  title: string;
  subtitle?: string;
}

export function TopNav({ title, subtitle }: TopNavProps) {
  const { isDark, toggleDark, colors } = useTheme();
  const { profile } = useProfile();
  const { user } = useAuth();
  const [notifOpen, setNotifOpen] = useState(false);
  const displayName = user?.name?.split(" ")[0] || profile.name.split(" ")[0];

  const notifications = [
    { text: "Time to study Mathematics!", time: "5 min ago", color: colors.primary },
    { text: "Daily goal: 4 hours remaining", time: "1 hr ago", color: colors.secondary },
    { text: "Great job! You hit 80% productivity", time: "3 hrs ago", color: "#10b981" },
  ];

  return (
    <header
      className="fixed top-0 right-0 z-30 h-16 flex items-center justify-between px-6"
      style={{
        left: 256,
        background: colors.topNavBg,
        backdropFilter: "blur(10px)",
        borderBottom: `1px solid ${colors.primary}18`,
        transition: "background 0.3s ease",
      }}
    >
      {/* Title */}
      <div>
        <h1 style={{ fontFamily: "Poppins, sans-serif", fontWeight: 700, fontSize: "1.1rem", color: colors.textPrimary, lineHeight: 1.2 }}>
          {title}
        </h1>
        {subtitle && (
          <p style={{ fontFamily: "Poppins, sans-serif", fontSize: "0.75rem", color: colors.textSecondary, lineHeight: 1 }}>
            {subtitle}
          </p>
        )}
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div
          className="hidden md:flex items-center gap-2 px-3 py-2 rounded-xl"
          style={{ background: colors.mutedBg, border: `1px solid ${colors.primary}22` }}
        >
          <Search className="w-4 h-4" style={{ color: colors.textSecondary }} />
          <input
            type="text"
            placeholder="Search subjects..."
            className="bg-transparent outline-none text-sm w-32"
            style={{ fontFamily: "Poppins, sans-serif", color: colors.textPrimary }}
          />
        </div>

        {/* Dark Mode Toggle */}
        <button
          onClick={toggleDark}
          className="w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200"
          style={{ background: colors.mutedBg, border: `1px solid ${colors.primary}22` }}
          title={isDark ? "Switch to light mode" : "Switch to dark mode"}
        >
          {isDark ? (
            <Sun className="w-4 h-4" style={{ color: "#f59e0b" }} />
          ) : (
            <Moon className="w-4 h-4" style={{ color: colors.secondary }} />
          )}
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setNotifOpen(!notifOpen)}
            className="w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 relative"
            style={{ background: colors.mutedBg, border: `1px solid ${colors.primary}22` }}
          >
            <Bell className="w-4 h-4" style={{ color: colors.primary }} />
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full flex items-center justify-center text-white" style={{ background: "#ef4444", fontSize: "0.6rem", fontFamily: "Poppins, sans-serif", fontWeight: 700 }}>3</span>
          </button>

          {notifOpen && (
            <div
              className="absolute right-0 top-12 w-72 rounded-2xl shadow-2xl z-50 overflow-hidden"
              style={{ background: colors.cardBg, border: `1px solid ${colors.cardBorder}` }}
            >
              <div className="px-4 py-3 border-b" style={{ borderColor: colors.cardBorder }}>
                <p style={{ fontFamily: "Poppins, sans-serif", fontWeight: 600, fontSize: "0.875rem", color: colors.textPrimary }}>Notifications</p>
              </div>
              {notifications.map((n, i) => (
                <div
                  key={i}
                  className="px-4 py-3 transition-colors cursor-pointer flex items-start gap-3"
                  style={{ borderBottom: i < 2 ? `1px solid ${colors.cardBorder}` : "none" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = `${colors.primary}10`; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}
                >
                  <div className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0" style={{ background: n.color }} />
                  <div>
                    <p style={{ fontFamily: "Poppins, sans-serif", fontSize: "0.8rem", color: colors.textPrimary, fontWeight: 500 }}>{n.text}</p>
                    <p style={{ fontFamily: "Poppins, sans-serif", fontSize: "0.7rem", color: colors.textSecondary }}>{n.time}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Profile */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-xl cursor-pointer transition-all duration-200" style={{ background: colors.gradient }}>
          <div className="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
          <span style={{ fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.8rem", color: "#fff" }}>
            {displayName}
          </span>
        </div>
      </div>
    </header>
  );
}
