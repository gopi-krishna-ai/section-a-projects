import { useState } from "react";
import { ChevronLeft, ChevronRight, Plus, X, Clock, BookOpen } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useStudyData, CalendarEvent } from "../context/StudyDataContext";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const EVENT_TYPES = ["exam", "assignment", "study", "reminder"] as const;
const TYPE_COLORS: Record<string, string> = { exam: "#ef4444", assignment: "#f59e0b", study: "#10b981", reminder: "#6366f1" };
const TYPE_BG: Record<string, string> = { exam: "#fef2f2", assignment: "#fffbeb", study: "#f0fdf4", reminder: "#eef2ff" };

function buildCalendar(year: number, month: number) {
  const first = new Date(year, month, 1).getDay();
  const days = new Date(year, month + 1, 0).getDate();
  const cells: (number | null)[] = Array(first).fill(null);
  for (let d = 1; d <= days; d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);
  return cells;
}

function fmt(year: number, month: number, day: number) {
  return `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

interface AddEventForm { title: string; time: string; type: CalendarEvent["type"]; description: string; }

export function CalendarPage() {
  const { colors } = useTheme();
  const { events, addEvent, deleteEvent } = useStudyData();

  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());
  const [selected, setSelected] = useState<string>(fmt(today.getFullYear(), today.getMonth(), today.getDate()));
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState<AddEventForm>({ title: "", time: "09:00", type: "study", description: "" });

  const prev = () => { if (month === 0) { setMonth(11); setYear(y => y - 1); } else setMonth(m => m - 1); };
  const next = () => { if (month === 11) { setMonth(0); setYear(y => y + 1); } else setMonth(m => m + 1); };

  const cells = buildCalendar(year, month);
  const todayStr = fmt(today.getFullYear(), today.getMonth(), today.getDate());
  const selectedEvents = events.filter(e => e.date === selected);
  const upcomingEvents = events.filter(e => e.date >= todayStr).sort((a, b) => a.date.localeCompare(b.date)).slice(0, 5);

  const getEventsForDay = (day: number) => events.filter(e => e.date === fmt(year, month, day));

  const handleAdd = () => {
    if (!form.title.trim()) return;
    addEvent({ ...form, date: selected, color: TYPE_COLORS[form.type] });
    setForm({ title: "", time: "09:00", type: "study", description: "" });
    setShowAdd(false);
  };

  const card: React.CSSProperties = { background: colors.cardBg, border: `1px solid ${colors.cardBorder}`, borderRadius: 16, boxShadow: `0 4px 20px ${colors.primary}0d` };
  const label: React.CSSProperties = { color: colors.textSecondary, fontSize: "0.78rem", fontWeight: 600, display: "block", marginBottom: 4 };
  const input: React.CSSProperties = { width: "100%", padding: "0.65rem 0.85rem", borderRadius: "0.6rem", outline: "none", background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, fontFamily: "Inter, sans-serif", fontSize: "0.875rem", color: colors.textPrimary, boxSizing: "border-box" };

  return (
    <div className="space-y-5" style={{ fontFamily: "Inter, sans-serif" }}>
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-5">
        {/* Calendar grid (spans 3 cols) */}
        <div className="xl:col-span-3 p-5" style={card}>
          {/* Header */}
          <div className="flex items-center justify-between mb-5">
            <h2 style={{ fontWeight: 700, fontSize: "1.1rem", color: colors.textPrimary }}>
              {MONTHS[month]} {year}
            </h2>
            <div className="flex items-center gap-2">
              <button onClick={prev} className="w-8 h-8 rounded-lg flex items-center justify-center transition-all" style={{ background: colors.mutedBg, color: colors.textSecondary }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = colors.gradient; (e.currentTarget as HTMLElement).style.color = "#fff"; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = colors.mutedBg; (e.currentTarget as HTMLElement).style.color = colors.textSecondary; }}
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button onClick={() => { setYear(today.getFullYear()); setMonth(today.getMonth()); setSelected(todayStr); }}
                className="px-3 py-1.5 rounded-lg text-xs transition-all" style={{ background: colors.mutedBg, color: colors.textSecondary, fontWeight: 500 }}>Today</button>
              <button onClick={next} className="w-8 h-8 rounded-lg flex items-center justify-center transition-all" style={{ background: colors.mutedBg, color: colors.textSecondary }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = colors.gradient; (e.currentTarget as HTMLElement).style.color = "#fff"; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = colors.mutedBg; (e.currentTarget as HTMLElement).style.color = colors.textSecondary; }}
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Day headers */}
          <div className="grid grid-cols-7 mb-2">
            {DAYS.map(d => (
              <div key={d} className="text-center py-2" style={{ color: colors.textSecondary, fontSize: "0.75rem", fontWeight: 600 }}>{d}</div>
            ))}
          </div>

          {/* Day cells */}
          <div className="grid grid-cols-7 gap-0.5">
            {cells.map((day, i) => {
              if (!day) return <div key={i} className="aspect-square" />;
              const dateStr = fmt(year, month, day);
              const isToday = dateStr === todayStr;
              const isSelected = dateStr === selected;
              const dayEvents = getEventsForDay(day);
              return (
                <button key={i} onClick={() => setSelected(dateStr)}
                  className="aspect-square flex flex-col items-center justify-start p-1 rounded-xl transition-all duration-150 relative"
                  style={{
                    background: isSelected ? colors.gradient : isToday ? `${colors.primary}18` : "transparent",
                    border: isToday && !isSelected ? `1.5px solid ${colors.primary}40` : "1.5px solid transparent",
                  }}
                >
                  <span style={{ fontWeight: isToday || isSelected ? 700 : 400, fontSize: "0.82rem", color: isSelected ? "#fff" : isToday ? colors.primary : colors.textPrimary, lineHeight: 1 }}>{day}</span>
                  <div className="flex flex-wrap gap-0.5 mt-0.5 justify-center">
                    {dayEvents.slice(0, 3).map(ev => (
                      <div key={ev.id} className="w-1.5 h-1.5 rounded-full" style={{ background: isSelected ? "rgba(255,255,255,0.8)" : ev.color }} />
                    ))}
                    {dayEvents.length > 3 && <span style={{ fontSize: "0.5rem", color: isSelected ? "rgba(255,255,255,0.7)" : colors.textSecondary }}>+{dayEvents.length - 3}</span>}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right sidebar */}
        <div className="space-y-4">
          {/* Selected day events */}
          <div className="p-5" style={card}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <p style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>
                  {new Date(selected + "T12:00:00").toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric" })}
                </p>
                <p style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{selectedEvents.length} event{selectedEvents.length !== 1 ? "s" : ""}</p>
              </div>
              <button onClick={() => setShowAdd(true)} className="w-8 h-8 rounded-xl flex items-center justify-center transition-all" style={{ background: colors.gradient, color: "#fff" }}>
                <Plus className="w-4 h-4" />
              </button>
            </div>

            {showAdd && (
              <div className="mb-4 p-4 rounded-xl space-y-3" style={{ background: colors.mutedBg, border: `1px solid ${colors.cardBorder}` }}>
                <div>
                  <label style={label}>Event title</label>
                  <input value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} placeholder="e.g. Math Exam" style={input}
                    onFocus={e => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                    onBlur={e => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                  />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label style={label}>Time</label>
                    <input type="time" value={form.time} onChange={e => setForm(f => ({ ...f, time: e.target.value }))} style={input} />
                  </div>
                  <div>
                    <label style={label}>Type</label>
                    <select value={form.type} onChange={e => setForm(f => ({ ...f, type: e.target.value as CalendarEvent["type"] }))} style={{ ...input, appearance: "none" }}>
                      {EVENT_TYPES.map(t => <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>)}
                    </select>
                  </div>
                </div>
                <div>
                  <label style={label}>Notes (optional)</label>
                  <input value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} placeholder="Any details..." style={input}
                    onFocus={e => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                    onBlur={e => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                  />
                </div>
                <div className="flex gap-2">
                  <button onClick={handleAdd} className="flex-1 py-2 rounded-lg text-white text-sm font-semibold" style={{ background: colors.gradient }}>Add event</button>
                  <button onClick={() => setShowAdd(false)} className="px-3 py-2 rounded-lg text-sm" style={{ background: colors.mutedBg, color: colors.textSecondary }}>Cancel</button>
                </div>
              </div>
            )}

            {selectedEvents.length === 0 && !showAdd ? (
              <div className="text-center py-8">
                <BookOpen className="w-8 h-8 mx-auto mb-2" style={{ color: colors.textSecondary }} />
                <p style={{ color: colors.textSecondary, fontSize: "0.82rem" }}>No events. Click + to add one.</p>
              </div>
            ) : (
              <div className="space-y-2">
                {selectedEvents.map(ev => (
                  <div key={ev.id} className="p-3 rounded-xl flex items-start gap-3 group" style={{ background: TYPE_BG[ev.type], border: `1px solid ${ev.color}22` }}>
                    <div className="w-2.5 h-2.5 rounded-full flex-shrink-0 mt-1" style={{ background: ev.color }} />
                    <div className="flex-1 min-w-0">
                      <p style={{ fontWeight: 600, fontSize: "0.82rem", color: colors.textPrimary, lineHeight: 1.3 }}>{ev.title}</p>
                      <div className="flex items-center gap-1 mt-0.5">
                        <Clock className="w-3 h-3" style={{ color: colors.textSecondary }} />
                        <span style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>{ev.time}</span>
                        <span className="ml-1 px-1.5 py-0.5 rounded" style={{ background: ev.color + "22", color: ev.color, fontSize: "0.62rem", fontWeight: 600, textTransform: "capitalize" }}>{ev.type}</span>
                      </div>
                      {ev.description && <p style={{ color: colors.textSecondary, fontSize: "0.7rem", marginTop: 2, lineHeight: 1.4 }}>{ev.description}</p>}
                    </div>
                    <button onClick={() => deleteEvent(ev.id)} className="w-5 h-5 rounded flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all" style={{ color: "#ef4444" }}>
                      <X className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Upcoming events */}
          <div className="p-5" style={card}>
            <p style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem", marginBottom: 12 }}>Upcoming</p>
            {upcomingEvents.length === 0 ? (
              <p style={{ color: colors.textSecondary, fontSize: "0.82rem" }}>No upcoming events.</p>
            ) : (
              <div className="space-y-2.5">
                {upcomingEvents.map(ev => (
                  <div key={ev.id} className="flex items-start gap-2.5 cursor-pointer" onClick={() => setSelected(ev.date)}>
                    <div className="w-2 h-2 rounded-full flex-shrink-0 mt-1.5" style={{ background: ev.color }} />
                    <div>
                      <p style={{ fontWeight: 500, fontSize: "0.8rem", color: colors.textPrimary, lineHeight: 1.3 }}>{ev.title}</p>
                      <p style={{ color: colors.textSecondary, fontSize: "0.68rem" }}>
                        {new Date(ev.date + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" })} · {ev.time}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
