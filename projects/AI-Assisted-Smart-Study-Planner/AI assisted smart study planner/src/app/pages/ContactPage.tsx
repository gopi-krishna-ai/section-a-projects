import { useState } from "react";
import { Mail, MessageSquare, Clock, CheckCircle2 } from "lucide-react";

const topics = ["General inquiry", "Technical support", "Billing question", "Feature request", "Partnership", "Press inquiry", "Other"];
const contacts = [
  { icon: Mail, label: "Email", value: "hello@studyai.io", desc: "We reply within 24 hours" },
  { icon: MessageSquare, label: "Live Chat", value: "In-app chat", desc: "Mon–Fri, 9am–6pm EST" },
  { icon: Clock, label: "Response time", value: "< 24 hours", desc: "For all support tickets" },
];

export function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", topic: "General inquiry", message: "" });
  const [sent, setSent] = useState(false);
  const [sending, setSending] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSending(true);
    await new Promise(r => setTimeout(r, 1200));
    setSending(false);
    setSent(true);
  };

  const inputS: React.CSSProperties = { width: "100%", padding: "0.72rem 1rem", borderRadius: "0.75rem", outline: "none", background: "#f8faff", border: "1.5px solid #e2e8f0", fontFamily: "Inter, sans-serif", fontSize: "0.9rem", color: "#0f172a", boxSizing: "border-box", transition: "border-color 0.15s" };
  const focus = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; };
  const blur = (e: React.FocusEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => { e.target.style.border = "1.5px solid #e2e8f0"; e.target.style.background = "#f8faff"; };

  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Contact</p>
        <h1 style={{ fontWeight: 800, fontSize: "clamp(2rem, 5vw, 3rem)", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 16 }}>We'd love to hear from you</h1>
        <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: 480, margin: "0 auto" }}>Got a question, feedback, or issue? Our team is here to help.</p>
      </section>

      <section className="pb-24 px-6">
        <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Info */}
          <div className="space-y-5">
            {contacts.map(({ icon: Icon, label, value, desc }) => (
              <div key={label} className="p-5 rounded-2xl" style={{ border: "1px solid #e2e8f0", background: "#fff" }}>
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "#eff6ff" }}>
                    <Icon className="w-4.5 h-4.5 w-5 h-5" style={{ color: "#4F8EF7" }} />
                  </div>
                  <span style={{ fontWeight: 600, color: "#0f172a", fontSize: "0.9rem" }}>{label}</span>
                </div>
                <p style={{ fontWeight: 700, color: "#4F8EF7", fontSize: "0.95rem", marginBottom: 4 }}>{value}</p>
                <p style={{ color: "#64748b", fontSize: "0.8rem" }}>{desc}</p>
              </div>
            ))}
            <div className="p-5 rounded-2xl" style={{ background: "linear-gradient(135deg, #1e1b4b, #0f172a)" }}>
              <p style={{ fontWeight: 700, color: "#f8fafc", fontSize: "0.9rem", marginBottom: 6 }}>Student support</p>
              <p style={{ color: "#94a3b8", fontSize: "0.82rem", lineHeight: 1.6 }}>Have a .edu email? Email us at <span style={{ color: "#60a5fa" }}>students@studyai.io</span> for priority support and student discounts.</p>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-2 p-8 rounded-2xl" style={{ background: "#fff", border: "1px solid #e2e8f0", boxShadow: "0 8px 40px rgba(0,0,0,0.04)" }}>
            {!sent ? (
              <>
                <h2 style={{ fontWeight: 700, color: "#0f172a", fontSize: "1.25rem", marginBottom: 20 }}>Send us a message</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label style={{ color: "#374151", fontSize: "0.83rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Full name</label>
                      <input required value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Alex Johnson" style={inputS} onFocus={focus} onBlur={blur} />
                    </div>
                    <div>
                      <label style={{ color: "#374151", fontSize: "0.83rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Email address</label>
                      <input type="email" required value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="you@university.edu" style={inputS} onFocus={focus} onBlur={blur} />
                    </div>
                  </div>
                  <div>
                    <label style={{ color: "#374151", fontSize: "0.83rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Topic</label>
                    <select value={form.topic} onChange={e => setForm(f => ({ ...f, topic: e.target.value }))} style={{ ...inputS, appearance: "none", cursor: "pointer" }} onFocus={focus} onBlur={blur}>
                      {topics.map(t => <option key={t}>{t}</option>)}
                    </select>
                  </div>
                  <div>
                    <label style={{ color: "#374151", fontSize: "0.83rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Message</label>
                    <textarea required rows={5} value={form.message} onChange={e => setForm(f => ({ ...f, message: e.target.value }))} placeholder="Tell us how we can help…" style={{ ...inputS, resize: "vertical" as const, fontFamily: "Inter, sans-serif" }} onFocus={focus} onBlur={blur} />
                  </div>
                  <button type="submit" disabled={sending} className="w-full py-3.5 rounded-xl text-white font-bold flex items-center justify-center gap-2" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", fontSize: "0.95rem", boxShadow: "0 8px 24px rgba(79,142,247,0.3)" }}>
                    {sending ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Sending...</> : "Send message"}
                  </button>
                </form>
              </>
            ) : (
              <div className="text-center py-10">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5" style={{ background: "#f0fdf4" }}>
                  <CheckCircle2 className="w-8 h-8" style={{ color: "#10b981" }} />
                </div>
                <h3 style={{ fontWeight: 700, fontSize: "1.3rem", color: "#0f172a", marginBottom: 10 }}>Message sent!</h3>
                <p style={{ color: "#64748b", fontSize: "0.9rem", lineHeight: 1.7, maxWidth: 360, margin: "0 auto 20px" }}>Thanks for reaching out, {form.name}! We'll get back to you at <strong>{form.email}</strong> within 24 hours.</p>
                <button onClick={() => { setSent(false); setForm({ name: "", email: "", topic: "General inquiry", message: "" }); }} style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.875rem", background: "none", border: "none", cursor: "pointer" }}>Send another message</button>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
