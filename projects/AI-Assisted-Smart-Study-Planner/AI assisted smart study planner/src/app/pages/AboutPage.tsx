import { Link } from "react-router";
import { Brain, Heart, Target, Users, ArrowRight } from "lucide-react";

const team = [
  { name: "Jordan Kim", role: "Co-founder & CEO", initials: "JK", color: "#4F8EF7", bio: "Former teaching assistant and software engineer who struggled with study planning in college." },
  { name: "Priya Nair", role: "Co-founder & CTO", initials: "PN", color: "#7B61FF", bio: "AI researcher with a passion for applying machine learning to real-world education challenges." },
  { name: "Marcus Torres", role: "Head of Design", initials: "MT", color: "#10b981", bio: "UX designer focused on creating tools that make students' lives genuinely easier." },
  { name: "Aisha Okonkwo", role: "Head of Growth", initials: "AO", color: "#f59e0b", bio: "Education startup veteran who has helped over 200K students improve their academic performance." },
];

const values = [
  { icon: Brain, title: "Student-first", desc: "Every decision we make is guided by one question: does this help students study better?", color: "#4F8EF7" },
  { icon: Heart, title: "Genuine care", desc: "We care deeply about the wellbeing of the students we serve, not just their grades.", color: "#ef4444" },
  { icon: Target, title: "Measurable results", desc: "We're obsessed with building tools that produce real, demonstrable outcomes.", color: "#10b981" },
  { icon: Users, title: "Built in community", desc: "We co-design StudyAI with our users. Their feedback shapes every release.", color: "#7B61FF" },
];

export function AboutPage() {
  return (
    <div style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Hero */}
      <section className="py-20 px-6" style={{ background: "linear-gradient(180deg, #f8fafc, #fff)" }}>
        <div className="max-w-3xl mx-auto text-center">
          <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-7 h-7 text-white" />
          </div>
          <h1 style={{ fontWeight: 800, fontSize: "clamp(2rem, 5vw, 3.25rem)", color: "#0f172a", letterSpacing: "-0.02em", marginBottom: 20 }}>
            We're building the future of student success
          </h1>
          <p style={{ color: "#64748b", fontSize: "1.05rem", lineHeight: 1.8 }}>
            StudyAI was born from frustration. Our founders were students who spent more time trying to organize their studies than actually studying. We knew there had to be a better way — one powered by AI and built around how students actually learn.
          </p>
        </div>
      </section>

      {/* Story */}
      <section className="py-16 px-6" style={{ background: "#fff" }}>
        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <div>
            <p style={{ color: "#4F8EF7", fontWeight: 600, fontSize: "0.85rem", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 12 }}>Our story</p>
            <h2 style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a", marginBottom: 16 }}>Started in a library, built for the world</h2>
            <div className="space-y-4">
              {["In 2024, Jordan and Priya were both final-year students drowning in deadlines. Despite trying every study app and planner available, nothing seemed to help them manage their time intelligently.",
                "They started hacking together a simple script that analyzed their past study sessions and recommended when to study. It worked so well, they shared it with classmates — and the response was overwhelming.",
                "Today, StudyAI serves over 50,000 students across 30 countries, and we're just getting started. Our mission hasn't changed: help every student reach their academic potential."].map((p, i) => (
                <p key={i} style={{ color: "#64748b", fontSize: "0.95rem", lineHeight: 1.75 }}>{p}</p>
              ))}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {[
              { value: "2024", label: "Founded" }, { value: "50K+", label: "Students" },
              { value: "30+", label: "Countries" }, { value: "4.9★", label: "Rating" },
            ].map(({ value, label }) => (
              <div key={label} className="p-6 rounded-2xl text-center" style={{ background: "#f8fafc", border: "1px solid #e2e8f0" }}>
                <p style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a", lineHeight: 1 }}>{value}</p>
                <p style={{ color: "#64748b", fontSize: "0.82rem", marginTop: 4 }}>{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-16 px-6" style={{ background: "#f8fafc" }}>
        <div className="max-w-5xl mx-auto">
          <h2 className="text-center mb-12" style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a" }}>What we stand for</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map(({ icon: Icon, title, desc, color }) => (
              <div key={title} className="p-6 rounded-2xl" style={{ background: "#fff", border: "1px solid #e2e8f0" }}>
                <div className="w-10 h-10 rounded-xl flex items-center justify-center mb-4" style={{ background: `${color}15` }}>
                  <Icon className="w-5 h-5" style={{ color }} />
                </div>
                <h3 style={{ fontWeight: 700, color: "#0f172a", fontSize: "0.95rem", marginBottom: 8 }}>{title}</h3>
                <p style={{ color: "#64748b", fontSize: "0.83rem", lineHeight: 1.65 }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-16 px-6" style={{ background: "#fff" }}>
        <div className="max-w-5xl mx-auto">
          <h2 className="text-center mb-12" style={{ fontWeight: 800, fontSize: "2rem", color: "#0f172a" }}>Meet the team</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {team.map(({ name, role, initials, color, bio }) => (
              <div key={name} className="p-6 rounded-2xl text-center" style={{ border: "1px solid #e2e8f0" }}>
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4 text-white" style={{ background: `linear-gradient(135deg, ${color}, ${color}aa)`, fontWeight: 700, fontSize: "1rem" }}>{initials}</div>
                <p style={{ fontWeight: 700, color: "#0f172a", fontSize: "0.95rem" }}>{name}</p>
                <p style={{ color, fontSize: "0.8rem", fontWeight: 500, marginBottom: 10 }}>{role}</p>
                <p style={{ color: "#64748b", fontSize: "0.8rem", lineHeight: 1.6 }}>{bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 text-center" style={{ background: "linear-gradient(135deg, #1e1b4b, #0f172a)" }}>
        <h2 style={{ fontWeight: 800, fontSize: "2rem", color: "#f8fafc", marginBottom: 12 }}>Join us on this mission</h2>
        <p style={{ color: "#94a3b8", marginBottom: 28, fontSize: "1rem" }}>Help us build the future of learning. Start for free today.</p>
        <Link to="/signup" className="inline-flex items-center gap-2 px-8 py-3.5 rounded-2xl text-white no-underline font-bold" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
          Get started <ArrowRight className="w-4 h-4" />
        </Link>
      </section>
    </div>
  );
}
