import { Link } from "react-router";
import { Brain, Calendar, Timer, FileText, BarChart3, Zap, CheckCircle2, ArrowRight, Shield, Users } from "lucide-react";

const features = [
  {
    icon: Brain, title: "AI Study Plans", color: "#4F8EF7", bg: "#eff6ff",
    desc: "Our AI analyzes your subjects, workload, and deadlines to generate a personalized daily study schedule. It adapts every week based on your progress.",
    points: ["Subject difficulty analysis", "Deadline-aware scheduling", "Weekly plan regeneration", "Study time optimization"],
  },
  {
    icon: Zap, title: "Productivity Prediction", color: "#7B61FF", bg: "#f5f3ff",
    desc: "StudyAI learns when you study best by analyzing your session data over time. It then schedules the hardest subjects during your peak hours.",
    points: ["Hourly focus pattern detection", "Subject-time recommendations", "Distraction risk alerts", "Weekly improvement insights"],
  },
  {
    icon: Calendar, title: "Smart Calendar", color: "#10b981", bg: "#f0fdf4",
    desc: "A full-featured academic calendar that shows your exams, assignments, and study sessions side by side. Never miss a deadline again.",
    points: ["Month, week, and day views", "Exam and assignment tracking", "Color-coded event types", "Drag-and-drop scheduling"],
  },
  {
    icon: Timer, title: "Pomodoro Timer", color: "#f59e0b", bg: "#fffbeb",
    desc: "Research-backed timed study sessions with customizable focus and break intervals. Track your focus history and productivity statistics.",
    points: ["Custom focus/break durations", "Session history tracking", "Focus streak counter", "Browser notifications"],
  },
  {
    icon: FileText, title: "Smart Notes", color: "#ef4444", bg: "#fef2f2",
    desc: "A distraction-free note editor organized by subject. Full-text search, tagging, and word count make your notes effortless to use.",
    points: ["Markdown-aware editor", "Subject organization", "Full-text search", "Tags and filtering"],
  },
  {
    icon: BarChart3, title: "Deep Analytics", color: "#06b6d4", bg: "#f0fdff",
    desc: "Comprehensive charts on every aspect of your study habits. Understand where your time goes and how to optimize your routine.",
    points: ["Study hours over time", "Subject performance scores", "Productivity trend analysis", "Radar skill assessment"],
  },
];

export function FeaturesPage() {
  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Features</p>
        <h1 style={{ fontWeight: 800, fontSize: "clamp(2rem, 5vw, 3.25rem)", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 16 }}>
          Everything you need to excel
        </h1>
        <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: 520, margin: "0 auto 32px" }}>
          Purpose-built features for students who want results, not just another task manager.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          {[Shield, Users, Zap].map((Icon, i) => (
            <div key={i} className="flex items-center gap-2 px-4 py-2 rounded-full" style={{ background: "#f1f5f9", border: "1px solid #e2e8f0" }}>
              <Icon className="w-4 h-4" style={{ color: "#4F8EF7" }} />
              <span style={{ color: "#374151", fontSize: "0.82rem", fontWeight: 500 }}>{["FERPA Compliant", "50K+ Students", "AI-Powered"][i]}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 pb-24">
        <div className="max-w-6xl mx-auto space-y-16">
          {features.map(({ icon: Icon, title, color, bg, desc, points }, i) => (
            <div key={title} className={`grid grid-cols-1 lg:grid-cols-2 gap-12 items-center ${i % 2 === 1 ? "lg:flex-row-reverse" : ""}`}>
              <div className={i % 2 === 1 ? "lg:order-2" : ""}>
                <div className="w-12 h-12 rounded-2xl flex items-center justify-center mb-5" style={{ background: bg }}>
                  <Icon className="w-6 h-6" style={{ color }} />
                </div>
                <h2 style={{ fontWeight: 800, fontSize: "1.8rem", color: "#0f172a", letterSpacing: "-0.01em", marginBottom: 12 }}>{title}</h2>
                <p style={{ color: "#64748b", fontSize: "1rem", lineHeight: 1.75, marginBottom: 20 }}>{desc}</p>
                <ul className="space-y-3 list-none p-0 m-0 mb-6">
                  {points.map(p => (
                    <li key={p} className="flex items-center gap-2.5">
                      <CheckCircle2 className="w-4 h-4 flex-shrink-0" style={{ color }} />
                      <span style={{ color: "#374151", fontSize: "0.9rem" }}>{p}</span>
                    </li>
                  ))}
                </ul>
                <Link to="/signup" className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-white no-underline text-sm font-semibold" style={{ background: `linear-gradient(135deg, ${color}, ${color}bb)` }}>
                  Try it free <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
              <div className={`rounded-2xl p-8 flex items-center justify-center min-h-52 ${i % 2 === 1 ? "lg:order-1" : ""}`} style={{ background: bg, border: `1px solid ${color}22` }}>
                <div className="text-center">
                  <div className="w-20 h-20 rounded-3xl flex items-center justify-center mx-auto mb-4" style={{ background: `linear-gradient(135deg, ${color}, ${color}aa)`, boxShadow: `0 12px 40px ${color}40` }}>
                    <Icon className="w-10 h-10 text-white" />
                  </div>
                  <p style={{ fontWeight: 700, color: "#0f172a", fontSize: "1.1rem" }}>{title}</p>
                  <p style={{ color, fontSize: "0.82rem", marginTop: 4, fontWeight: 500 }}>Included in all plans</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(135deg, #1e1b4b, #0f172a)" }}>
        <h2 style={{ fontWeight: 800, fontSize: "2.25rem", color: "#f8fafc", marginBottom: 12 }}>See all features in action</h2>
        <p style={{ color: "#94a3b8", fontSize: "1rem", marginBottom: 28 }}>Start your free account and explore the full platform today.</p>
        <Link to="/signup" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl text-white no-underline font-bold" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", boxShadow: "0 8px 30px rgba(79,142,247,0.35)" }}>
          Get started free <ArrowRight className="w-4 h-4" />
        </Link>
      </section>
    </div>
  );
}
