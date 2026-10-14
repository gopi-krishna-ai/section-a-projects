import { useState } from "react";
import { CheckCircle2, Circle, Clock, Plus, Trash2, Trophy, Zap, Calendar, Tag, X, ChevronDown } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useStudyData } from "../context/StudyDataContext";

const priorityConfig = {
  high: { color: "#ef4444", bg: "#fef2f2", label: "High" },
  medium: { color: "#f59e0b", bg: "#fffbeb", label: "Medium" },
  low: { color: "#10b981", bg: "#f0fdf4", label: "Low" },
};

const today = new Date().toISOString().split("T")[0];
const addDays = (n: number) => new Date(Date.now() + n * 86400000).toISOString().split("T")[0];

export function TasksPage() {
  const { colors } = useTheme();
  const { tasks, addTask, deleteTask, toggleTask, subjects } = useStudyData();

  const [filter, setFilter] = useState<"all" | "pending" | "completed" | "today" | "high">("all");
  const [showAdd, setShowAdd] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newSubject, setNewSubject] = useState(subjects[0]?.name || "Mathematics");
  const [newDuration, setNewDuration] = useState("1h");
  const [newPriority, setNewPriority] = useState<"high" | "medium" | "low">("medium");
  const [newDeadline, setNewDeadline] = useState(today);
  const [newCategory, setNewCategory] = useState("Study");
  const [sortBy, setSortBy] = useState<"deadline" | "priority" | "subject">("deadline");

  const priorityOrder = { high: 0, medium: 1, low: 2 };

  const filtered = tasks.filter(t => {
    if (filter === "pending") return !t.completed;
    if (filter === "completed") return t.completed;
    if (filter === "today") return t.deadline === today && !t.completed;
    if (filter === "high") return t.priority === "high" && !t.completed;
    return true;
  }).sort((a, b) => {
    if (sortBy === "priority") return priorityOrder[a.priority] - priorityOrder[b.priority];
    if (sortBy === "subject") return a.subject.localeCompare(b.subject);
    return a.deadline.localeCompare(b.deadline);
  });

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.filter(t => !t.completed).length;
  const todayCount = tasks.filter(t => t.deadline === today && !t.completed).length;
  const highCount = tasks.filter(t => t.priority === "high" && !t.completed).length;
  const completionPct = tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0;

  const subjectColors: Record<string, string> = Object.fromEntries(subjects.map(s => [s.name, s.color]));

  const handleAdd = () => {
    if (!newTitle.trim()) return;
    const subj = subjects.find(s => s.name === newSubject);
    addTask({ title: newTitle.trim(), subject: newSubject, subjectColor: subj?.color || "#4F8EF7", priority: newPriority, deadline: newDeadline, duration: newDuration, completed: false, category: newCategory });
    setNewTitle("");
    setShowAdd(false);
  };

  const card: React.CSSProperties = { background: colors.cardBg, border: `1px solid ${colors.cardBorder}`, boxShadow: `0 4px 20px ${colors.primary}0d` };
  const inputS: React.CSSProperties = { background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, color: colors.textPrimary, fontFamily: "Inter, sans-serif", fontSize: "0.875rem", outline: "none", borderRadius: "0.75rem", padding: "0.65rem 0.9rem", boxSizing: "border-box" };

  const isOverdue = (deadline: string) => !tasks.find(t => t.deadline === deadline)?.completed && deadline < today;

  return (
    <div className="space-y-5" style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Tasks", value: tasks.length, icon: "📋", color: colors.primary },
          { label: "Completed", value: completedCount, icon: "✅", color: "#10b981" },
          { label: "Due Today", value: todayCount, icon: "⏰", color: "#f59e0b" },
          { label: "High Priority", value: highCount, icon: "🔥", color: "#ef4444" },
        ].map((s, i) => (
          <div key={i} className="rounded-2xl p-4" style={card}>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xl">{s.icon}</span>
              <span style={{ color: colors.textSecondary, fontSize: "0.75rem" }}>{s.label}</span>
            </div>
            <p style={{ fontWeight: 800, fontSize: "1.5rem", color: colors.textPrimary }}>{s.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Task list */}
        <div className="lg:col-span-2 space-y-4">
          {/* Controls */}
          <div className="flex items-center justify-between gap-3 flex-wrap">
            <div className="flex rounded-xl overflow-hidden" style={{ background: colors.cardBg, border: `1px solid ${colors.cardBorder}` }}>
              {([
                { key: "all", label: `All (${tasks.length})` },
                { key: "pending", label: `Pending (${pendingCount})` },
                { key: "today", label: `Today (${todayCount})` },
                { key: "high", label: `High (${highCount})` },
                { key: "completed", label: `Done (${completedCount})` },
              ] as const).map(({ key, label }) => (
                <button key={key} onClick={() => setFilter(key)} className="px-3 py-2 text-xs transition-all duration-150" style={{ background: filter === key ? colors.gradient : "transparent", color: filter === key ? "#fff" : colors.textSecondary, fontWeight: filter === key ? 600 : 400 }}>
                  {label}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-2">
              <select value={sortBy} onChange={e => setSortBy(e.target.value as typeof sortBy)} style={{ ...inputS, padding: "0.45rem 0.75rem", fontSize: "0.78rem", appearance: "none", cursor: "pointer" }}>
                <option value="deadline">Sort: Deadline</option>
                <option value="priority">Sort: Priority</option>
                <option value="subject">Sort: Subject</option>
              </select>
              <button onClick={() => setShowAdd(!showAdd)} className="flex items-center gap-1.5 px-4 py-2 rounded-xl transition-all text-white text-sm font-semibold" style={{ background: colors.gradient }}>
                <Plus className="w-4 h-4" /> Add Task
              </button>
            </div>
          </div>

          {/* Add Task Form */}
          {showAdd && (
            <div className="rounded-2xl p-5" style={{ ...card, border: `1.5px solid ${colors.primary}30` }}>
              <div className="flex items-center justify-between mb-4">
                <h4 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>New Task</h4>
                <button onClick={() => setShowAdd(false)}><X className="w-4 h-4" style={{ color: colors.textSecondary }} /></button>
              </div>
              <div className="space-y-3">
                <input type="text" value={newTitle} onChange={e => setNewTitle(e.target.value)} placeholder="What do you need to study?" style={{ ...inputS, width: "100%" }}
                  onFocus={e => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                  onBlur={e => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                  onKeyDown={e => { if (e.key === "Enter") handleAdd(); }}
                />
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 4 }}>Subject</label>
                    <select value={newSubject} onChange={e => setNewSubject(e.target.value)} style={{ ...inputS, width: "100%", appearance: "none" }}>
                      {subjects.map(s => <option key={s.id} value={s.name}>{s.name}</option>)}
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 4 }}>Duration</label>
                    <select value={newDuration} onChange={e => setNewDuration(e.target.value)} style={{ ...inputS, width: "100%", appearance: "none" }}>
                      {["15m", "30m", "45m", "1h", "1.5h", "2h", "3h"].map(d => <option key={d}>{d}</option>)}
                    </select>
                  </div>
                  <div>
                    <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 4 }}>Deadline</label>
                    <input type="date" value={newDeadline} onChange={e => setNewDeadline(e.target.value)} style={{ ...inputS, width: "100%" }} />
                  </div>
                  <div>
                    <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 4 }}>Category</label>
                    <select value={newCategory} onChange={e => setNewCategory(e.target.value)} style={{ ...inputS, width: "100%", appearance: "none" }}>
                      {["Study", "Practice", "Revision", "Reading", "Assignment", "Project"].map(c => <option key={c}>{c}</option>)}
                    </select>
                  </div>
                </div>
                <div>
                  <label style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Priority</label>
                  <div className="flex gap-2">
                    {(["high", "medium", "low"] as const).map(p => (
                      <button key={p} type="button" onClick={() => setNewPriority(p)} className="flex-1 py-2 rounded-xl text-xs transition-all" style={{ background: newPriority === p ? priorityConfig[p].bg : colors.mutedBg, color: newPriority === p ? priorityConfig[p].color : colors.textSecondary, fontWeight: newPriority === p ? 700 : 400, border: `1.5px solid ${newPriority === p ? priorityConfig[p].color : "transparent"}` }}>
                        {priorityConfig[p].label}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={handleAdd} className="flex-1 py-2.5 rounded-xl text-white font-semibold text-sm" style={{ background: colors.gradient }}>Add Task</button>
                  <button onClick={() => setShowAdd(false)} className="px-4 py-2.5 rounded-xl text-sm" style={{ background: colors.mutedBg, color: colors.textSecondary }}>Cancel</button>
                </div>
              </div>
            </div>
          )}

          {/* Task cards */}
          <div className="space-y-2">
            {filtered.map(task => {
              const overdue = !task.completed && task.deadline < today;
              return (
                <div key={task.id} className="group rounded-2xl p-4 transition-all duration-150 hover:-translate-y-0.5" style={{ ...card, border: task.completed ? `1.5px solid #10b98122` : overdue ? `1.5px solid #ef444422` : `1.5px solid ${colors.cardBorder}`, opacity: task.completed ? 0.75 : 1 }}>
                  <div className="flex items-start gap-3">
                    <button onClick={() => toggleTask(task.id)} className="mt-0.5 flex-shrink-0 transition-all">
                      {task.completed ? <CheckCircle2 className="w-5 h-5" style={{ color: "#10b981" }} /> : <Circle className="w-5 h-5" style={{ color: colors.inputBorder }} />}
                    </button>
                    <div className="flex-1 min-w-0">
                      <p style={{ fontWeight: 500, color: task.completed ? colors.textSecondary : colors.textPrimary, fontSize: "0.875rem", textDecoration: task.completed ? "line-through" : "none", lineHeight: 1.4 }}>{task.title}</p>
                      <div className="flex items-center gap-2 mt-1 flex-wrap">
                        <span className="flex items-center gap-1" style={{ color: subjectColors[task.subject] || colors.primary, fontSize: "0.7rem", fontWeight: 500 }}>
                          <Tag className="w-3 h-3" />{task.subject}
                        </span>
                        <span style={{ color: colors.cardBorder }}>·</span>
                        <span className="flex items-center gap-1" style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>
                          <Clock className="w-3 h-3" />{task.duration}
                        </span>
                        <span style={{ color: colors.cardBorder }}>·</span>
                        <span className="flex items-center gap-1" style={{ color: overdue ? "#ef4444" : colors.textSecondary, fontSize: "0.7rem", fontWeight: overdue ? 600 : 400 }}>
                          <Calendar className="w-3 h-3" />
                          {overdue ? "Overdue" : task.deadline === today ? "Today" : task.deadline}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 ml-auto flex-shrink-0">
                      <span className="px-2 py-0.5 rounded-full text-xs" style={{ background: priorityConfig[task.priority].bg, color: priorityConfig[task.priority].color, fontWeight: 600, fontSize: "0.62rem" }}>
                        {priorityConfig[task.priority].label}
                      </span>
                      <span className="px-2 py-0.5 rounded-full text-xs hidden sm:block" style={{ background: `${subjectColors[task.subject] || colors.primary}18`, color: subjectColors[task.subject] || colors.primary, fontWeight: 600, fontSize: "0.62rem" }}>
                        {task.category}
                      </span>
                      <button onClick={() => deleteTask(task.id)} className="w-7 h-7 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-150"
                        onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = "#fef2f2"; }}
                        onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                        <Trash2 className="w-3.5 h-3.5" style={{ color: "#ef4444" }} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
            {filtered.length === 0 && (
              <div className="text-center py-14 rounded-2xl" style={card}>
                <CheckCircle2 className="w-10 h-10 mx-auto mb-3" style={{ color: colors.textSecondary }} />
                <p style={{ color: colors.textPrimary, fontWeight: 600, fontSize: "0.95rem", marginBottom: 6 }}>No tasks here</p>
                <p style={{ color: colors.textSecondary, fontSize: "0.85rem" }}>
                  {filter === "completed" ? "Complete some tasks to see them here." : "Add a new task to get started!"}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right panel */}
        <div className="space-y-4">
          {/* Progress circle */}
          <div className="rounded-2xl p-5 text-center" style={card}>
            <div className="flex items-center gap-2 mb-4 justify-center">
              <Trophy className="w-4 h-4" style={{ color: "#f59e0b" }} />
              <span style={{ fontWeight: 600, color: colors.textPrimary, fontSize: "0.875rem" }}>Overall Progress</span>
            </div>
            <div className="relative w-32 h-32 mx-auto mb-4">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="52" fill="none" stroke={colors.mutedBg} strokeWidth="10" />
                <circle cx="60" cy="60" r="52" fill="none" strokeWidth="10" strokeLinecap="round"
                  stroke="url(#progressGrad)"
                  strokeDasharray={`${2 * Math.PI * 52}`}
                  strokeDashoffset={`${2 * Math.PI * 52 * (1 - completionPct / 100)}`}
                  style={{ transition: "stroke-dashoffset 1s ease" }}
                />
                <defs>
                  <linearGradient id="progressGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop key="pg0" offset="0%" stopColor={colors.primary} />
                    <stop key="pg1" offset="100%" stopColor="#10b981" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span style={{ fontWeight: 800, fontSize: "1.6rem", color: colors.textPrimary }}>{completionPct}%</span>
                <span style={{ color: colors.textSecondary, fontSize: "0.65rem" }}>Complete</span>
              </div>
            </div>
            <p style={{ color: colors.textSecondary, fontSize: "0.78rem", lineHeight: 1.5 }}>
              {completedCount} of {tasks.length} tasks completed.
              {completionPct >= 70 ? " 🎉 Excellent progress!" : " Keep going!"}
            </p>
          </div>

          {/* Study Time */}
          <div className="rounded-2xl p-5" style={card}>
            <div className="flex items-center gap-2 mb-3">
              <Zap className="w-4 h-4" style={{ color: colors.secondary }} />
              <span style={{ fontWeight: 600, color: colors.textPrimary, fontSize: "0.875rem" }}>Study Time</span>
            </div>
            <div className="space-y-3">
              {(() => {
                const parse = (d: string) => { const h = parseFloat(d); return isNaN(h) ? 0.5 : h; };
                const total = tasks.reduce((a, t) => a + parse(t.duration), 0);
                const done = tasks.filter(t => t.completed).reduce((a, t) => a + parse(t.duration), 0);
                return [
                  { label: "Completed", value: `${done}h`, color: "#10b981" },
                  { label: "Remaining", value: `${(total - done).toFixed(1)}h`, color: "#f59e0b" },
                  { label: "Total planned", value: `${total}h`, color: colors.primary },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span style={{ color: colors.textSecondary, fontSize: "0.78rem" }}>{item.label}</span>
                    <span style={{ color: item.color, fontWeight: 700, fontSize: "0.9rem" }}>{item.value}</span>
                  </div>
                ));
              })()}
            </div>
          </div>

          {/* By Subject */}
          <div className="rounded-2xl p-5" style={card}>
            <h4 style={{ fontWeight: 600, color: colors.textPrimary, fontSize: "0.875rem", marginBottom: 12 }}>By Subject</h4>
            <div className="space-y-3">
              {subjects.map((sub) => {
                const subTasks = tasks.filter(t => t.subject === sub.name);
                const subDone = subTasks.filter(t => t.completed).length;
                const pct = subTasks.length > 0 ? Math.round((subDone / subTasks.length) * 100) : 0;
                return (
                  <div key={sub.id}>
                    <div className="flex justify-between mb-1">
                      <span style={{ color: colors.textPrimary, fontSize: "0.75rem", fontWeight: 500 }}>{sub.name}</span>
                      <span style={{ color: sub.color, fontSize: "0.75rem", fontWeight: 600 }}>{subDone}/{subTasks.length}</span>
                    </div>
                    <div className="h-1.5 rounded-full" style={{ background: colors.mutedBg }}>
                      <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, background: sub.color }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
