import { Link } from "react-router";
import { Brain, ArrowLeft, Home, Search } from "lucide-react";

export function NotFoundPage() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6" style={{ background: "linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%)", fontFamily: "Inter, sans-serif" }}>
      <div className="text-center max-w-lg">
        {/* Animated icon */}
        <div className="relative w-24 h-24 mx-auto mb-8">
          <div className="w-24 h-24 rounded-3xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", boxShadow: "0 16px 48px rgba(79,142,247,0.3)" }}>
            <Brain className="w-12 h-12 text-white" />
          </div>
          <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full flex items-center justify-center text-white" style={{ background: "#ef4444", fontSize: "1rem", fontWeight: 700 }}>?</div>
        </div>

        {/* 404 number */}
        <div className="mb-4" style={{ fontWeight: 900, fontSize: "7rem", lineHeight: 1, letterSpacing: "-0.04em", background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
          404
        </div>

        <h1 style={{ fontWeight: 800, fontSize: "1.75rem", color: "#0f172a", marginBottom: 12 }}>
          Oops — page not found
        </h1>
        <p style={{ color: "#64748b", fontSize: "1rem", lineHeight: 1.7, marginBottom: 32 }}>
          Looks like your study plan didn't include this page. Don't worry — even the best AI gets lost sometimes. Let's get you back on track.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link to="/" className="flex items-center gap-2 px-6 py-3 rounded-2xl text-white no-underline font-semibold" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", boxShadow: "0 8px 24px rgba(79,142,247,0.3)" }}>
            <Home className="w-4 h-4" /> Go to homepage
          </Link>
          <Link to="/app/dashboard" className="flex items-center gap-2 px-6 py-3 rounded-2xl no-underline font-semibold" style={{ border: "1.5px solid #e2e8f0", color: "#64748b", background: "#fff" }}>
            <ArrowLeft className="w-4 h-4" /> Back to dashboard
          </Link>
        </div>

        {/* Quick links */}
        <div className="mt-10 pt-8 border-t" style={{ borderColor: "#e2e8f0" }}>
          <p style={{ color: "#94a3b8", fontSize: "0.82rem", marginBottom: 12 }}>Or try one of these:</p>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {[
              { label: "Features", to: "/features" },
              { label: "Pricing", to: "/pricing" },
              { label: "Contact", to: "/contact" },
              { label: "Sign up", to: "/signup" },
            ].map(({ label, to }) => (
              <Link key={to} to={to} className="px-4 py-1.5 rounded-xl no-underline text-sm" style={{ background: "#fff", border: "1px solid #e2e8f0", color: "#64748b" }}
                onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = "#4F8EF7"; (e.currentTarget as HTMLElement).style.color = "#4F8EF7"; }}
                onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = "#e2e8f0"; (e.currentTarget as HTMLElement).style.color = "#64748b"; }}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
