import { useState } from "react";
import {
  BookOpen, Clock, BarChart2, Save, X,
  CheckCircle2, Zap, Brain, Plus, Trash2, Pencil
} from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useStudyData, Subject } from "../context/StudyDataContext";

const difficultyOptions = [
  { value: "Easy" as const, color: "#10b981", bg: "#f0fdf4", desc: "Light review, low mental effort" },
  { value: "Medium" as const, color: "#f59e0b", bg: "#fffbeb", desc: "Moderate focus required" },
  { value: "Hard" as const, color: "#ef4444", bg: "#fef2f2", desc: "Deep concentration needed" },
];

const subjectEmojis = ["📐", "⚡", "💻", "🤖", "🐍", "🌍", "🎨", "📊", "🧬", "📚", "🔭", "🧮"];
const subjectColors = ["#4F8EF7", "#7B61FF", "#10b981", "#f59e0b", "#ef4444", "#06b6d4", "#8b5cf6", "#f97316"];

export function AddSubjectPage() {
  const { colors } = useTheme();
  const { subjects, addSubject, updateSubject, deleteSubject } = useStudyData();

  const [editingId, setEditingId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [hours, setHours] = useState(3);
  const [difficulty, setDifficulty] = useState<"Easy" | "Medium" | "Hard">("Medium");
  const [selectedEmoji, setSelectedEmoji] = useState("📚");
  const [success, setSuccess] = useState(false);

  const cardStyle = {
    background: colors.cardBg,
    border: `1px solid ${colors.cardBorder}`,
    boxShadow: `0 4px 20px ${colors.primary}0d`,
  };

  const inputStyle = {
    background: colors.inputBg,
    border: `1.5px solid ${colors.inputBorder}`,
    color: colors.textPrimary,
    fontFamily: "Inter, sans-serif",
    fontSize: "0.875rem",
  };

  const handleEdit = (subject: Subject) => {
    setEditingId(subject.id);
    setName(subject.name);
    setHours(subject.totalHours);
    setDifficulty(subject.difficulty);
    setSelectedEmoji(subject.emoji);
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setName("");
    setHours(3);
    setDifficulty("Medium");
    setSelectedEmoji("📚");
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    if (editingId) {
      updateSubject(editingId, { name: name.trim(), totalHours: hours, difficulty, emoji: selectedEmoji });
      handleCancelEdit();
    } else {
      const color = subjectColors[subjects.length % subjectColors.length];
      addSubject({
        name: name.trim(),
        emoji: selectedEmoji,
        color,
        totalHours: hours,
        completedHours: 0,
        difficulty,
      });
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        setName("");
        setHours(3);
        setDifficulty("Medium");
        setSelectedEmoji("📚");
      }, 2000);
    }
  };

  return (
    <div className="space-y-6" style={{ fontFamily: "Inter, sans-serif" }}>
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Form */}
        <div className="lg:col-span-3">
          <div className="rounded-2xl overflow-hidden" style={cardStyle}>
            <div className="p-6 pb-4" style={{ background: editingId ? `linear-gradient(135deg, #f59e0b, #ef4444)` : colors.gradient }}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: "rgba(255,255,255,0.2)" }}>
                    {editingId ? <Pencil className="w-5 h-5 text-white" /> : <Plus className="w-6 h-6 text-white" />}
                  </div>
                  <div>
                    <h2 className="text-white" style={{ fontWeight: 700, fontSize: "1.1rem" }}>
                      {editingId ? "Edit Subject" : "Add New Subject"}
                    </h2>
                    <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "0.75rem" }}>
                      {editingId ? "Update subject details below" : "Plan your next study session with AI guidance"}
                    </p>
                  </div>
                </div>
                {editingId && (
                  <button onClick={handleCancelEdit} className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ background: "rgba(255,255,255,0.15)" }}>
                    <X className="w-4 h-4 text-white" />
                  </button>
                )}
              </div>
            </div>

            <form onSubmit={handleSave} className="p-6 space-y-5">
              {/* Emoji Selector */}
              <div>
                <label style={{ color: colors.textSecondary, fontSize: "0.825rem", fontWeight: 600 }}>Pick an Icon</label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {subjectEmojis.map((emoji) => (
                    <button
                      key={emoji}
                      type="button"
                      onClick={() => setSelectedEmoji(emoji)}
                      className="w-10 h-10 rounded-xl text-xl flex items-center justify-center transition-all duration-200"
                      style={{
                        background: selectedEmoji === emoji ? colors.gradient : colors.mutedBg,
                        transform: selectedEmoji === emoji ? "scale(1.1)" : "scale(1)",
                        boxShadow: selectedEmoji === emoji ? `0 4px 12px ${colors.primary}40` : "none",
                      }}
                    >
                      {emoji}
                    </button>
                  ))}
                </div>
              </div>

              {/* Subject Name */}
              <div>
                <label style={{ color: colors.textSecondary, fontSize: "0.825rem", fontWeight: 600 }}>Subject Name *</label>
                <div className="relative mt-1.5">
                  <BookOpen className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: colors.textSecondary }} />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Advanced Mathematics"
                    required
                    className="w-full pl-10 pr-4 py-3 rounded-xl outline-none transition-all duration-200"
                    style={inputStyle}
                    onFocus={(e) => { e.target.style.border = `1.5px solid ${colors.primary}`; }}
                    onBlur={(e) => { e.target.style.border = `1.5px solid ${colors.inputBorder}`; }}
                  />
                </div>
              </div>

              {/* Target Study Hours */}
              <div>
                <label style={{ color: colors.textSecondary, fontSize: "0.825rem", fontWeight: 600 }}>
                  Target Study Hours: <span style={{ color: colors.primary }}>{hours}h</span>
                </label>
                <div className="mt-3 flex items-center gap-4">
                  <input
                    type="range"
                    min={0.5}
                    max={12}
                    step={0.5}
                    value={hours}
                    onChange={(e) => setHours(parseFloat(e.target.value))}
                    className="flex-1 h-2 rounded-full appearance-none cursor-pointer"
                    style={{ accentColor: colors.primary }}
                  />
                  <div className="flex items-center gap-1.5 px-3 py-2 rounded-xl min-w-[60px] justify-center" style={{ background: `${colors.primary}18` }}>
                    <Clock className="w-3.5 h-3.5" style={{ color: colors.primary }} />
                    <span style={{ color: colors.primary, fontWeight: 700, fontSize: "0.85rem" }}>{hours}h</span>
                  </div>
                </div>
                <div className="flex justify-between mt-1">
                  {[0.5, 3, 6, 9, 12].map(v => (
                    <span key={v} style={{ color: colors.textSecondary, fontSize: "0.65rem" }}>{v}h</span>
                  ))}
                </div>
              </div>

              {/* Difficulty Level */}
              <div>
                <label style={{ color: colors.textSecondary, fontSize: "0.825rem", fontWeight: 600 }}>Difficulty Level</label>
                <div className="grid grid-cols-3 gap-3 mt-2">
                  {difficultyOptions.map(({ value, color, bg, desc }) => (
                    <button
                      key={value}
                      type="button"
                      onClick={() => setDifficulty(value)}
                      className="p-3 rounded-xl transition-all duration-200 text-left"
                      style={{
                        background: difficulty === value ? bg : colors.mutedBg,
                        border: `2px solid ${difficulty === value ? color : colors.cardBorder}`,
                        transform: difficulty === value ? "translateY(-2px)" : "none",
                        boxShadow: difficulty === value ? `0 4px 12px ${color}30` : "none",
                      }}
                    >
                      <div className="flex items-center gap-1.5 mb-1">
                        <BarChart2 className="w-3.5 h-3.5" style={{ color }} />
                        <span style={{ color, fontWeight: 700, fontSize: "0.8rem" }}>{value}</span>
                      </div>
                      <p style={{ color: colors.textSecondary, fontSize: "0.65rem", lineHeight: 1.4 }}>{desc}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* AI Suggestion */}
              <div className="p-4 rounded-xl" style={{ background: `linear-gradient(135deg, ${colors.primary}0d, ${colors.secondary}0d)`, border: `1.5px solid ${colors.primary}25` }}>
                <div className="flex items-center gap-2 mb-1">
                  <Brain className="w-4 h-4" style={{ color: colors.secondary }} />
                  <span style={{ color: colors.secondary, fontWeight: 600, fontSize: "0.78rem" }}>AI Suggestion</span>
                </div>
                <p style={{ color: colors.textSecondary, fontSize: "0.75rem", lineHeight: 1.5 }}>
                  Based on your schedule, the best time for <strong>{difficulty}</strong> subjects is{" "}
                  <span style={{ color: colors.primary, fontWeight: 600 }}>
                    {difficulty === "Hard" ? "6 PM – 9 PM" : difficulty === "Medium" ? "4 PM – 7 PM" : "10 AM – 12 PM"}
                  </span>
                  {" "}when your focus peaks.
                </p>
              </div>

              {/* Buttons */}
              <div className="flex gap-3 pt-2">
                <button
                  type="submit"
                  className="flex-1 flex items-center justify-center gap-2 py-3.5 rounded-xl transition-all duration-200"
                  style={{
                    background: success ? "linear-gradient(135deg, #10b981, #059669)" : editingId ? "linear-gradient(135deg, #f59e0b, #ef4444)" : colors.gradient,
                    color: "#fff",
                    fontWeight: 600,
                    fontSize: "0.9rem",
                    boxShadow: success ? "0 8px 30px rgba(16,185,129,0.35)" : `0 8px 30px ${colors.primary}35`,
                  }}
                >
                  {success ? (
                    <><CheckCircle2 className="w-4 h-4" /> Saved Successfully!</>
                  ) : editingId ? (
                    <><Save className="w-4 h-4" /> Update Subject</>
                  ) : (
                    <><Save className="w-4 h-4" /> Save Subject</>
                  )}
                </button>
                {editingId && (
                  <button
                    type="button"
                    onClick={handleCancelEdit}
                    className="px-5 py-3.5 rounded-xl transition-all duration-200"
                    style={{ background: colors.mutedBg, color: colors.textSecondary, fontWeight: 600, fontSize: "0.9rem" }}
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
            </form>
          </div>
        </div>

        {/* Right: Tips + Subjects List */}
        <div className="lg:col-span-2 space-y-4">
          {/* AI Tips */}
          <div className="rounded-2xl p-5" style={{ background: "linear-gradient(135deg, #1a1f3e, #2d1b6e)", boxShadow: "0 4px 30px rgba(79,142,247,0.15)" }}>
            <div className="flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5" style={{ color: "#f59e0b" }} />
              <span className="text-white" style={{ fontWeight: 700, fontSize: "0.9rem" }}>Smart Study Tips</span>
            </div>
            <div className="space-y-3">
              {[
                { tip: "Study Hard subjects at your peak time (6-9 PM)", icon: "🧠" },
                { tip: "Limit sessions to 90 minutes for best retention", icon: "⏱️" },
                { tip: "Use active recall over passive re-reading", icon: "📝" },
                { tip: "Group similar subjects in the same session", icon: "📚" },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-xl" style={{ background: "rgba(255,255,255,0.06)" }}>
                  <span className="text-base">{item.icon}</span>
                  <p style={{ color: "#94a3b8", fontSize: "0.75rem", lineHeight: 1.5 }}>{item.tip}</p>
                </div>
              ))}
            </div>
          </div>

          {/* My Subjects */}
          <div className="rounded-2xl p-5" style={cardStyle}>
            <div className="flex items-center justify-between mb-4">
              <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "0.9rem" }}>My Subjects</h3>
              <span className="px-2 py-1 rounded-lg text-xs" style={{ background: `${colors.primary}18`, color: colors.primary, fontWeight: 600 }}>
                {subjects.length} total
              </span>
            </div>

            {subjects.length === 0 ? (
              <div className="text-center py-6">
                <BookOpen className="w-8 h-8 mx-auto mb-2" style={{ color: colors.textSecondary }} />
                <p style={{ color: colors.textSecondary, fontSize: "0.8rem" }}>No subjects yet. Add your first one!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {subjects.map((subject) => {
                  const progress = Math.min(100, Math.round((subject.completedHours / subject.totalHours) * 100));
                  const isEditing = editingId === subject.id;
                  return (
                    <div
                      key={subject.id}
                      className="p-3 rounded-xl transition-all duration-200"
                      style={{
                        background: isEditing ? `${colors.primary}0d` : colors.mutedBg,
                        border: `1.5px solid ${isEditing ? colors.primary : colors.cardBorder}`,
                      }}
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0" style={{ background: `${subject.color}15` }}>
                          {subject.emoji}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p style={{ fontWeight: 600, color: colors.textPrimary, fontSize: "0.825rem", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            {subject.name}
                          </p>
                          <div className="flex items-center gap-2">
                            <span style={{ color: colors.textSecondary, fontSize: "0.7rem" }}>{subject.completedHours}h / {subject.totalHours}h</span>
                            <span style={{
                              color: subject.difficulty === "Hard" ? "#ef4444" : subject.difficulty === "Medium" ? "#f59e0b" : "#10b981",
                              fontSize: "0.62rem", fontWeight: 600,
                              background: subject.difficulty === "Hard" ? "#fef2f2" : subject.difficulty === "Medium" ? "#fffbeb" : "#f0fdf4",
                              padding: "1px 5px", borderRadius: 999
                            }}>
                              {subject.difficulty}
                            </span>
                          </div>
                          <div className="mt-1.5 h-1.5 rounded-full" style={{ background: colors.cardBorder }}>
                            <div className="h-full rounded-full" style={{ width: `${progress}%`, background: subject.color }} />
                          </div>
                        </div>
                        <div className="flex items-center gap-1 flex-shrink-0">
                          <button
                            onClick={() => isEditing ? handleCancelEdit() : handleEdit(subject)}
                            className="w-7 h-7 rounded-lg flex items-center justify-center transition-all duration-200"
                            style={{ background: isEditing ? `${colors.primary}20` : "transparent" }}
                            title={isEditing ? "Cancel edit" : "Edit"}
                          >
                            {isEditing ? (
                              <X className="w-3.5 h-3.5" style={{ color: colors.primary }} />
                            ) : (
                              <Pencil className="w-3.5 h-3.5" style={{ color: colors.textSecondary }} />
                            )}
                          </button>
                          <button
                            onClick={() => deleteSubject(subject.id)}
                            className="w-7 h-7 rounded-lg flex items-center justify-center transition-all duration-200 hover:bg-red-50"
                            title="Delete"
                          >
                            <Trash2 className="w-3.5 h-3.5" style={{ color: "#cbd5e0" }} />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
