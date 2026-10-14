import { useState } from "react";
import {
  User, Bell, Brain, Clock, Palette, Shield, Save,
  CheckCircle2, Volume2, Moon, Sun, Smartphone, Monitor,
} from "lucide-react";
import { useTheme, THEMES, ThemeId } from "../context/ThemeContext";
import { useProfile } from "../context/ProfileContext";
import { useAuth } from "../context/AuthContext";

interface ToggleProps {
  value: boolean;
  onChange: (v: boolean) => void;
  color?: string;
}

function Toggle({ value, onChange, color = "#4F8EF7" }: ToggleProps) {
  return (
    <button
      onClick={() => onChange(!value)}
      className="relative inline-flex w-11 h-6 rounded-full transition-all duration-300 flex-shrink-0"
      style={{ background: value ? `linear-gradient(135deg, ${color}, #7B61FF)` : "#cbd5e1" }}
    >
      <span
        className="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-all duration-300 shadow-sm"
        style={{ transform: value ? "translateX(20px)" : "translateX(0)" }}
      />
    </button>
  );
}

export function SettingsPage() {
  const { isDark, toggleDark, themeId, setThemeId, colors, currentTheme } = useTheme();
  const { profile, saveProfile } = useProfile();
  const { user, updateUser } = useAuth();

  // Prefer auth user data over profile defaults
  const [name, setName] = useState(user?.name || profile.name);
  const [email, setEmail] = useState(user?.email || profile.email);
  const [university, setUniversity] = useState(user?.university || profile.university);
  const [dailyGoal, setDailyGoal] = useState(profile.dailyGoal);
  const [notifications, setNotifications] = useState({
    studyReminders: true,
    breakAlerts: true,
    weeklyReport: true,
    achievements: false,
    email: false,
  });
  const [aiSettings, setAiSettings] = useState({
    predictionEnabled: true,
    adaptiveSchedule: true,
    smartSuggestions: true,
    focusMode: false,
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    saveProfile({ name, email, university, dailyGoal });
    updateUser({ name, email, university });
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const cardStyle = {
    background: colors.cardBg,
    border: `1px solid ${colors.cardBorder}`,
    boxShadow: `0 4px 20px ${colors.primary}0d`,
    transition: "background 0.3s ease",
  };

  const labelStyle = { color: colors.textSecondary, fontSize: "0.78rem" as const, fontWeight: 600 as const };
  const textPrimary = { color: colors.textPrimary };

  return (
    <div className="space-y-6 max-w-4xl" style={{ fontFamily: "Poppins, sans-serif" }}>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Column */}
        <div className="space-y-4">
          {/* Profile Card */}
          <div className="rounded-2xl overflow-hidden" style={cardStyle}>
            <div className="p-6 text-center" style={{ background: colors.gradient }}>
              <div className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-3 relative" style={{ background: "rgba(255,255,255,0.2)" }}>
                <User className="w-10 h-10 text-white" />
                <button className="absolute bottom-0 right-0 w-6 h-6 rounded-full bg-white flex items-center justify-center" style={{ boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
                  <span style={{ fontSize: "0.6rem" }}>✏️</span>
                </button>
              </div>
              <p className="text-white" style={{ fontWeight: 700, fontSize: "1rem" }}>{name}</p>
              <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "0.75rem" }}>{email}</p>
              <div className="flex items-center justify-center gap-2 mt-2 px-3 py-1.5 rounded-full mx-auto w-fit" style={{ background: "rgba(255,255,255,0.15)" }}>
                <span style={{ color: "#fff", fontSize: "0.7rem", fontWeight: 600 }}>🎓 Student</span>
              </div>
            </div>
            <div className="p-4 space-y-3">
              {[
                { label: "Institution", value: university || "—" },
                { label: "Study Streak", value: "5 Days 🔥" },
                { label: "Daily Goal", value: `${dailyGoal}h` },
                { label: "Avg Score", value: "78%" },
              ].map((item, i) => (
                <div key={i} className="flex justify-between items-center">
                  <span style={labelStyle}>{item.label}</span>
                  <span style={{ ...textPrimary, fontSize: "0.825rem", fontWeight: 600 }}>{item.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Appearance Card */}
          <div className="rounded-2xl p-5 space-y-5" style={cardStyle}>
            <div className="flex items-center gap-2">
              <Palette className="w-4 h-4" style={{ color: colors.primary }} />
              <span style={{ fontWeight: 600, ...textPrimary, fontSize: "0.875rem" }}>Appearance</span>
            </div>

            {/* Dark Mode Toggle */}
            <div>
              <p style={{ ...labelStyle, marginBottom: "0.5rem", display: "block" }}>Color Mode</p>
              <div className="flex items-center gap-2 p-1 rounded-xl" style={{ background: colors.mutedBg, border: `1px solid ${colors.cardBorder}` }}>
                {[
                  { id: "light", icon: Sun, label: "Light" },
                  { id: "dark", icon: Moon, label: "Dark" },
                  { id: "system", icon: Monitor, label: "System" },
                ].map(({ id, icon: Icon, label }) => {
                  const active = id === "dark" ? isDark : id === "light" ? !isDark : false;
                  return (
                    <button
                      key={id}
                      onClick={() => {
                        if (id === "dark" && !isDark) toggleDark();
                        if (id === "light" && isDark) toggleDark();
                      }}
                      className="flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg transition-all duration-200"
                      style={{
                        background: active ? colors.gradient : "transparent",
                        color: active ? "#fff" : colors.textSecondary,
                        fontSize: "0.75rem",
                        fontWeight: active ? 600 : 400,
                      }}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Color Theme */}
            <div>
              <p style={{ ...labelStyle, marginBottom: "0.5rem", display: "block" }}>Accent Color</p>
              <div className="grid grid-cols-3 gap-2">
                {THEMES.map((t) => {
                  const isSelected = themeId === t.id;
                  return (
                    <button
                      key={t.id}
                      onClick={() => setThemeId(t.id as ThemeId)}
                      className="p-2.5 rounded-xl transition-all duration-200 flex flex-col items-center gap-1.5"
                      style={{
                        background: isSelected ? `linear-gradient(135deg, ${t.primary}20, ${t.secondary}20)` : colors.mutedBg,
                        border: `2px solid ${isSelected ? t.primary : colors.cardBorder}`,
                      }}
                    >
                      <div className="w-5 h-5 rounded-full flex items-center justify-center" style={{ background: `linear-gradient(135deg, ${t.primary}, ${t.secondary})` }}>
                        {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-white" />}
                      </div>
                      <p style={{ color: isSelected ? t.primary : colors.textSecondary, fontSize: "0.65rem", fontWeight: isSelected ? 600 : 400 }}>{t.label}</p>
                    </button>
                  );
                })}
              </div>

              {/* Live Preview Strip */}
              <div className="mt-3 rounded-xl overflow-hidden" style={{ height: 8, background: `linear-gradient(90deg, ${currentTheme.primary}, ${currentTheme.secondary})` }} />
              <p style={{ color: colors.textSecondary, fontSize: "0.68rem", marginTop: "0.35rem", textAlign: "center" }}>
                Preview: {currentTheme.label}
              </p>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-2 space-y-4">
          {/* Profile Settings */}
          <div className="rounded-2xl p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <User className="w-4 h-4" style={{ color: colors.primary }} />
              <span style={{ fontWeight: 600, ...textPrimary, fontSize: "0.875rem" }}>Profile Settings</span>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label style={labelStyle}>Full Name</label>
                <input
                  type="text" value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1.5 w-full px-3 py-2.5 rounded-xl outline-none transition-all"
                  style={{ background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, fontFamily: "Poppins", fontSize: "0.825rem", color: colors.textPrimary }}
                  onFocus={(e) => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                  onBlur={(e) => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                />
              </div>
              <div>
                <label style={labelStyle}>Email</label>
                <input
                  type="email" value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="mt-1.5 w-full px-3 py-2.5 rounded-xl outline-none transition-all"
                  style={{ background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, fontFamily: "Poppins", fontSize: "0.825rem", color: colors.textPrimary }}
                  onFocus={(e) => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                  onBlur={(e) => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                />
              </div>
              <div className="col-span-2">
                <label style={labelStyle}>University / Institution</label>
                <input
                  type="text" value={university}
                  onChange={(e) => setUniversity(e.target.value)}
                  className="mt-1.5 w-full px-3 py-2.5 rounded-xl outline-none transition-all"
                  style={{ background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, fontFamily: "Poppins", fontSize: "0.825rem", color: colors.textPrimary }}
                  onFocus={(e) => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                  onBlur={(e) => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                />
              </div>
              <div className="col-span-2">
                <label style={labelStyle}>
                  Daily Study Goal: <span style={{ color: colors.primary }}>{dailyGoal}h</span>
                </label>
                <div className="flex items-center gap-4 mt-1.5">
                  <input
                    type="range" min={1} max={16} step={0.5} value={dailyGoal}
                    onChange={(e) => setDailyGoal(parseFloat(e.target.value))}
                    className="flex-1 h-2 rounded-full appearance-none cursor-pointer"
                    style={{ accentColor: colors.primary }}
                  />
                  <span className="w-12 text-center py-1.5 rounded-lg" style={{ background: `${colors.primary}18`, color: colors.primary, fontWeight: 700, fontSize: "0.825rem" }}>{dailyGoal}h</span>
                </div>
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="rounded-2xl p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <Bell className="w-4 h-4" style={{ color: "#f59e0b" }} />
              <span style={{ fontWeight: 600, ...textPrimary, fontSize: "0.875rem" }}>Notifications</span>
            </div>
            <div className="space-y-4">
              {[
                { key: "studyReminders" as const, label: "Study Reminders", desc: "Get notified before your study sessions", icon: Clock },
                { key: "breakAlerts" as const, label: "Break Alerts", desc: "Pomodoro-style break notifications", icon: Volume2 },
                { key: "weeklyReport" as const, label: "Weekly Report", desc: "AI-generated weekly performance summary", icon: Brain },
                { key: "achievements" as const, label: "Achievements", desc: "Badges and milestone notifications", icon: Shield },
                { key: "email" as const, label: "Email Notifications", desc: "Receive updates via email", icon: Smartphone },
              ].map(({ key, label, desc, icon: Icon }) => (
                <div key={key} className="flex items-center justify-between">
                  <div className="flex items-start gap-3">
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style={{ background: `${colors.primary}15` }}>
                      <Icon className="w-4 h-4" style={{ color: colors.primary }} />
                    </div>
                    <div>
                      <p style={{ color: colors.textPrimary, fontSize: "0.825rem", fontWeight: 500 }}>{label}</p>
                      <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{desc}</p>
                    </div>
                  </div>
                  <Toggle
                    value={notifications[key]}
                    onChange={(v) => setNotifications(prev => ({ ...prev, [key]: v }))}
                    color={colors.primary}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* AI Settings */}
          <div className="rounded-2xl p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <Brain className="w-4 h-4" style={{ color: colors.secondary }} />
              <span style={{ fontWeight: 600, ...textPrimary, fontSize: "0.875rem" }}>AI & Productivity Settings</span>
            </div>
            <div className="space-y-3">
              {[
                { key: "predictionEnabled" as const, label: "Productivity Prediction", desc: "Enable AI-based daily productivity forecast", color: colors.secondary },
                { key: "adaptiveSchedule" as const, label: "Adaptive Schedule", desc: "AI adjusts your plan based on performance", color: colors.primary },
                { key: "smartSuggestions" as const, label: "Smart Suggestions", desc: "Get personalized study tips from AI", color: "#10b981" },
                { key: "focusMode" as const, label: "Focus Mode", desc: "Block distractions during study sessions", color: "#f59e0b" },
              ].map(({ key, label, desc, color }) => (
                <div
                  key={key}
                  className="flex items-center justify-between p-3 rounded-xl transition-all"
                  style={{ background: aiSettings[key] ? `${color}0d` : colors.mutedBg }}
                >
                  <div>
                    <p style={{ color: colors.textPrimary, fontSize: "0.825rem", fontWeight: 500 }}>{label}</p>
                    <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{desc}</p>
                  </div>
                  <Toggle
                    value={aiSettings[key]}
                    onChange={(v) => setAiSettings(prev => ({ ...prev, [key]: v }))}
                    color={color}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            className="w-full py-3.5 rounded-xl flex items-center justify-center gap-2 transition-all duration-200"
            style={{
              background: saved ? "linear-gradient(135deg, #10b981, #059669)" : colors.gradient,
              color: "#fff",
              fontFamily: "Poppins, sans-serif",
              fontWeight: 600,
              fontSize: "0.9rem",
              boxShadow: saved ? "0 8px 30px rgba(16,185,129,0.3)" : `0 8px 30px ${colors.primary}40`,
            }}
          >
            {saved ? (
              <><CheckCircle2 className="w-5 h-5" /> Settings Saved!</>
            ) : (
              <><Save className="w-5 h-5" /> Save Changes</>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
