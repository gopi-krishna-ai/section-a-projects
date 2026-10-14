import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, AreaChart, Area, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, Legend
} from "recharts";
import { Brain, TrendingUp, Award, Zap, BarChart3, Target } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useStudyData } from "../context/StudyDataContext";

// ---------- Dynamic data generators ----------

function getLast7DaysData() {
  const today = new Date();
  const scores = [65, 72, 68, 78, 75, 85, 82, 79, 71, 88, 84, 76];
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() - (6 - i));
    const dateStr = d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    const score = scores[(d.getDate() + d.getMonth()) % scores.length];
    return { date: dateStr, score, target: 80 };
  });
}

function getLastWeekData() {
  const today = new Date();
  const scores = [60, 68, 74, 71, 80, 77, 65];
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() - (13 - i));
    const dateStr = d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
    const score = scores[(d.getDate() + d.getMonth() + 3) % scores.length];
    return { date: dateStr, score, target: 80 };
  });
}

function getLast4MonthsHours() {
  const today = new Date();
  const hoursValues = [85, 92, 78, 105, 98, 88, 110, 102, 95, 118, 87, 93];
  return Array.from({ length: 4 }, (_, i) => {
    const d = new Date(today.getFullYear(), today.getMonth() - (3 - i), 1);
    const month = d.toLocaleDateString("en-US", { month: "short" });
    const hours = hoursValues[(d.getMonth()) % hoursValues.length];
    return { month, hours, goal: 100 };
  });
}

function getCurrentAndLastWeekStudy() {
  const today = new Date();
  const monthName = today.toLocaleDateString("en-US", { month: "short" });
  const prevMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1).toLocaleDateString("en-US", { month: "short" });
  return [
    { week: `${prevMonth} W3`, comp: 15, bee: 12, ds: 18, ai: 8, py: 10 },
    { week: `${prevMonth} W4`, comp: 18, bee: 10, ds: 20, ai: 10, py: 12 },
    { week: `${monthName} W1`, comp: 22, bee: 14, ds: 16, ai: 12, py: 9 },
    { week: `${monthName} W2`, comp: 25, bee: 16, ds: 22, ai: 9, py: 14 },
  ];
}

const radarData = [
  { metric: "Focus", score: 82 },
  { metric: "Consistency", score: 75 },
  { metric: "Retention", score: 88 },
  { metric: "Speed", score: 70 },
  { metric: "Accuracy", score: 90 },
  { metric: "Time Mgmt", score: 78 },
];

