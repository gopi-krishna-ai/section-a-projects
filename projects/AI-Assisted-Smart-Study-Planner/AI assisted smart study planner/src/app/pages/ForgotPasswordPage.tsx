import { useState } from "react";
import { Link } from "react-router";
import { Brain, Mail, ArrowLeft, CheckCircle2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function ForgotPasswordPage() {
  const { forgotPassword } = useAuth();
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.includes("@")) { setError("Please enter a valid email address."); return; }
    setLoading(true);
    await forgotPassword(email);
    setLoading(false);
    setSent(true);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <Link to="/" className="flex items-center gap-2.5 justify-center mb-8 no-underline">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "#0f172a", fontFamily: "Inter, sans-serif" }}>StudyAI</span>
        </Link>

        <div className="rounded-3xl p-8" style={{ background: "#fff", boxShadow: "0 25px 80px rgba(79,142,247,0.12)", fontFamily: "Inter, sans-serif" }}>
          {!sent ? (
            <>
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{ background: "linear-gradient(135deg, #eff6ff, #f5f3ff)" }}>
                <Mail className="w-7 h-7" style={{ color: "#4F8EF7" }} />
              </div>
              <div className="text-center mb-7">
                <h1 style={{ fontWeight: 800, fontSize: "1.6rem", color: "#0f172a", marginBottom: 8 }}>Reset your password</h1>
                <p style={{ color: "#64748b", fontSize: "0.9rem", lineHeight: 1.6 }}>
                  Enter the email address linked to your account and we'll send you a reset link.
                </p>
              </div>

              {error && (
                <div className="mb-4 p-3.5 rounded-xl" style={{ background: "#fef2f2", border: "1px solid #fecaca" }}>
                  <p style={{ color: "#dc2626", fontSize: "0.85rem" }}>{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label style={{ color: "#374151", fontSize: "0.85rem", fontWeight: 600, display: "block", marginBottom: 6 }}>Email address</label>
                  <input type="email" value={email} onChange={(e) => { setEmail(e.target.value); setError(""); }} placeholder="you@university.edu"
                    style={{ width: "100%", padding: "0.75rem 1rem", borderRadius: "0.75rem", outline: "none", background: "#f8faff", border: "1.5px solid #e2e8f0", fontFamily: "Inter, sans-serif", fontSize: "0.9rem", color: "#0f172a", boxSizing: "border-box" }}
                    onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                    onBlur={(e) => { e.target.style.border = "1.5px solid #e2e8f0"; e.target.style.background = "#f8faff"; }}
                  />
                </div>

                <button type="submit" disabled={loading} className="w-full py-3.5 rounded-xl text-white flex items-center justify-center gap-2" style={{ background: loading ? "#94a3b8" : "linear-gradient(135deg, #4F8EF7, #7B61FF)", fontWeight: 700, fontSize: "0.95rem", boxShadow: "0 8px 30px rgba(79,142,247,0.3)" }}>
                  {loading ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Sending...</> : "Send reset link"}
                </button>
              </form>
            </>
          ) : (
            <div className="text-center">
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{ background: "#f0fdf4" }}>
                <CheckCircle2 className="w-8 h-8" style={{ color: "#10b981" }} />
              </div>
              <h1 style={{ fontWeight: 800, fontSize: "1.6rem", color: "#0f172a", marginBottom: 12 }}>Check your inbox!</h1>
              <p style={{ color: "#64748b", fontSize: "0.9rem", lineHeight: 1.7, marginBottom: 8 }}>
                We sent a password reset link to
              </p>
              <p style={{ color: "#0f172a", fontWeight: 600, fontSize: "0.95rem", marginBottom: 20 }}>{email}</p>
              <p style={{ color: "#64748b", fontSize: "0.83rem", lineHeight: 1.6, marginBottom: 24 }}>
                Didn't receive the email? Check your spam folder, or{" "}
                <button onClick={() => setSent(false)} style={{ color: "#4F8EF7", fontWeight: 600, background: "none", border: "none", cursor: "pointer", padding: 0 }}>try again</button>.
              </p>
              <div className="h-px mb-5" style={{ background: "#f1f5f9" }} />
              <p style={{ color: "#64748b", fontSize: "0.83rem" }}>
                The link expires in 1 hour for security.
              </p>
            </div>
          )}

          <div className="mt-6 text-center">
            <Link to="/login" className="flex items-center justify-center gap-1.5 no-underline" style={{ color: "#64748b", fontSize: "0.875rem" }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.color = "#4F8EF7"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.color = "#64748b"; }}
            >
              <ArrowLeft className="w-4 h-4" /> Back to sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
