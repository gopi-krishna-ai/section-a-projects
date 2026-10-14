import { useState } from "react";
import { Link, useLocation } from "react-router";
import { Brain, Menu, X } from "lucide-react";

const navLinks = [
  { label: "Features", to: "/features" },
  { label: "Pricing", to: "/pricing" },
  { label: "About", to: "/about" },
  { label: "FAQ", to: "/faq" },
];

export function PublicNav() {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50" style={{ background: "rgba(255,255,255,0.92)", backdropFilter: "blur(12px)", borderBottom: "1px solid rgba(0,0,0,0.07)" }}>
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 no-underline">
          <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-4.5 h-4.5 text-white w-5 h-5" />
          </div>
          <span style={{ fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: "1rem", color: "#0f172a" }}>StudyAI</span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((l) => (
            <Link key={l.to} to={l.to} style={{ fontFamily: "Inter, sans-serif", fontWeight: 500, fontSize: "0.875rem", color: location.pathname === l.to ? "#4F8EF7" : "#64748b", textDecoration: "none", transition: "color 0.15s" }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.color = "#4F8EF7"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.color = location.pathname === l.to ? "#4F8EF7" : "#64748b"; }}
            >
              {l.label}
            </Link>
          ))}
        </div>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-3">
          <Link to="/login" style={{ fontFamily: "Inter, sans-serif", fontWeight: 500, fontSize: "0.875rem", color: "#475569", textDecoration: "none" }}>
            Log in
          </Link>
          <Link to="/signup" className="px-4 py-2 rounded-xl text-white no-underline" style={{ fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.875rem", background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", boxShadow: "0 4px 15px rgba(79,142,247,0.35)" }}>
            Get started free
          </Link>
        </div>

        {/* Mobile toggle */}
        <button onClick={() => setOpen(!open)} className="md:hidden p-2 rounded-lg" style={{ color: "#64748b" }}>
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden px-6 pb-4 space-y-2" style={{ background: "rgba(255,255,255,0.97)" }}>
          {navLinks.map((l) => (
            <Link key={l.to} to={l.to} onClick={() => setOpen(false)} className="block py-2 no-underline" style={{ fontFamily: "Inter, sans-serif", fontWeight: 500, fontSize: "0.875rem", color: "#475569" }}>
              {l.label}
            </Link>
          ))}
          <div className="flex flex-col gap-2 pt-2 border-t" style={{ borderColor: "#f1f5f9" }}>
            <Link to="/login" onClick={() => setOpen(false)} className="py-2 text-center rounded-xl no-underline" style={{ fontFamily: "Inter, sans-serif", fontWeight: 500, fontSize: "0.875rem", color: "#475569", border: "1px solid #e2e8f0" }}>
              Log in
            </Link>
            <Link to="/signup" onClick={() => setOpen(false)} className="py-2 text-center rounded-xl text-white no-underline" style={{ fontFamily: "Inter, sans-serif", fontWeight: 600, fontSize: "0.875rem", background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
              Get started free
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
