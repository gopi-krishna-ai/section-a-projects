import { Link } from "react-router";
import { CheckCircle2, X, Zap, ArrowRight } from "lucide-react";

const plans = [
  {
    name: "Free", price: 0, period: "forever", color: "#64748b",
    desc: "Perfect for getting started",
    features: ["3 active subjects", "Basic task tracker", "Pomodoro timer (25/5)", "7-day analytics history", "5 notes", "Email support"],
    missing: ["AI study plans", "Full analytics", "Unlimited notes", "Calendar sync", "Priority support"],
    cta: "Get started free", highlight: false,
  },
  {
    name: "Pro", price: 9, period: "month", color: "#4F8EF7",
    desc: "For serious students",
    features: ["Unlimited subjects", "AI-generated study plans", "Full analytics & charts", "Unlimited notes & tags", "Calendar (daily/weekly/monthly)", "Pomodoro with custom timers", "Data export (CSV/PDF)", "Priority email support"],
    missing: ["Group study sessions", "Admin dashboard"],
    cta: "Start 14-day free trial", highlight: true,
  },
  {
    name: "Team", price: 19, period: "month", color: "#7B61FF",
    desc: "For study groups & institutions",
    features: ["Everything in Pro", "Up to 10 members", "Shared notes & resources", "Group Pomodoro sessions", "Progress reports for all members", "Admin dashboard", "Custom branding", "Dedicated account manager"],
    missing: [],
    cta: "Contact sales", highlight: false,
  },
];

const faqs = [
  { q: "Is there a free trial?", a: "Yes! Pro comes with a 14-day free trial. No credit card required to start." },
  { q: "Can I cancel anytime?", a: "Absolutely. Cancel any time from your account settings. No hidden fees or penalties." },
  { q: "What happens to my data if I downgrade?", a: "Your data is safe. You'll have read-only access to content beyond the Free plan limits." },
  { q: "Do you offer student discounts?", a: "Yes! Students with a .edu email get 30% off Pro. Email us at students@studyai.io." },
];

export function PricingPage() {
  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Header */}
      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(180deg, #f8fafc 0%, #fff 100%)" }}>
        <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Pricing</p>
        <h1 style={{ fontWeight: 800, fontSize: "clamp(2rem, 5vw, 3.25rem)", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 16 }}>Simple, honest pricing</h1>
        <p style={{ color: "#64748b", fontSize: "1.05rem", maxWidth: 500, margin: "0 auto" }}>Start free. Upgrade when you need more. No tricks, no hidden fees.</p>
      </section>

      {/* Plans */}
      <section className="px-6 pb-20">
        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map(({ name, price, period, color, desc, features, missing, cta, highlight }) => (
            <div key={name} className="rounded-2xl p-7 flex flex-col relative" style={{ background: highlight ? "linear-gradient(135deg, #1e1b4b, #0f172a)" : "#fff", border: highlight ? "2px solid #4F8EF7" : "1px solid #e2e8f0", boxShadow: highlight ? "0 24px 60px rgba(79,142,247,0.2)" : "0 4px 20px rgba(0,0,0,0.04)" }}>
              {highlight && <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full text-white text-xs font-bold" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>Most popular</div>}
              <div className="mb-6">
                <p style={{ fontWeight: 700, fontSize: "1.1rem", color: highlight ? "#f8fafc" : "#0f172a", marginBottom: 4 }}>{name}</p>
                <p style={{ color: highlight ? "#94a3b8" : "#64748b", fontSize: "0.83rem", marginBottom: 16 }}>{desc}</p>
                <div className="flex items-end gap-1">
                  <span style={{ fontWeight: 800, fontSize: "2.8rem", color: highlight ? "#fff" : "#0f172a", lineHeight: 1 }}>${price}</span>
                  <span style={{ color: highlight ? "#94a3b8" : "#64748b", fontSize: "0.85rem", marginBottom: 4 }}>/{period}</span>
                </div>
              </div>
              <Link to="/signup" className="block text-center py-3 rounded-xl no-underline mb-6" style={{ fontWeight: 700, fontSize: "0.9rem", background: highlight ? "linear-gradient(135deg, #4F8EF7, #7B61FF)" : "transparent", color: highlight ? "#fff" : color, border: highlight ? "none" : `2px solid ${color}30`, boxShadow: highlight ? "0 8px 24px rgba(79,142,247,0.35)" : "none" }}>
                {cta}
              </Link>
              <div className="space-y-2.5 flex-1">
                {features.map(f => (
                  <div key={f} className="flex items-start gap-2.5">
                    <CheckCircle2 className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: highlight ? "#60a5fa" : color }} />
                    <span style={{ color: highlight ? "#cbd5e1" : "#374151", fontSize: "0.85rem" }}>{f}</span>
                  </div>
                ))}
                {missing.map(f => (
                  <div key={f} className="flex items-start gap-2.5">
                    <X className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color: "#94a3b8" }} />
                    <span style={{ color: "#94a3b8", fontSize: "0.85rem" }}>{f}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 px-6" style={{ background: "#f8fafc" }}>
        <div className="max-w-2xl mx-auto">
          <h2 className="text-center mb-12" style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a" }}>Pricing FAQs</h2>
          <div className="space-y-4">
            {faqs.map(({ q, a }) => (
              <div key={q} className="p-5 rounded-2xl" style={{ background: "#fff", border: "1px solid #e2e8f0" }}>
                <p style={{ fontWeight: 600, color: "#0f172a", marginBottom: 8, fontSize: "0.95rem" }}>{q}</p>
                <p style={{ color: "#64748b", fontSize: "0.875rem", lineHeight: 1.65 }}>{a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 text-center" style={{ background: "#fff" }}>
        <Zap className="w-10 h-10 mx-auto mb-5" style={{ color: "#4F8EF7" }} />
        <h2 style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a", marginBottom: 12 }}>Ready to study smarter?</h2>
        <p style={{ color: "#64748b", fontSize: "1rem", marginBottom: 28 }}>Join thousands of students already using StudyAI for free.</p>
        <Link to="/signup" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl text-white no-underline" style={{ fontWeight: 700, background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", boxShadow: "0 8px 30px rgba(79,142,247,0.3)", fontSize: "1rem" }}>
          Get started free <ArrowRight className="w-4 h-4" />
        </Link>
      </section>
    </div>
  );
}
