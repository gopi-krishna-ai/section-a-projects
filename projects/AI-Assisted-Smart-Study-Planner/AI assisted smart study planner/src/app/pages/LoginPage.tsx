import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Brain, Eye, EyeOff, Zap, ArrowRight } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function LoginPage() {
  const navigate = useNavigate();
  const { login, isLoading } = useAuth();
  const [email, setEmail] = useState("alex.johnson@university.edu");
  const [password, setPassword] = useState("password");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email || !password) { setError("Please fill in all fields."); return; }
    try {
      await login(email, password, remember);
      navigate("/app/dashboard");
    } catch {
      setError("Invalid email or password. Please try again.");
    }
  };

  const inputStyle = {
    background: "#f8faff", border: "1.5px solid #e2e8f0",
    fontFamily: "Inter, sans-serif", fontSize: "0.9rem", color: "#1a1f3e",
    width: "100%", padding: "0.75rem 1rem", borderRadius: "0.75rem",
    outline: "none", transition: "border-color 0.15s, background 0.15s", boxSizing: "border-box" as const,
  };

  return (
    <div className="min-h-screen flex" style={{ fontFamily: "Inter, sans-serif" }}>
      {/* Left panel */}
      <div className="hidden lg:flex flex-col justify-between w-[45%] p-12 relative overflow-hidden" style={{ background: "linear-gradient(135deg, #0f1228 0%, #1a1f3e 50%, #1a0a3e 100%)" }}>
        <div className="absolute top-16 left-10 w-72 h-72 rounded-full opacity-20 blur-3xl" style={{ background: "radial-gradient(circle, #4F8EF7, transparent)" }} />
        <div className="absolute bottom-24 right-8 w-80 h-80 rounded-full opacity-15 blur-3xl" style={{ background: "radial-gradient(circle, #7B61FF, transparent)" }} />

        <Link to="/" className="flex items-center gap-3 relative z-10 no-underline">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="text-white" style={{ fontWeight: 700, fontSize: "1.1rem" }}>StudyAI</p>
            <p style={{ color: "#64748b", fontSize: "0.72rem" }}>Smart Study Planner</p>
          </div>
        </Link>

        <div className="relative z-10 space-y-8">
          <div>
            <h2 className="text-white mb-4" style={{ fontWeight: 800, fontSize: "2.4rem", lineHeight: 1.15, letterSpacing: "-0.02em" }}>
              Study Smarter,<br />
              <span style={{ background: "linear-gradient(135deg, #60a5fa, #a78bfa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Not Harder.</span>
            </h2>
            <p style={{ color: "#64748b", fontSize: "1rem", lineHeight: 1.7, maxWidth: 340 }}>
              AI-powered study planning that adapts to your patterns and helps you reach your academic goals.
            </p>
          </div>
          <div className="space-y-3">
            {[
              { text: "AI-generated personalized study plans", color: "#4F8EF7" },
              { text: "Productivity prediction & analytics", color: "#7B61FF" },
              { text: "Smart task tracking & Pomodoro timer", color: "#10b981" },
            ].map((f, i) => (
              <div key={i} className="flex items-center gap-3 p-3.5 rounded-xl" style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)" }}>
                <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: f.color }} />
                <span style={{ color: "#cbd5e1", fontSize: "0.875rem" }}>{f.text}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="relative z-10 p-5 rounded-2xl" style={{ background: "rgba(79,142,247,0.08)", border: "1px solid rgba(79,142,247,0.18)" }}>
          <div className="w-5 h-0.5 mb-3" style={{ background: "#4F8EF7" }} />
          <p style={{ color: "#e2e8f0", fontSize: "0.9rem", lineHeight: 1.65, fontStyle: "italic" }}>
            "StudyAI helped me go from struggling to scoring top marks. The AI plan just works."
          </p>
          <p className="mt-3" style={{ color: "#64748b", fontSize: "0.78rem" }}>— Sarah Chen, Computer Science Year 3</p>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center px-6 py-12" style={{ background: "linear-gradient(135deg, #f0f4ff 0%, #f8f0ff 100%)" }}>
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <Link to="/" className="flex lg:hidden items-center gap-3 mb-8 justify-center no-underline">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "#0f172a" }}>StudyAI</span>
          </Link>

          <div className="rounded-3xl p-8" style={{ background: "#fff", boxShadow: "0 25px 80px rgba(79,142,247,0.12)" }}>
            <div className="mb-8">
              <h1 style={{ fontWeight: 800, fontSize: "1.7rem", color: "#0f172a", lineHeight: 1.2, marginBottom: 8 }}>Welcome back 👋</h1>
              <p style={{ color: "#64748b", fontSize: "0.9rem" }}>Sign in to continue your learning journey.</p>
            </div>

            {error && (
              <div className="mb-5 p-3.5 rounded-xl" style={{ background: "#fef2f2", border: "1px solid #fecaca" }}>
                <p style={{ color: "#dc2626", fontSize: "0.85rem" }}>{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label style={{ color: "#374151", fontSize: "0.85rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Email address</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@university.edu" style={inputStyle}
                  onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                  onBlur={(e) => { e.target.style.border = "1.5px solid #e2e8f0"; e.target.style.background = "#f8faff"; }}
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label style={{ color: "#374151", fontSize: "0.85rem", fontWeight: 600 }}>Password</label>
                  <Link to="/forgot-password" style={{ color: "#4F8EF7", fontSize: "0.8rem", textDecoration: "none", fontWeight: 500 }}>Forgot password?</Link>
                </div>
                <div className="relative">
                  <input type={showPassword ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" style={{ ...inputStyle, paddingRight: "2.8rem" }}
                    onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                    onBlur={(e) => { e.target.style.border = "1.5px solid #e2e8f0"; e.target.style.background = "#f8faff"; }}
                  />
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2" style={{ color: "#94a3b8" }}>
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <label className="flex items-center gap-2.5 cursor-pointer">
                <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} className="w-4 h-4 rounded" style={{ accentColor: "#4F8EF7" }} />
                <span style={{ color: "#64748b", fontSize: "0.85rem" }}>Remember me for 30 days</span>
              </label>

              <button type="submit" disabled={isLoading} className="w-full py-3.5 rounded-xl text-white flex items-center justify-center gap-2 transition-all duration-200 mt-2" style={{ background: isLoading ? "#94a3b8" : "linear-gradient(135deg, #4F8EF7, #7B61FF)", fontWeight: 700, fontSize: "0.95rem", boxShadow: isLoading ? "none" : "0 8px 30px rgba(79,142,247,0.35)", cursor: isLoading ? "not-allowed" : "pointer" }}>
                {isLoading ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Signing in...</> : <><Zap className="w-4 h-4" /> Sign in to Dashboard</>}
              </button>
            </form>

            <div className="mt-5 flex items-center gap-3">
              <div className="flex-1 h-px" style={{ background: "#f1f5f9" }} />
              <span style={{ color: "#94a3b8", fontSize: "0.8rem" }}>or</span>
              <div className="flex-1 h-px" style={{ background: "#f1f5f9" }} />
            </div>

            <button className="mt-4 w-full py-3 rounded-xl flex items-center justify-center gap-3 transition-all" style={{ border: "1.5px solid #e2e8f0", background: "#fff", color: "#374151", fontWeight: 500, fontSize: "0.9rem" }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "#cbd5e1"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.borderColor = "#e2e8f0"; }}
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
              Continue with Google
            </button>

            <div className="mt-6 text-center">
              <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
                Don't have an account?{" "}
                <Link to="/signup" style={{ color: "#4F8EF7", fontWeight: 600, textDecoration: "none" }}>
                  Sign up free <ArrowRight className="w-3.5 h-3.5 inline" />
                </Link>
              </p>
            </div>
          </div>

          <p className="mt-4 text-center" style={{ color: "#94a3b8", fontSize: "0.75rem" }}>
            Demo: any email + password works → instantly enters dashboard
          </p>
        </div>
      </div>
    </div>
  );
}
