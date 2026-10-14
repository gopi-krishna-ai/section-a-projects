import { Link } from "react-router";
import { Brain, Twitter, Github, Linkedin } from "lucide-react";

const cols = [
  { heading: "Product", links: [{ label: "Features", to: "/features" }, { label: "Pricing", to: "/pricing" }, { label: "Changelog", to: "#" }, { label: "Roadmap", to: "#" }] },
  { heading: "Company", links: [{ label: "About", to: "/about" }, { label: "Blog", to: "#" }, { label: "Careers", to: "#" }, { label: "Contact", to: "/contact" }] },
  { heading: "Resources", links: [{ label: "FAQ", to: "/faq" }, { label: "Help Center", to: "#" }, { label: "Community", to: "#" }, { label: "Status", to: "#" }] },
  { heading: "Legal", links: [{ label: "Privacy Policy", to: "/privacy" }, { label: "Terms of Service", to: "/terms" }, { label: "Cookie Policy", to: "#" }] },
];

export function PublicFooter() {
  return (
    <footer style={{ background: "#0f172a", fontFamily: "Inter, sans-serif" }}>
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-10">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
                <Brain className="w-4 h-4 text-white" />
              </div>
              <span style={{ fontWeight: 700, fontSize: "1rem", color: "#f8fafc" }}>StudyAI</span>
            </div>
            <p style={{ color: "#64748b", fontSize: "0.8rem", lineHeight: 1.7, maxWidth: 200 }}>
              AI-powered study planning that helps students achieve their academic goals.
            </p>
            <div className="flex items-center gap-3 mt-5">
              {[Twitter, Github, Linkedin].map((Icon, i) => (
                <a key={i} href="#" className="w-8 h-8 rounded-lg flex items-center justify-center transition-all" style={{ background: "rgba(255,255,255,0.06)" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "rgba(79,142,247,0.2)"; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "rgba(255,255,255,0.06)"; }}
                >
                  <Icon className="w-4 h-4" style={{ color: "#94a3b8" }} />
                </a>
              ))}
            </div>
          </div>

          {/* Link columns */}
          {cols.map((col) => (
            <div key={col.heading}>
              <p style={{ fontWeight: 600, fontSize: "0.8rem", color: "#f1f5f9", marginBottom: "1rem", letterSpacing: "0.05em", textTransform: "uppercase" }}>{col.heading}</p>
              <ul className="space-y-2.5 list-none p-0 m-0">
                {col.links.map((l) => (
                  <li key={l.label}>
                    <Link to={l.to} style={{ color: "#64748b", fontSize: "0.85rem", textDecoration: "none", transition: "color 0.15s" }}
                      onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.color = "#94a3b8"; }}
                      onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.color = "#64748b"; }}
                    >
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-6 flex flex-col md:flex-row items-center justify-between gap-4" style={{ borderTop: "1px solid rgba(255,255,255,0.07)" }}>
          <p style={{ color: "#475569", fontSize: "0.8rem" }}>© 2026 StudyAI. All rights reserved.</p>
          <p style={{ color: "#475569", fontSize: "0.8rem" }}>Made with ❤️ for students everywhere</p>
        </div>
      </div>
    </footer>
  );
}