const hourlyPattern = [
  { hour: "6AM", mon: 40, tue: 50, wed: 35, thu: 60, fri: 55, sat: 70, sun: 45 },
  { hour: "8AM", mon: 65, tue: 70, wed: 60, thu: 75, fri: 68, sat: 80, sun: 55 },
  { hour: "10AM", mon: 78, tue: 80, wed: 72, thu: 85, fri: 75, sat: 82, sun: 60 },
  { hour: "12PM", mon: 55, tue: 60, wed: 50, thu: 65, fri: 58, sat: 72, sun: 48 },
  { hour: "2PM", mon: 45, tue: 50, wed: 42, thu: 55, fri: 48, sat: 65, sun: 40 },
  { hour: "4PM", mon: 70, tue: 75, wed: 68, thu: 80, fri: 72, sat: 78, sun: 62 },
  { hour: "6PM", mon: 88, tue: 90, wed: 85, thu: 92, fri: 88, sat: 85, sun: 78 },
  { hour: "8PM", mon: 85, tue: 88, wed: 82, thu: 90, fri: 85, sat: 80, sun: 75 },
  { hour: "10PM", mon: 68, tue: 72, wed: 65, thu: 75, fri: 70, sat: 68, sun: 60 },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ background: "#1a1f3e", borderRadius: 12, padding: "10px 14px", boxShadow: "0 8px 30px rgba(0,0,0,0.2)" }}>
        <p style={{ color: "#94a3b8", fontSize: "0.75rem", marginBottom: 4, fontFamily: "Inter" }}>{label}</p>
        {payload.map((entry: any, i: number) => (
          <p key={i} style={{ color: entry.color, fontSize: "0.8rem", fontFamily: "Inter", fontWeight: 600 }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export function AnalyticsPage() {
  const { colors } = useTheme();
  const { subjects } = useStudyData();

  const productivityTrend = getLast7DaysData();
  const lastWeekTrend = getLastWeekData();
  const monthlyHours = getLast4MonthsHours();
  const weeklyStudy = getCurrentAndLastWeekStudy();

  const now = new Date();
  const reportDate = now.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });

  const subjectPerformance = subjects.map((s, i) => {
    const scores = [78, 85, 92, 70, 80, 75, 88];
    return { subject: s.name.split(" ")[0], fullName: s.name, score: scores[i % scores.length], color: s.color };
  });

  const totalCompletedHours = subjects.reduce((a, s) => a + s.completedHours, 0);
  const bestSubject = subjects.reduce((best, s) => (s.completedHours / s.totalHours > (best?.completedHours / best?.totalHours || 0) ? s : best), subjects[0]);
  const weakestSubject = subjects.reduce((weak, s) => (s.completedHours / s.totalHours < (weak?.completedHours / weak?.totalHours || 1) ? s : weak), subjects[0]);

  const card = {
    background: colors.cardBg,
    border: `1px solid ${colors.cardBorder}`,
    boxShadow: `0 4px 20px ${colors.primary}0d`,
  };

  return (
    <div className="space-y-6" style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Avg Productivity", value: "78%", change: "+12% this month", icon: Zap, color: colors.secondary, bg: `${colors.secondary}15`, trend: "up" },
          { label: "Total Study Hrs", value: `${Math.round(totalCompletedHours * 10)}h`, change: "+45h vs last month", icon: BarChart3, color: colors.primary, bg: `${colors.primary}15`, trend: "up" },
          { label: "Best Streak", value: "12 days", change: "All-time record", icon: Award, color: "#f59e0b", bg: "#fffbeb", trend: "up" },
          { label: "Top Subject", value: bestSubject?.name.split(" ")[0] || "D.S.", change: "Highest completion", icon: Target, color: "#10b981", bg: "#f0fdf4", trend: "up" },
        ].map((stat, i) => (
          <div key={i} className="rounded-2xl p-4 transition-all duration-200 hover:-translate-y-0.5" style={card}>
            <div className="flex items-start justify-between mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: stat.bg }}>
                <stat.icon className="w-5 h-5" style={{ color: stat.color }} />
              </div>
              <div className="flex items-center gap-1 px-2 py-1 rounded-lg" style={{ background: "#f0fdf4" }}>
                <TrendingUp className="w-3 h-3" style={{ color: "#10b981" }} />
              </div>
            </div>
            <p style={{ fontWeight: 800, fontSize: "1.4rem", color: colors.textPrimary }}>{stat.value}</p>
            <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{stat.label}</p>
            <p style={{ color: "#10b981", fontSize: "0.65rem", marginTop: 2, fontWeight: 600 }}>{stat.change}</p>
          </div>
        ))}
      </div>

      {/* Row 1: Productivity Trend + Radar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Productivity Trend – Current vs Last Week */}
        <div className="lg:col-span-2 rounded-2xl p-5" style={card}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Productivity Trend</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Current week vs last week</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-1.5 rounded-full" style={{ background: colors.secondary }} />
                <span style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>This week</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-1.5 rounded-full" style={{ background: "#94a3b8", opacity: 0.5 }} />
                <span style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>Last week</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-1.5 rounded-full border border-dashed" style={{ borderColor: "#f59e0b" }} />
                <span style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>Target</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={productivityTrend}>
              <defs>
                <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={colors.secondary} stopOpacity={0.25} />
                  <stop offset="95%" stopColor={colors.secondary} stopOpacity={0} />
                </linearGradient>
                <linearGradient id="lastWeekGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#94a3b8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="date" tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} domain={[50, 100]} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="score" name="This week" stroke={colors.secondary} strokeWidth={2.5} fill="url(#scoreGrad)" dot={{ fill: colors.secondary, r: 4, strokeWidth: 0 }} activeDot={{ r: 6 }} />
              <Line type="monotone" dataKey="target" name="Target" stroke="#f59e0b" strokeWidth={1.5} strokeDasharray="5 5" dot={false} />
            </AreaChart>
          </ResponsiveContainer>

          {/* Last week comparison */}
          <div className="mt-3 pt-3" style={{ borderTop: `1px solid ${colors.cardBorder}` }}>
            <p style={{ color: colors.textSecondary, fontSize: "0.7rem", marginBottom: 6 }}>Last week</p>
            <ResponsiveContainer width="100%" height={60}>
              <AreaChart data={lastWeekTrend}>
                <defs>
                  <linearGradient id="lastGrad2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.12} />
                    <stop offset="95%" stopColor="#94a3b8" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
                <Area type="monotone" dataKey="score" stroke="#94a3b8" strokeWidth={1.5} fill="url(#lastGrad2)" dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Radar Chart */}
        <div className="rounded-2xl p-5" style={card}>
          <div className="mb-4">
            <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Skills Radar</h3>
            <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Overall academic skill profile</p>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <RadarChart data={radarData}>
              <PolarGrid stroke={colors.cardBorder} />
              <PolarAngleAxis dataKey="metric" tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={false} axisLine={false} />
              <Radar name="Score" dataKey="score" stroke={colors.primary} fill={colors.primary} fillOpacity={0.25} strokeWidth={2} dot={{ fill: colors.primary, r: 3 }} />
            </RadarChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-2 mt-2">
            {radarData.map((d) => (
              <div key={d.metric} className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full" style={{ background: colors.primary }} />
                <span style={{ color: colors.textSecondary, fontSize: "0.65rem" }}>{d.metric}: {d.score}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 2: Subject Performance + Hours by Subject */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Subject Performance */}
        <div className="rounded-2xl p-5" style={card}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Subject Performance</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Average test/quiz scores</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={subjectPerformance} barSize={36}>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="subject" tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} domain={[0, 100]} />
              <Tooltip content={<CustomTooltip />} />
              <defs>
                <linearGradient id="subjGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={colors.primary} />
                  <stop offset="100%" stopColor={colors.secondary} />
                </linearGradient>
              </defs>
              <Bar dataKey="score" name="Score" fill="url(#subjGrad)" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Hours by Subject – current & prev month */}
        <div className="rounded-2xl p-5" style={card}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Hours by Subject (Monthly)</h3>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Weekly distribution breakdown</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={weeklyStudy} barSize={10}>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="week" tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 10, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontFamily: "Inter", fontSize: "0.7rem", paddingTop: 8 }} />
              <Bar dataKey="comp" name="Comp. Math" fill="#4F8EF7" radius={[4, 4, 0, 0]} />
              <Bar dataKey="bee" name="Elec. Eng." fill="#7B61FF" radius={[4, 4, 0, 0]} />
              <Bar dataKey="ds" name="D.S." fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="ai" name="A.I." fill="#f59e0b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="py" name="Python" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Row 3: Monthly Hours vs Goal + AI Insight */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Hours vs Goal */}
        <div className="rounded-2xl p-5" style={card}>
          <div className="mb-4">
            <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.95rem" }}>Monthly Hours vs Goal</h3>
            <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>Track your monthly study targets</p>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={monthlyHours} barSize={28}>
              <CartesianGrid strokeDasharray="3 3" stroke={colors.mutedBg} vertical={false} />
              <XAxis dataKey="month" tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontFamily: "Inter", fontSize: 11, fill: colors.textSecondary }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="hours" name="Actual" fill={colors.primary} radius={[6, 6, 0, 0]} />
              <Bar dataKey="goal" name="Goal" fill={colors.mutedBg} radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* AI Productivity Insight */}
        <div className="lg:col-span-2 rounded-2xl p-5 relative overflow-hidden" style={{ background: "linear-gradient(135deg, #1a1f3e 0%, #2d1b6e 100%)", boxShadow: "0 8px 30px rgba(79,142,247,0.15)" }}>
          <div className="absolute top-0 right-0 w-40 h-40 rounded-full opacity-10 blur-2xl pointer-events-none" style={{ background: "radial-gradient(circle, #7B61FF, transparent)", transform: "translate(20%, -20%)" }} />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: "rgba(79,142,247,0.2)" }}>
                <Brain className="w-4 h-4" style={{ color: "#4F8EF7" }} />
              </div>
              <div>
                <p className="text-white" style={{ fontWeight: 700, fontSize: "0.95rem" }}>AI Study Insight Report</p>
                <p style={{ color: "#718096", fontSize: "0.7rem" }}>Generated: {reportDate}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              {[
                { label: "Peak Hours", value: "6 PM – 9 PM", icon: "🕕", color: "#4F8EF7" },
                { label: "Weakest Day", value: "Wednesday", icon: "📅", color: "#ef4444" },
                { label: "Best Subject", value: bestSubject?.name.split(" ")[0] || "D.S.", icon: "💻", color: "#10b981" },
                { label: "Needs Focus", value: weakestSubject?.name.split(" ")[0] || "Python", icon: "📌", color: "#f59e0b" },
              ].map((item, i) => (
                <div key={i} className="p-3 rounded-xl" style={{ background: "rgba(255,255,255,0.06)" }}>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-base">{item.icon}</span>
                    <p style={{ color: "#94a3b8", fontSize: "0.65rem" }}>{item.label}</p>
                  </div>
                  <p style={{ color: item.color, fontWeight: 700, fontSize: "0.875rem" }}>{item.value}</p>
                </div>
              ))}
            </div>

            <div className="p-4 rounded-xl" style={{ background: "rgba(79,142,247,0.1)", border: "1px solid rgba(79,142,247,0.2)" }}>
              <p style={{ color: "#94a3b8", fontSize: "0.75rem", lineHeight: 1.7 }}>
                🤖 <span style={{ color: "#4F8EF7", fontWeight: 600 }}>AI Analysis:</span> Based on your past 7 days, your average productivity is <span style={{ color: "#10b981", fontWeight: 600 }}>78%</span> — <span style={{ color: "#f59e0b" }}>12% above average</span>. You perform best on <span style={{ color: "#7B61FF", fontWeight: 600 }}>Saturdays</span> and your focus peaks between <span style={{ color: "#4F8EF7", fontWeight: 600 }}>6 PM – 9 PM</span>. Recommend scheduling Computation Math & Electronics during this window. Consider a 20-min break pattern on Wednesdays.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
