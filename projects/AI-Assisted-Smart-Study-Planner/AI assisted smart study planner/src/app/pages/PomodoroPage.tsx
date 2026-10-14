import { useState, useEffect, useRef } from "react";
import { Play, Pause, RotateCcw, Brain, Coffee, Settings2, BarChart2 } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

type Mode = "focus" | "short" | "long";

const DEFAULTS = { focus: 25 * 60, short: 5 * 60, long: 15 * 60 };
const MODE_LABELS = { focus: "Focus", short: "Short Break", long: "Long Break" };
const MODE_COLORS: Record<Mode, { a: string; b: string }> = {
  focus: { a: "#4F8EF7", b: "#7B61FF" },
  short: { a: "#10b981", b: "#059669" },
  long: { a: "#f59e0b", b: "#d97706" },
};

const historyData = [
  { day: "Mon", sessions: 4 }, { day: "Tue", sessions: 6 },
  { day: "Wed", sessions: 3 }, { day: "Thu", sessions: 7 },
  { day: "Fri", sessions: 5 }, { day: "Sat", sessions: 8 }, { day: "Sun", sessions: 4 },
];

export function PomodoroPage() {
  const { colors } = useTheme();
  const [mode, setMode] = useState<Mode>("focus");
  const [timeLeft, setTimeLeft] = useState(DEFAULTS.focus);
  const [running, setRunning] = useState(false);
  const [sessions, setSessions] = useState(0);
  const [totalToday, setTotalToday] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [customTimes, setCustomTimes] = useState({ focus: 25, short: 5, long: 15 });
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const totalTime = customTimes[mode] * 60;
  const progress = ((totalTime - timeLeft) / totalTime) * 100;
  const mins = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const c = MODE_COLORS[mode];
  const R = 54;
  const circ = 2 * Math.PI * R;
  const dashOffset = circ * (1 - progress / 100);

  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => {
        setTimeLeft(p => {
          if (p <= 1) {
            clearInterval(intervalRef.current!);
            setRunning(false);
            if (mode === "focus") { setSessions(s => s + 1); setTotalToday(t => t + customTimes.focus); }
            return totalTime;
          }
          return p - 1;
        });
      }, 1000);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
  }, [running, mode, totalTime, customTimes]);

  const switchMode = (m: Mode) => { setRunning(false); setMode(m); setTimeLeft(customTimes[m] * 60); };
  const reset = () => { setRunning(false); setTimeLeft(customTimes[mode] * 60); };

  const card: React.CSSProperties = { background: colors.cardBg, border: `1px solid ${colors.cardBorder}`, borderRadius: 16 };

  return (
    <div className="max-w-4xl mx-auto space-y-5" style={{ fontFamily: "Inter, sans-serif" }}>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Timer */}
        <div className="lg:col-span-2 p-8" style={card}>
          {/* Mode tabs */}
          <div className="flex rounded-xl p-1 mb-8" style={{ background: colors.mutedBg }}>
            {(Object.keys(DEFAULTS) as Mode[]).map(m => (
              <button key={m} onClick={() => switchMode(m)} className="flex-1 py-2.5 rounded-lg text-sm transition-all duration-200" style={{ background: mode === m ? `linear-gradient(135deg, ${c.a}, ${c.b})` : "transparent", color: mode === m ? "#fff" : colors.textSecondary, fontWeight: mode === m ? 600 : 400 }}>
                {MODE_LABELS[m]}
              </button>
            ))}
          </div>

          {/* Circle */}
          <div className="flex flex-col items-center">
            <div className="relative w-52 h-52 mb-8">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r={R} fill="none" stroke={`${c.a}20`} strokeWidth="8" />
                <circle cx="60" cy="60" r={R} fill="none" stroke={`url(#pomGrad-${mode})`} strokeWidth="8"
                  strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={dashOffset}
                  style={{ transition: "stroke-dashoffset 0.7s ease" }}
                />
                <defs>
                  <linearGradient id={`pomGrad-${mode}`} x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop key="s0" offset="0%" stopColor={c.a} />
                    <stop key="s1" offset="100%" stopColor={c.b} />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span style={{ fontFamily: "Inter, sans-serif", fontWeight: 800, fontSize: "3rem", color: colors.textPrimary, lineHeight: 1, letterSpacing: "-0.02em" }}>
                  {String(mins).padStart(2, "0")}:{String(secs).padStart(2, "0")}
                </span>
                <span style={{ color: c.a, fontSize: "0.75rem", fontWeight: 600, marginTop: 4 }}>{MODE_LABELS[mode]}</span>
                {sessions > 0 && <span style={{ color: colors.textSecondary, fontSize: "0.68rem", marginTop: 2 }}>{sessions} 🍅 today</span>}
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-4">
              <button onClick={reset} className="w-12 h-12 rounded-2xl flex items-center justify-center transition-all" style={{ background: colors.mutedBg, color: colors.textSecondary }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = colors.inputBg; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = colors.mutedBg; }}
              >
                <RotateCcw className="w-5 h-5" />
              </button>
              <button onClick={() => setRunning(r => !r)} className="w-20 h-20 rounded-3xl flex items-center justify-center transition-all" style={{ background: `linear-gradient(135deg, ${c.a}, ${c.b})`, boxShadow: `0 8px 30px ${c.a}40`, color: "#fff" }}>
                {running ? <Pause className="w-8 h-8" /> : <Play className="w-8 h-8 ml-1" />}
              </button>
              <button onClick={() => setShowSettings(!showSettings)} className="w-12 h-12 rounded-2xl flex items-center justify-center transition-all" style={{ background: colors.mutedBg, color: colors.textSecondary }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = colors.inputBg; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = colors.mutedBg; }}
              >
                <Settings2 className="w-5 h-5" />
              </button>
            </div>

            <p className="mt-5" style={{ color: colors.textSecondary, fontSize: "0.82rem" }}>
              {!running && timeLeft === totalTime ? `Click play to start your ${MODE_LABELS[mode].toLowerCase()} session` : running ? "Stay focused! You're doing great." : "Paused — click play to resume"}
            </p>
          </div>

          {/* Custom times */}
          {showSettings && (
            <div className="mt-6 p-4 rounded-xl" style={{ background: colors.mutedBg, border: `1px solid ${colors.cardBorder}` }}>
              <p style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.85rem", marginBottom: 12 }}>Custom Durations</p>
              <div className="grid grid-cols-3 gap-4">
                {(["focus", "short", "long"] as Mode[]).map(m => (
                  <div key={m}>
                    <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 4 }}>{MODE_LABELS[m]} (min)</label>
                    <input type="number" min={1} max={90} value={customTimes[m]} onChange={e => { const v = parseInt(e.target.value); if (!isNaN(v) && v > 0) { setCustomTimes(p => ({ ...p, [m]: v })); if (mode === m) { setRunning(false); setTimeLeft(v * 60); } } }}
                      style={{ width: "100%", padding: "0.5rem 0.75rem", borderRadius: "0.6rem", background: colors.cardBg, border: `1.5px solid ${colors.inputBorder}`, color: colors.textPrimary, fontFamily: "Inter, sans-serif", fontSize: "0.875rem", outline: "none", boxSizing: "border-box" }}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Stats sidebar */}
        <div className="space-y-4">
          <div className="p-5" style={card}>
            <div className="flex items-center gap-2 mb-4">
              <BarChart2 className="w-4 h-4" style={{ color: colors.primary }} />
              <p style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>Today's Stats</p>
            </div>
            {[
              { label: "Sessions completed", value: `${sessions} 🍅`, color: c.a },
              { label: "Focus time", value: `${totalToday} min`, color: "#10b981" },
              { label: "Best streak", value: "3 sessions", color: "#f59e0b" },
            ].map(({ label, value, color }) => (
              <div key={label} className="flex items-center justify-between py-2.5 border-b last:border-0" style={{ borderColor: colors.cardBorder }}>
                <span style={{ color: colors.textSecondary, fontSize: "0.82rem" }}>{label}</span>
                <span style={{ color, fontWeight: 700, fontSize: "0.9rem" }}>{value}</span>
              </div>
            ))}
          </div>

          {/* Weekly chart */}
          <div className="p-5" style={card}>
            <div className="flex items-center gap-2 mb-4">
              <Brain className="w-4 h-4" style={{ color: colors.secondary }} />
              <p style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>This Week</p>
            </div>
            <div className="flex items-end justify-between gap-1.5 h-24">
              {historyData.map(({ day, sessions: s }) => (
                <div key={day} className="flex flex-col items-center gap-1 flex-1">
                  <div className="w-full rounded-t-lg flex-1 flex flex-col justify-end" style={{ background: `${colors.primary}18` }}>
                    <div className="w-full rounded-t-lg transition-all duration-500" style={{ height: `${(s / 8) * 100}%`, background: `linear-gradient(180deg, ${colors.primary}, ${colors.secondary})`, minHeight: 4 }} />
                  </div>
                  <span style={{ color: colors.textSecondary, fontSize: "0.62rem" }}>{day}</span>
                  <span style={{ color: colors.primary, fontSize: "0.62rem", fontWeight: 600 }}>{s}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tips */}
          <div className="p-5" style={card}>
            <div className="flex items-center gap-2 mb-3">
              <Coffee className="w-4 h-4" style={{ color: "#f59e0b" }} />
              <p style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>Focus Tips</p>
            </div>
            <ul className="space-y-2.5 list-none p-0 m-0">
              {["Silence your phone notifications", "Work on one task at a time", "Take your breaks — don't skip them", "Hydrate between sessions"].map((tip, i) => (
                <li key={i} className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ background: colors.primary }} />
                  <span style={{ color: colors.textSecondary, fontSize: "0.8rem", lineHeight: 1.5 }}>{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
