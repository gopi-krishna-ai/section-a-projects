import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router";
import {
  Brain, Zap, Clock, CheckCircle2, Plus, TrendingUp, Target,
  Timer, BookOpen, Flame, Star, Play, Pause, RotateCcw, Coffee, Calendar, FileText
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Area, AreaChart
} from "recharts";
import { useTheme } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";
import { useStudyData } from "../context/StudyDataContext";

const FOCUS_SECONDS = 25 * 60;
const BREAK_SECONDS = 5 * 60;

const weeklyData = [
  { day: "Mon", hours: 3.5, productivity: 72 },
  { day: "Tue", hours: 5, productivity: 85 },
  { day: "Wed", hours: 2, productivity: 55 },
  { day: "Thu", hours: 6, productivity: 90 },
  { day: "Fri", hours: 4.5, productivity: 80 },
  { day: "Sat", hours: 7, productivity: 92 },
  { day: "Sun", hours: 3, productivity: 68 },
];

const hourlyProductivity = [
  { time: "6AM", score: 40 }, { time: "8AM", score: 55 }, { time: "10AM", score: 70 },
  { time: "12PM", score: 60 }, { time: "2PM", score: 45 }, { time: "4PM", score: 65 },
  { time: "6PM", score: 92 }, { time: "8PM", score: 88 }, { time: "10PM", score: 70 },
];

const tips = [
  "Take a 5-min break every 25 minutes for better focus.",
  "Review your notes within 24 hours of learning for retention.",
  "Sleep at least 7 hours — it consolidates memory.",
];

function PomodoroTimer({ colors }: { colors: ReturnType<typeof useTheme>["colors"] }) {
  const [mode, setMode] = useState<"focus" | "break">("focus");
  const [timeLeft, setTimeLeft] = useState(FOCUS_SECONDS);
  const [running, setRunning] = useState(false);
  const [sessions, setSessions] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const totalTime = mode === "focus" ? FOCUS_SECONDS : BREAK_SECONDS;
  const progress = ((totalTime - timeLeft) / totalTime) * 100;
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;

  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(intervalRef.current!);
            setRunning(false);
            if (mode === "focus") { setSessions(s => s + 1); setMode("break"); return BREAK_SECONDS; }
            else { setMode("focus"); return FOCUS_SECONDS; }
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
  }, [running, mode]);

  const handleReset = () => { setRunning(false); setTimeLeft(mode === "focus" ? FOCUS_SECONDS : BREAK_SECONDS); };
  const switchMode = (m: "focus" | "break") => { setRunning(false); setMode(m); setTimeLeft(m === "focus" ? FOCUS_SECONDS : BREAK_SECONDS); };

  const R = 42;
  const circ = 2 * Math.PI * R;
  const dashOffset = circ * (1 - progress / 100);
  const mc = mode === "focus" ? colors.primary : "#10b981";
  const mc2 = mode === "focus" ? colors.secondary : "#059669";

  return (
    <div className="flex flex-col items-center gap-3 w-full">
      <div className="flex rounded-xl overflow-hidden w-full" style={{ background: colors.mutedBg }}>
        {(["focus", "break"] as const).map(m => (
          <button key={m} onClick={() => switchMode(m)} className="flex-1 flex items-center justify-center gap-1.5 py-2 text-xs transition-all duration-200" style={{ background: mode === m ? `linear-gradient(135deg, ${mc}, ${mc2})` : "transparent", color: mode === m ? "#fff" : colors.textSecondary, fontFamily: "Inter, sans-serif", fontWeight: 600 }}>
            {m === "focus" ? <Brain className="w-3 h-3" /> : <Coffee className="w-3 h-3" />}
            {m === "focus" ? "Focus" : "Break"}
          </button>
        ))}
      </div>

      <div className="relative w-32 h-32">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r={R} fill="none" stroke={`${mc}20`} strokeWidth="8" />
          <circle cx="50" cy="50" r={R} fill="none" stroke={`url(#timerGrad-${mode})`} strokeWidth="8"
            strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={dashOffset}
            style={{ transition: "stroke-dashoffset 0.8s ease" }}
          />
          <defs>
            <linearGradient id="timerGrad-focus" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop key="tf0" offset="0%" stopColor="#4F8EF7" />
              <stop key="tf1" offset="100%" stopColor="#7B61FF" />
            </linearGradient>
            <linearGradient id="timerGrad-break" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop key="tb0" offset="0%" stopColor="#10b981" />
              <stop key="tb1" offset="100%" stopColor="#059669" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span style={{ fontFamily: "Inter, sans-serif", fontWeight: 800, fontSize: "1.35rem", color: colors.textPrimary, lineHeight: 1 }}>
            {String(mins).padStart(2, "0")}:{String(secs).padStart(2, "0")}
          </span>
          <span style={{ fontFamily: "Inter, sans-serif", fontSize: "0.6rem", color: mc, fontWeight: 600, marginTop: 2 }}>
            {mode === "focus" ? "Focus" : "Break"}
          </span>
          {sessions > 0 && <span style={{ fontFamily: "Inter, sans-serif", fontSize: "0.55rem", color: colors.textSecondary, marginTop: 1 }}>{sessions} 🍅</span>}
        </div>
      </div>

      <div className="flex items-center gap-2 w-full">
        <button onClick={() => setRunning(r => !r)} className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl transition-all duration-200" style={{ background: `linear-gradient(135deg, ${mc}, ${mc2})`, color: "#fff", fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.8rem", boxShadow: `0 4px 15px ${mc}40` }}>
          {running ? <><Pause className="w-3.5 h-3.5" /> Pause</> : <><Play className="w-3.5 h-3.5" /> {timeLeft === totalTime ? "Start" : "Resume"}</>}
        </button>
        <button onClick={handleReset} className="w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-200" style={{ background: colors.mutedBg, color: colors.textSecondary }} title="Reset">
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>

      <p style={{ color: colors.textSecondary, fontSize: "0.68rem", fontFamily: "Inter, sans-serif" }}>
        {sessions === 0 ? "Start your first focus session!" : `${sessions} session${sessions > 1 ? "s" : ""} completed today`}
      </p>
    </div>
  );
}

