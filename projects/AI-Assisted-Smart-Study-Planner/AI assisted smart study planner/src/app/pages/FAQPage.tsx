import { useState } from "react";
import { Link } from "react-router";
import { ChevronDown, MessageSquare } from "lucide-react";

const categories = [
  {
    name: "Getting started",
    questions: [
      { q: "What is StudyAI?", a: "StudyAI is an AI-powered study planning platform for students. It generates personalized study plans, tracks your tasks, analyzes your productivity, and helps you manage your academic schedule in one place." },
      { q: "How do I get started?", a: "Sign up for free, add your subjects and upcoming exams, and let the AI generate your first study plan. The whole setup takes under 5 minutes." },
      { q: "Is StudyAI free to use?", a: "Yes! We have a generous Free plan that includes up to 3 subjects, a basic task tracker, and a Pomodoro timer. For more features, check out our Pro plan." },
      { q: "Do I need to install anything?", a: "No. StudyAI is entirely web-based. Just visit app.studyai.io in any modern browser. Mobile apps for iOS and Android are coming soon." },
    ],
  },
  {
    name: "AI features",
    questions: [
      { q: "How does the AI study plan work?", a: "When you add your subjects and deadlines, our AI analyzes your workload, subject difficulty, and time available to generate a day-by-day study schedule. It updates every week based on your progress." },
      { q: "How accurate is the productivity prediction?", a: "Productivity prediction improves over time as the AI learns your patterns. After 2–3 weeks of regular use, most students report the predictions are 85–90% accurate for their peak focus hours." },
      { q: "Can I edit the AI-generated plan?", a: "Absolutely. The AI plan is a starting point. You can drag, edit, or delete any session from the calendar. The AI will take your changes into account in future plan generations." },
    ],
  },
  {
    name: "Account & billing",
    questions: [
      { q: "How do I upgrade to Pro?", a: "Go to Settings → Billing and click 'Upgrade to Pro'. We accept all major credit cards and PayPal. Your upgrade is instant." },
      { q: "Can I cancel anytime?", a: "Yes. Cancel anytime from Settings → Billing. If you cancel, you keep Pro until the end of your current billing period, then move to the Free plan automatically." },
      { q: "Do you offer student discounts?", a: "Yes! Students with a valid .edu email address get 30% off the Pro plan. Email students@studyai.io from your .edu address to get your discount code." },
      { q: "Is my data private?", a: "Absolutely. We never sell your data. Your study data is encrypted and stored securely. See our Privacy Policy for full details." },
    ],
  },
  {
    name: "Technical",
    questions: [
      { q: "Which browsers are supported?", a: "StudyAI works on all modern browsers: Chrome, Firefox, Safari, Edge, and Brave. We recommend Chrome or Edge for the best experience." },
      { q: "Can I export my data?", a: "Yes. Pro users can export all their data (tasks, notes, analytics) as CSV or PDF from Settings → Data & Privacy." },
      { q: "Is there an API?", a: "Not yet, but it's on our roadmap. If you're a developer interested in building on top of StudyAI, email api@studyai.io." },
    ],
  },
];

function FAQItem({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b" style={{ borderColor: "#f1f5f9" }}>
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between py-4 text-left gap-4">
        <span style={{ fontWeight: 600, color: "#0f172a", fontSize: "0.925rem", lineHeight: 1.5 }}>{q}</span>
        <ChevronDown className="w-5 h-5 flex-shrink-0 transition-transform duration-200" style={{ color: "#64748b", transform: open ? "rotate(180deg)" : "none" }} />
      </button>
      {open && <p style={{ color: "#64748b", fontSize: "0.875rem", lineHeight: 1.75, paddingBottom: 16 }}>{a}</p>}
    </div>
  );
}

export function FAQPage() {
  const [activeCategory, setActiveCategory] = useState("Getting started");

  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>FAQ</p>
        <h1 style={{ fontWeight: 800, fontSize: "clamp(2rem, 5vw, 3rem)", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 16 }}>Frequently asked questions</h1>
        <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: 460, margin: "0 auto" }}>Can't find your answer? <Link to="/contact" style={{ color: "#4F8EF7", textDecoration: "none", fontWeight: 600 }}>Contact support →</Link></p>
      </section>

      <section className="pb-24 px-6">
        <div className="max-w-4xl mx-auto">
          {/* Category tabs */}
          <div className="flex flex-wrap gap-2 mb-8 justify-center">
            {categories.map(c => (
              <button key={c.name} onClick={() => setActiveCategory(c.name)} className="px-4 py-2 rounded-xl text-sm transition-all" style={{ background: activeCategory === c.name ? "linear-gradient(135deg, #4F8EF7, #7B61FF)" : "#f8fafc", color: activeCategory === c.name ? "#fff" : "#64748b", fontWeight: activeCategory === c.name ? 600 : 400, border: activeCategory === c.name ? "none" : "1px solid #e2e8f0" }}>
                {c.name}
              </button>
            ))}
          </div>

          {/* Questions */}
          <div className="rounded-2xl p-6" style={{ background: "#fff", border: "1px solid #e2e8f0" }}>
            {categories.find(c => c.name === activeCategory)?.questions.map(({ q, a }) => (
              <FAQItem key={q} q={q} a={a} />
            ))}
          </div>

          {/* Still need help */}
          <div className="mt-10 p-6 rounded-2xl text-center" style={{ background: "linear-gradient(135deg, #eff6ff, #f5f3ff)", border: "1px solid #e0e7ff" }}>
            <MessageSquare className="w-8 h-8 mx-auto mb-3" style={{ color: "#4F8EF7" }} />
            <h3 style={{ fontWeight: 700, color: "#0f172a", fontSize: "1.05rem", marginBottom: 6 }}>Still have questions?</h3>
            <p style={{ color: "#64748b", fontSize: "0.875rem", marginBottom: 16 }}>Our support team typically responds within a few hours.</p>
            <Link to="/contact" className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-white no-underline text-sm font-semibold" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
              Contact support
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
