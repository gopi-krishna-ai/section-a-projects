import { useState, useEffect } from "react";
import { Plus, Search, Trash2, Tag, Clock, FileText, Save } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useStudyData } from "../context/StudyDataContext";

export function NotesPage() {
  const { colors } = useTheme();
  const { notes, addNote, updateNote, deleteNote, subjects } = useStudyData();

  const [selectedId, setSelectedId] = useState<string | null>(notes[0]?.id || null);
  const [search, setSearch] = useState("");
  const [subjectFilter, setSubjectFilter] = useState("All");
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [editTags, setEditTags] = useState("");
  const [saved, setSaved] = useState(false);
  const [unsaved, setUnsaved] = useState(false);

  const selectedNote = notes.find(n => n.id === selectedId) || null;

  useEffect(() => {
    if (selectedNote) {
      setEditTitle(selectedNote.title);
      setEditContent(selectedNote.content);
      setEditTags(selectedNote.tags.join(", "));
      setUnsaved(false);
    }
  }, [selectedId]);

  const filtered = notes.filter(n => {
    const matchSearch = n.title.toLowerCase().includes(search.toLowerCase()) || n.content.toLowerCase().includes(search.toLowerCase());
    const matchSubject = subjectFilter === "All" || n.subject === subjectFilter;
    return matchSearch && matchSubject;
  }).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));

  const handleSave = () => {
    if (!selectedId) return;
    updateNote(selectedId, { title: editTitle, content: editContent, tags: editTags.split(",").map(t => t.trim()).filter(Boolean) });
    setSaved(true);
    setUnsaved(false);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleNewNote = () => {
    addNote({ title: "Untitled Note", content: "", subject: subjects[0]?.name || "General", subjectColor: subjects[0]?.color || "#4F8EF7", tags: [] });
    setTimeout(() => {
      const newNote = notes[0];
      if (newNote) setSelectedId(newNote.id);
    }, 0);
  };

  const handleChange = (field: "title" | "content" | "tags", val: string) => {
    if (field === "title") setEditTitle(val);
    if (field === "content") setEditContent(val);
    if (field === "tags") setEditTags(val);
    setUnsaved(true);
  };

  const allSubjects = ["All", ...Array.from(new Set(notes.map(n => n.subject)))];

  const card: React.CSSProperties = { background: colors.cardBg, border: `1px solid ${colors.cardBorder}` };
  const inputS: React.CSSProperties = { background: colors.inputBg, border: `1.5px solid ${colors.inputBorder}`, color: colors.textPrimary, fontFamily: "Inter, sans-serif", outline: "none", borderRadius: "0.75rem", padding: "0.65rem 0.9rem", fontSize: "0.875rem", width: "100%", boxSizing: "border-box" };

  return (
    <div style={{ fontFamily: "Inter, sans-serif", height: "calc(100vh - 5rem)" }} className="flex gap-5">
      {/* Left: Note list */}
      <div className="w-72 flex-shrink-0 flex flex-col rounded-2xl overflow-hidden" style={card}>
        {/* Search + new */}
        <div className="p-4 border-b" style={{ borderColor: colors.cardBorder }}>
          <div className="flex items-center gap-2 mb-3">
            <div className="flex-1 flex items-center gap-2 px-3 py-2 rounded-xl" style={{ background: colors.mutedBg, border: `1px solid ${colors.cardBorder}` }}>
              <Search className="w-4 h-4 flex-shrink-0" style={{ color: colors.textSecondary }} />
              <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search notes…" style={{ background: "transparent", border: "none", outline: "none", fontFamily: "Inter, sans-serif", fontSize: "0.82rem", color: colors.textPrimary, width: "100%" }} />
            </div>
            <button onClick={handleNewNote} className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 transition-all" style={{ background: colors.gradient, color: "#fff" }}>
              <Plus className="w-4 h-4" />
            </button>
          </div>
          {/* Subject filter */}
          <div className="flex gap-1 overflow-x-auto pb-1">
            {allSubjects.map(s => (
              <button key={s} onClick={() => setSubjectFilter(s)} className="px-2.5 py-1 rounded-lg flex-shrink-0 text-xs transition-all" style={{ background: subjectFilter === s ? colors.gradient : colors.mutedBg, color: subjectFilter === s ? "#fff" : colors.textSecondary, fontWeight: subjectFilter === s ? 600 : 400 }}>
                {s === "All" ? "All" : s.split(" ")[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Notes list */}
        <div className="flex-1 overflow-y-auto">
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full p-6 text-center">
              <FileText className="w-8 h-8 mb-3" style={{ color: colors.textSecondary }} />
              <p style={{ color: colors.textSecondary, fontSize: "0.82rem" }}>No notes found</p>
              <button onClick={handleNewNote} className="mt-3 px-4 py-2 rounded-xl text-white text-xs font-semibold" style={{ background: colors.gradient }}>Create first note</button>
            </div>
          ) : filtered.map(note => (
            <button key={note.id} onClick={() => setSelectedId(note.id)}
              className="w-full text-left p-4 border-b transition-all"
              style={{ background: selectedId === note.id ? `${colors.primary}12` : "transparent", borderColor: colors.cardBorder, borderLeft: selectedId === note.id ? `3px solid ${colors.primary}` : "3px solid transparent" }}
            >
              <p style={{ fontWeight: 600, fontSize: "0.82rem", color: colors.textPrimary, lineHeight: 1.3, marginBottom: 4, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{note.title || "Untitled"}</p>
              <p style={{ color: colors.textSecondary, fontSize: "0.72rem", lineHeight: 1.4, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" as const }}>{note.content.replace(/^#+\s/gm, "").replace(/\*\*/g, "") || "No content"}</p>
              <div className="flex items-center justify-between mt-2">
                <span className="px-2 py-0.5 rounded text-xs" style={{ background: note.subjectColor + "20", color: note.subjectColor, fontWeight: 600 }}>{note.subject.split(" ")[0]}</span>
                <span style={{ color: colors.textSecondary, fontSize: "0.65rem" }}>
                  <Clock className="w-2.5 h-2.5 inline mr-0.5" />
                  {new Date(note.updatedAt + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" })}
                </span>
              </div>
            </button>
          ))}
        </div>

        <div className="p-3 border-t" style={{ borderColor: colors.cardBorder }}>
          <p style={{ color: colors.textSecondary, fontSize: "0.72rem", textAlign: "center" }}>{notes.length} notes</p>
        </div>
      </div>

      {/* Right: Editor */}
      <div className="flex-1 rounded-2xl flex flex-col overflow-hidden" style={card}>
        {selectedNote ? (
          <>
            {/* Toolbar */}
            <div className="flex items-center justify-between px-6 py-3.5 border-b" style={{ borderColor: colors.cardBorder }}>
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full" style={{ background: selectedNote.subjectColor }} />
                <select value={selectedNote.subject} onChange={e => updateNote(selectedNote.id, { subject: e.target.value })}
                  style={{ background: "transparent", border: "none", color: colors.textSecondary, fontFamily: "Inter, sans-serif", fontSize: "0.8rem", outline: "none", cursor: "pointer" }}>
                  {subjects.map(s => <option key={s.id} value={s.name}>{s.name}</option>)}
                </select>
                {unsaved && <span style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>• Unsaved changes</span>}
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => { if (selectedNote && window.confirm("Delete this note?")) { deleteNote(selectedNote.id); setSelectedId(notes.find(n => n.id !== selectedNote.id)?.id || null); } }}
                  className="w-8 h-8 rounded-lg flex items-center justify-center transition-all" style={{ color: colors.textSecondary }}
                  onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = "#fef2f2"; (e.currentTarget as HTMLElement).style.color = "#ef4444"; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = "transparent"; (e.currentTarget as HTMLElement).style.color = colors.textSecondary; }}
                >
                  <Trash2 className="w-4 h-4" />
                </button>
                <button onClick={handleSave} className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-white text-sm font-semibold transition-all" style={{ background: saved ? "#10b981" : colors.gradient }}>
                  <Save className="w-3.5 h-3.5" />
                  {saved ? "Saved!" : "Save"}
                </button>
              </div>
            </div>

            {/* Title */}
            <div className="px-6 pt-5">
              <input value={editTitle} onChange={e => handleChange("title", e.target.value)} placeholder="Note title…"
                style={{ width: "100%", background: "transparent", border: "none", outline: "none", fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: "1.5rem", color: colors.textPrimary, boxSizing: "border-box" }}
                onKeyDown={e => { if (e.key === "Enter") { e.preventDefault(); (document.getElementById("note-content") as HTMLTextAreaElement)?.focus(); } }}
              />
              {/* Tags */}
              <div className="flex items-center gap-2 mt-3 pb-4 border-b" style={{ borderColor: colors.cardBorder }}>
                <Tag className="w-3.5 h-3.5 flex-shrink-0" style={{ color: colors.textSecondary }} />
                <input value={editTags} onChange={e => handleChange("tags", e.target.value)} placeholder="Add tags, comma-separated…"
                  style={{ background: "transparent", border: "none", outline: "none", fontFamily: "Inter, sans-serif", fontSize: "0.8rem", color: colors.textSecondary, flex: 1 }}
                />
                {selectedNote.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {selectedNote.tags.map(t => (
                      <span key={t} className="px-2 py-0.5 rounded-full text-xs" style={{ background: `${colors.primary}18`, color: colors.primary, fontWeight: 500 }}>#{t}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Content */}
            <textarea id="note-content" value={editContent} onChange={e => handleChange("content", e.target.value)}
              placeholder="Start writing your notes here…&#10;&#10;You can use markdown formatting:&#10;## Headings  |  **bold**  |  - lists"
              style={{ flex: 1, width: "100%", padding: "1.25rem 1.5rem", background: "transparent", border: "none", outline: "none", resize: "none", fontFamily: "Inter, 'SF Mono', monospace", fontSize: "0.9rem", color: colors.textPrimary, lineHeight: 1.8, boxSizing: "border-box" }}
            />

            {/* Footer */}
            <div className="px-6 py-2.5 border-t flex items-center justify-between" style={{ borderColor: colors.cardBorder }}>
              <span style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>{editContent.split(/\s+/).filter(Boolean).length} words · {editContent.length} chars</span>
              <span style={{ color: colors.textSecondary, fontSize: "0.72rem" }}>
                Updated {new Date(selectedNote.updatedAt + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
              </span>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5" style={{ background: colors.mutedBg }}>
              <FileText className="w-8 h-8" style={{ color: colors.textSecondary }} />
            </div>
            <h3 style={{ fontWeight: 700, color: colors.textPrimary, fontSize: "1.1rem", marginBottom: 8 }}>Select a note</h3>
            <p style={{ color: colors.textSecondary, fontSize: "0.875rem", marginBottom: 20, maxWidth: 280 }}>Choose a note from the list, or create a new one to start writing.</p>
            <button onClick={handleNewNote} className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-white font-semibold" style={{ background: colors.gradient }}>
              <Plus className="w-4 h-4" /> New note
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
