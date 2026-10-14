import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Brain, Mail, ArrowRight, RefreshCw } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function EmailVerificationPage() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [resent, setResent] = useState(false);
  const [resending, setResending] = useState(false);

  const handleResend = async () => {
    setResending(true);
    await new Promise(r => setTimeout(r, 1000));
    setResending(false);
    setResent(true);
    setTimeout(() => setResent(false), 5000);
  };

  const handleVerifyDemo = () => {
    updateUser({ emailVerified: true });
    navigate("/app/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12" style={{ fontFamily: "Inter, sans-serif" }}>
      <div className="w-full max-w-md">
        <Link to="/" className="flex items-center gap-2.5 justify-center mb-8 no-underline">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "#0f172a" }}>StudyAI</span>
        </Link>

        <div className="rounded-3xl p-8 text-center" style={{ background: "#fff", boxShadow: "0 25px 80px rgba(79,142,247,0.12)" }}>
          {/* Animated envelope */}
          <div className="relative w-20 h-20 mx-auto mb-6">
            <div className="w-20 h-20 rounded-2xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #eff6ff, #f5f3ff)" }}>
              <Mail className="w-10 h-10" style={{ color: "#4F8EF7" }} />
            </div>
            <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
              <span style={{ color: "#fff", fontSize: "0.65rem", fontWeight: 700 }}>✓</span>
            </div>
          </div>

          <h1 style={{ fontWeight: 800, fontSize: "1.6rem", color: "#0f172a", marginBottom: 12 }}>Verify your email</h1>
          <p style={{ color: "#64748b", fontSize: "0.9rem", lineHeight: 1.7, marginBottom: 6 }}>
            We sent a verification email to:
          </p>
          <p style={{ color: "#0f172a", fontWeight: 700, fontSize: "1rem", marginBottom: 20 }}>
            {user?.email || "your email address"}
          </p>
          <p style={{ color: "#64748b", fontSize: "0.85rem", lineHeight: 1.65, marginBottom: 28 }}>
            Click the link in the email to activate your account. Once verified, you'll have full access to all StudyAI features.
          </p>

          {resent && (
            <div className="mb-5 p-3.5 rounded-xl" style={{ background: "#f0fdf4", border: "1px solid #bbf7d0" }}>
              <p style={{ color: "#15803d", fontSize: "0.85rem", fontWeight: 500 }}>✓ Verification email resent successfully!</p>
            </div>
          )}

          <div className="space-y-3">
            {/* Demo CTA */}
            <button onClick={handleVerifyDemo} className="w-full py-3.5 rounded-xl text-white flex items-center justify-center gap-2" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)", fontWeight: 700, fontSize: "0.95rem", boxShadow: "0 8px 30px rgba(79,142,247,0.3)" }}>
              Continue to Dashboard <ArrowRight className="w-4 h-4" />
            </button>
            <p style={{ color: "#94a3b8", fontSize: "0.72rem" }}>Demo mode: skip verification and go straight in</p>

            <div className="h-px my-4" style={{ background: "#f1f5f9" }} />

            <button onClick={handleResend} disabled={resending} className="w-full py-3 rounded-xl flex items-center justify-center gap-2" style={{ border: "1.5px solid #e2e8f0", background: "#fff", color: "#374151", fontWeight: 500, fontSize: "0.875rem", cursor: resending ? "not-allowed" : "pointer" }}>
              <RefreshCw className={`w-4 h-4 ${resending ? "animate-spin" : ""}`} style={{ color: "#64748b" }} />
              {resending ? "Resending..." : "Resend verification email"}
            </button>
          </div>

          <div className="mt-6 pt-5 border-t" style={{ borderColor: "#f1f5f9" }}>
            <p style={{ color: "#64748b", fontSize: "0.82rem", lineHeight: 1.6 }}>
              Wrong email? <Link to="/signup" style={{ color: "#4F8EF7", textDecoration: "none", fontWeight: 600 }}>Sign up again</Link>
              {" "}or{" "}
              <Link to="/login" style={{ color: "#4F8EF7", textDecoration: "none", fontWeight: 600 }}>sign in</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