export function DashboardPage() {
  const navigate = useNavigate();
  const { colors } = useTheme();
  const { user } = useAuth();
  const { tasks, subjects, events, toggleTask } = useStudyData();

  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = user?.name?.split(" ")[0] || "Student";

  const todayStr = new Date().toISOString().split("T")[0];
  const todayTasks = tasks.filter(t => t.deadline === todayStr || t.deadline <= todayStr).slice(0, 4);
  const todayEvents = events.filter(e => e.date === todayStr);
  const completedToday = tasks.filter(t => t.completed).length;
  const totalHours = subjects.reduce((a, s) => a + s.completedHours, 0);
  const overallProgress = subjects.length > 0 ? Math.round((subjects.reduce((a, s) => a + s.completedHours, 0) / subjects.reduce((a, s) => a + s.totalHours, 0)) * 100) : 0;

  const card: React.CSSProperties = { background: colors.cardBg, border: `1px solid ${colors.cardBorder}`, boxShadow: `0 4px 20px ${colors.primary}0d`, transition: "background 0.3s ease" };

  return (
    <div className="space-y-5" style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Row 1: Greeting + Timer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2 rounded-2xl p-6 relative overflow-hidden" style={{ background: "linear-gradient(135deg, #1a1f3e 0%, #2d1b6e 100%)" }}>
          <div className="absolute top-0 right-0 w-48 h-48 rounded-full opacity-10 blur-3xl pointer-events-none" style={{ background: "radial-gradient(circle, #7B61FF, transparent)", transform: "translate(30%, -30%)" }} />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-2">
              <Star className="w-4 h-4" style={{ color: "#f59e0b" }} />
              <span style={{ color: "#f59e0b", fontSize: "0.75rem", fontWeight: 600 }}>
                {new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })}
              </span>
            </div>
            <h2 className="text-white mb-2" style={{ fontWeight: 800, fontSize: "1.4rem" }}>
              {greeting}, {firstName}! 👋
            </h2>
            <p style={{ color: "#94a3b8", fontSize: "0.875rem", lineHeight: 1.65, maxWidth: 400 }}>
              Your AI assistant predicts <span style={{ color: "#7B61FF", fontWeight: 600 }}>82% productivity</span> for you today. Best study window: <span style={{ color: "#4F8EF7", fontWeight: 600 }}>6:30 PM – 8:30 PM</span>.
            </p>
            <div className="flex items-center gap-3 mt-4 flex-wrap">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg" style={{ background: "rgba(251,146,60,0.15)" }}>
                <Flame className="w-4 h-4" style={{ color: "#fb923c" }} />
                <span style={{ color: "#fb923c", fontSize: "0.75rem", fontWeight: 600 }}>5-Day Streak</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg" style={{ background: "rgba(16,185,129,0.15)" }}>
                <CheckCircle2 className="w-4 h-4" style={{ color: "#10b981" }} />
                <span style={{ color: "#10b981", fontSize: "0.75rem", fontWeight: 600 }}>{overallProgress}% Today's Goal</span>
              </div>
              {todayEvents.length > 0 && (
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg" style={{ background: "rgba(79,142,247,0.15)" }}>
                  <Calendar className="w-4 h-4" style={{ color: "#4F8EF7" }} />
                  <span style={{ color: "#4F8EF7", fontSize: "0.75rem", fontWeight: 600 }}>{todayEvents.length} event{todayEvents.length > 1 ? "s" : ""} today</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="rounded-2xl p-5 flex flex-col items-center" style={card}>
          <div className="flex items-center gap-2 mb-3 w-full">
            <Timer className="w-4 h-4" style={{ color: colors.secondary }} />
            <span style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.85rem" }}>Focus Timer</span>
          </div>
          <PomodoroTimer colors={colors} />
        </div>
      </div>

      {/* Row 2: Quick Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Study Hours Today", value: `${totalHours.toFixed(1)}h`, icon: Clock, color: colors.primary, bg: `${colors.primary}15`, change: "+0.5h" },
          { label: "Tasks Completed", value: `${completedToday}/${tasks.length}`, icon: CheckCircle2, color: "#10b981", bg: "#f0fdf4", change: `${tasks.length - completedToday} pending` },
          { label: "Productivity Score", value: "82%", icon: Zap, color: colors.secondary, bg: `${colors.secondary}15`, change: "+7% this week" },
          { label: "Subjects Active", value: `${subjects.length}`, icon: BookOpen, color: "#f59e0b", bg: "#fffbeb", change: "On track" },
        ].map((stat, i) => (
          <div key={i} className="rounded-2xl p-4 transition-all duration-200 hover:-translate-y-0.5 cursor-default" style={card}>
            <div className="flex items-start justify-between mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: stat.bg }}>
                <stat.icon className="w-5 h-5" style={{ color: stat.color }} />
              </div>
              <span style={{ color: "#10b981", fontSize: "0.68rem", fontWeight: 600, background: "#f0fdf4", padding: "2px 8px", borderRadius: 999 }}>{stat.change}</span>
            </div>
            <p style={{ color: colors.textPrimary, fontWeight: 800, fontSize: "1.4rem" }}>{stat.value}</p>
            <p style={{ color: colors.textSecondary, fontSize: "0.73rem", lineHeight: 1.3 }}>{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Row 3: Study Plan + Right Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Subject progress */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "1rem" }}>Today's Study Plan</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.75rem" }}>
                {subjects.filter(s => s.completedHours >= s.totalHours).length}/{subjects.length} subjects completed
              </p>
            </div>
            <button onClick={() => navigate("/app/planner")} className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-200" style={{ background: colors.gradient, color: "#fff", fontWeight: 600, fontSize: "0.8rem" }}>
              <Plus className="w-4 h-4" /> Add Subject
            </button>
          </div>

          <div className="space-y-3">
            {subjects.map((subject) => {
              const progress = Math.min(100, Math.round((subject.completedHours / subject.totalHours) * 100));
              const isDone = subject.completedHours >= subject.totalHours;
              return (
                <div key={subject.id} className="rounded-2xl p-4 transition-all duration-200 hover:shadow-lg" style={{ ...card, border: isDone ? `1.5px solid #10b981` : `1.5px solid ${colors.cardBorder}` }}>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center text-lg" style={{ background: `${subject.color}18` }}>{subject.emoji}</div>
                      <div>
                        <p style={{ fontWeight: 600, color: colors.textPrimary, fontSize: "0.9rem" }}>{subject.name}</p>
                        <div className="flex items-center gap-2">
                          <span style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{subject.completedHours}h / {subject.totalHours}h</span>
                          <span className="px-2 py-0.5 rounded-full" style={{ background: subject.difficulty === "Hard" ? "#fef2f2" : subject.difficulty === "Medium" ? "#fffbeb" : "#f0fdf4", color: subject.difficulty === "Hard" ? "#ef4444" : subject.difficulty === "Medium" ? "#f59e0b" : "#10b981", fontWeight: 600, fontSize: "0.62rem" }}>
                            {subject.difficulty}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span style={{ color: subject.color, fontWeight: 700, fontSize: "0.9rem" }}>{progress}%</span>
                      {isDone ? (
                        <div className="flex items-center gap-1 px-2 py-1 rounded-lg" style={{ background: "#f0fdf4" }}>
                          <CheckCircle2 className="w-3.5 h-3.5" style={{ color: "#10b981" }} />
                          <span style={{ color: "#10b981", fontSize: "0.7rem", fontWeight: 600 }}>Done!</span>
                        </div>
                      ) : (
                        <button onClick={() => navigate("/app/tasks")} className="px-3 py-1.5 rounded-lg text-xs transition-all" style={{ background: subject.color, color: "#fff", fontWeight: 600 }}>Study</button>
                      )}
                    </div>
                  </div>
                  <div className="h-2 rounded-full" style={{ background: colors.mutedBg }}>
                    <div className="h-full rounded-full transition-all duration-700" style={{ width: `${progress}%`, background: isDone ? "#10b981" : `linear-gradient(90deg, ${subject.color}, ${subject.color}99)` }} />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Today's tasks quick view */}
          {todayTasks.length > 0 && (
            <div className="rounded-2xl p-5" style={card}>
              <div className="flex items-center justify-between mb-3">
                <h4 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>Due Today</h4>
                <button onClick={() => navigate("/app/tasks")} style={{ color: colors.primary, fontSize: "0.78rem", fontWeight: 600, background: "none", border: "none", cursor: "pointer" }}>View all →</button>
              </div>
              <div className="space-y-2">
                {todayTasks.map(task => (
                  <div key={task.id} className="flex items-center gap-3 p-2 rounded-xl" style={{ background: colors.mutedBg }}>
                    <button onClick={() => toggleTask(task.id)} className="flex-shrink-0">
                      {task.completed ? <CheckCircle2 className="w-4 h-4" style={{ color: "#10b981" }} /> : <div className="w-4 h-4 rounded-full border-2" style={{ borderColor: "#cbd5e0" }} />}
                    </button>
                    <span style={{ flex: 1, color: task.completed ? colors.textSecondary : colors.textPrimary, fontSize: "0.82rem", textDecoration: task.completed ? "line-through" : "none" }}>{task.title}</span>
                    <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: task.subjectColor }} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Panel */}
        <div className="space-y-4">
          {/* AI Prediction */}
          <div className="rounded-2xl p-5 relative overflow-hidden" style={{ background: colors.gradient, boxShadow: `0 8px 30px ${colors.primary}40` }}>
            <div className="absolute top-0 right-0 w-24 h-24 rounded-full opacity-20 pointer-events-none" style={{ background: "radial-gradient(circle, #fff, transparent)", transform: "translate(20%, -20%)" }} />
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <Brain className="w-5 h-5 text-white" />
                <span style={{ color: "#fff", fontWeight: 600, fontSize: "0.8rem" }}>AI Prediction</span>
              </div>
              <div className="flex items-center gap-4 mb-4">
                <div className="relative w-20 h-20">
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 80 80">
                    <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="6" />
                    <circle cx="40" cy="40" r="32" fill="none" stroke="#fff" strokeWidth="6" strokeLinecap="round"
                      strokeDasharray={`${2 * Math.PI * 32}`} strokeDashoffset={`${2 * Math.PI * 32 * 0.18}`} />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span style={{ color: "#fff", fontWeight: 800, fontSize: "1rem" }}>82%</span>
                  </div>
                </div>
                <div>
                  <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "0.7rem" }}>Today's Score</p>
                  <p style={{ color: "#fff", fontWeight: 700, fontSize: "0.95rem" }}>HIGH</p>
                  <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "0.65rem" }}>Productivity</p>
                </div>
              </div>
              {[
                { icon: Clock, label: "Best Study Time", value: "6:30 PM – 8:30 PM" },
                { icon: TrendingUp, label: "Focus Trend", value: "↑ Improving (+7%)" },
              ].map(({ icon: Icon, label, value }) => (
                <div key={label} className="flex items-center gap-2 p-2 rounded-xl mb-2" style={{ background: "rgba(255,255,255,0.1)" }}>
                  <Icon className="w-3.5 h-3.5 text-white" />
                  <div>
                    <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "0.65rem" }}>{label}</p>
                    <p style={{ color: "#fff", fontWeight: 600, fontSize: "0.75rem" }}>{value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Today's events */}
          {todayEvents.length > 0 && (
            <div className="rounded-2xl p-4" style={card}>
              <div className="flex items-center gap-2 mb-3">
                <Calendar className="w-4 h-4" style={{ color: colors.primary }} />
                <span style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.8rem" }}>Today's Events</span>
              </div>
              <div className="space-y-2">
                {todayEvents.map(ev => (
                  <div key={ev.id} className="flex items-start gap-2 p-2 rounded-xl" style={{ background: colors.mutedBg }}>
                    <div className="w-2 h-2 rounded-full flex-shrink-0 mt-1.5" style={{ background: ev.color }} />
                    <div>
                      <p style={{ fontWeight: 500, color: colors.textPrimary, fontSize: "0.78rem" }}>{ev.title}</p>
                      <p style={{ color: colors.textSecondary, fontSize: "0.67rem" }}>{ev.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tip */}
          <div className="rounded-2xl p-4" style={card}>
            <div className="flex items-center gap-2 mb-2">
              <div className="w-6 h-6 rounded-lg flex items-center justify-center" style={{ background: "#fff3e0" }}>
                <Star className="w-3.5 h-3.5" style={{ color: "#f59e0b" }} />
              </div>
              <span style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.8rem" }}>Productivity Tip</span>
            </div>
            <p style={{ color: colors.textSecondary, fontSize: "0.78rem", lineHeight: 1.6 }}>
              💡 {tips[new Date().getDay() % tips.length]}
            </p>
          </div>

          {/* Daily Goal */}
          <div className="rounded-2xl p-4" style={card}>
            <div className="flex items-center gap-2 mb-3">
              <Target className="w-4 h-4" style={{ color: colors.secondary }} />
              <span style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.8rem" }}>Daily Goal</span>
            </div>
            <div className="flex items-end gap-2 mb-2">
              <span style={{ fontWeight: 800, fontSize: "1.5rem", color: colors.textPrimary }}>{overallProgress}%</span>
              <span style={{ color: colors.textSecondary, fontSize: "0.75rem", marginBottom: 4 }}>completed</span>
            </div>
            <div className="h-3 rounded-full" style={{ background: colors.mutedBg }}>
              <div className="h-full rounded-full transition-all duration-700" style={{ width: `${overallProgress}%`, background: colors.gradient }} />
            </div>
            <p className="mt-2" style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>
              {overallProgress < 100 ? `${100 - overallProgress}% more to complete today's goal!` : "🎉 Daily goal achieved!"}
            </p>
          </div>
        </div>
      </div>

      {/* Row 4: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="rounded-2xl p-5" style={card}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Weekly Study Hours</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>This week's distribution</p>
            </div>
            <div className="px-3 py-1 rounded-lg" style={{ background: `${colors.primary}18` }}>
              <span style={{ color: colors.primary, fontSize: "0.7rem", fontWeight: 600 }}>This Week</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={weeklyData} barSize={28}>
              <defs>
                <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop key="bg0" offset="0%" stopColor={colors.secondary} />
                  <stop key="bg1" offset="100%" stopColor={colors.primary} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="day" tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "none", boxShadow: "0 8px 30px rgba(0,0,0,0.1)", fontFamily: "Inter", fontSize: 12, background: colors.cardBg }} />
              <Bar dataKey="hours" name="Hours" fill="url(#barGrad)" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-2xl p-5" style={card}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Hourly Productivity</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Your focus throughout the day</p>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg" style={{ background: `${colors.secondary}18` }}>
              <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: colors.secondary }} />
              <span style={{ color: colors.secondary, fontSize: "0.7rem", fontWeight: 600 }}>Live</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={hourlyProductivity}>
              <defs>
                <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop key="ag0" offset="5%" stopColor={colors.secondary} stopOpacity={0.3} />
                  <stop key="ag1" offset="95%" stopColor={colors.secondary} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="time" tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} axisLine={false} tickLine={false} domain={[0, 100]} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "none", boxShadow: "0 8px 30px rgba(0,0,0,0.1)", fontFamily: "Inter", fontSize: 12, background: colors.cardBg }} />
              <Area type="monotone" dataKey="score" name="Score" stroke={colors.secondary} strokeWidth={2.5} fill="url(#areaGrad)" dot={{ fill: colors.secondary, strokeWidth: 0, r: 3 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
