import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Brain, Eye, EyeOff, Check, ArrowRight } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export function SignUpPage() {
  const navigate = useNavigate();
  const { signup, isLoading } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [agreed, setAgreed] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const strength = password.length >= 8 ? (password.match(/[A-Z]/) && password.match(/[0-9]/) ? "strong" : "medium") : password.length > 0 ? "weak" : "";
  const strengthColor = { strong: "#10b981", medium: "#f59e0b", weak: "#ef4444", "": "#e2e8f0" }[strength];
  const strengthWidth = { strong: "100%", medium: "66%", weak: "33%", "": "0%" }[strength];

  const validate = () => {
    const e: Record<string, string> = {};
    if (!name.trim()) e.name = "Full name is required.";
    if (!email.includes("@")) e.email = "Enter a valid email address.";
    if (password.length < 8) e.password = "Password must be at least 8 characters.";
    if (password !== confirm) e.confirm = "Passwords do not match.";
    if (!agreed) e.agreed = "Please agree to the terms.";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    await signup(name.trim(), email, password);
    navigate("/verify-email");
  };

  const field = (label: string, key: string, child: React.ReactNode) => (
    <div>
      <label style={{ color: "#374151", fontSize: "0.85rem", fontWeight: 600, display: "block", marginBottom: 6 }}>{label}</label>
      {child}
      {errors[key] && <p style={{ color: "#ef4444", fontSize: "0.78rem", marginTop: 4 }}>{errors[key]}</p>}
    </div>
  );

  const inputCls = (key: string): React.CSSProperties => ({
    width: "100%", padding: "0.72rem 1rem", borderRadius: "0.75rem", outline: "none",
    background: "#f8faff", border: `1.5px solid ${errors[key] ? "#fca5a5" : "#e2e8f0"}`,
    fontFamily: "Inter, sans-serif", fontSize: "0.9rem", color: "#0f172a", boxSizing: "border-box",
    transition: "border-color 0.15s",
  });

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <Link to="/" className="flex items-center gap-2.5 justify-center mb-8 no-underline">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #4F8EF7, #7B61FF)" }}>
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span style={{ fontWeight: 700, fontSize: "1.1rem", color: "#0f172a" }}>StudyAI</span>
        </Link>

        <div className="rounded-3xl p-8" style={{ background: "#fff", boxShadow: "0 25px 80px rgba(79,142,247,0.12)" }}>
          <div className="mb-7">
            <h1 style={{ fontWeight: 800, fontSize: "1.7rem", color: "#0f172a", marginBottom: 8 }}>Create your account 🚀</h1>
            <p style={{ color: "#64748b", fontSize: "0.9rem" }}>Join 50,000+ students studying smarter with AI.</p>
          </div>

          <button className="w-full mb-5 py-3 rounded-xl flex items-center justify-center gap-3" style={{ border: "1.5px solid #e2e8f0", background: "#fff", color: "#374151", fontWeight: 500, fontSize: "0.9rem" }}>
            <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Sign up with Google
          </button>

          <div className="flex items-center gap-3 mb-5">
            <div className="flex-1 h-px" style={{ background: "#f1f5f9" }} />
            <span style={{ color: "#94a3b8", fontSize: "0.8rem" }}>or sign up with email</span>
            <div className="flex-1 h-px" style={{ background: "#f1f5f9" }} />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {field("Full name", "name",
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Alex Johnson" style={inputCls("name")}
                onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                onBlur={(e) => { e.target.style.border = `1.5px solid ${errors.name ? "#fca5a5" : "#e2e8f0"}`; e.target.style.background = "#f8faff"; }}
              />
            )}
            {field("Email address", "email",
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@university.edu" style={inputCls("email")}
                onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                onBlur={(e) => { e.target.style.border = `1.5px solid ${errors.email ? "#fca5a5" : "#e2e8f0"}`; e.target.style.background = "#f8faff"; }}
              />
            )}
            {field("Password", "password",
              <div>
                <div className="relative">
                  <input type={showPw ? "text" : "password"} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Min. 8 characters" style={{ ...inputCls("password"), paddingRight: "2.8rem" }}
                    onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                    onBlur={(e) => { e.target.style.border = `1.5px solid ${errors.password ? "#fca5a5" : "#e2e8f0"}`; e.target.style.background = "#f8faff"; }}
                  />
                  <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-3 top-1/2 -translate-y-1/2" style={{ color: "#94a3b8" }}>
                    {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {password.length > 0 && (
                  <div className="mt-2">
                    <div className="h-1 rounded-full overflow-hidden" style={{ background: "#f1f5f9" }}>
                      <div className="h-full rounded-full transition-all duration-300" style={{ width: strengthWidth, background: strengthColor }} />
                    </div>
                    <p style={{ color: strengthColor, fontSize: "0.73rem", marginTop: 3, fontWeight: 500 }}>
                      {strength === "strong" ? "Strong password ✓" : strength === "medium" ? "Medium — add uppercase & numbers" : "Weak — too short"}
                    </p>
                  </div>
                )}
              </div>
            )}
            {field("Confirm password", "confirm",
              <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} placeholder="••••••••" style={inputCls("confirm")}
                onFocus={(e) => { e.target.style.border = "1.5px solid #4F8EF7"; e.target.style.background = "#fff"; }}
                onBlur={(e) => { e.target.style.border = `1.5px solid ${errors.confirm ? "#fca5a5" : "#e2e8f0"}`; e.target.style.background = "#f8faff"; }}
              />
            )}

            <div>
              <label className="flex items-start gap-3 cursor-pointer">
                <div className="w-5 h-5 rounded flex items-center justify-center flex-shrink-0 mt-0.5 transition-all" style={{ background: agreed ? "linear-gradient(135deg, #4F8EF7, #7B61FF)" : "#f8faff", border: `1.5px solid ${errors.agreed ? "#fca5a5" : agreed ? "#4F8EF7" : "#e2e8f0"}` }}
                  onClick={() => setAgreed(!agreed)}
                >
                  {agreed && <Check className="w-3 h-3 text-white" />}
                </div>
                <span style={{ color: "#64748b", fontSize: "0.83rem", lineHeight: 1.55 }}>
                  I agree to StudyAI's{" "}
                  <Link to="/terms" style={{ color: "#4F8EF7", textDecoration: "none" }}>Terms of Service</Link>{" "}and{" "}
                  <Link to="/privacy" style={{ color: "#4F8EF7", textDecoration: "none" }}>Privacy Policy</Link>
                </span>
              </label>
              {errors.agreed && <p style={{ color: "#ef4444", fontSize: "0.78rem", marginTop: 4 }}>{errors.agreed}</p>}
            </div>

            <button type="submit" disabled={isLoading} className="w-full py-3.5 rounded-xl text-white flex items-center justify-center gap-2 mt-1" style={{ background: isLoading ? "#94a3b8" : "linear-gradient(135deg, #4F8EF7, #7B61FF)", fontWeight: 700, fontSize: "0.95rem", boxShadow: isLoading ? "none" : "0 8px 30px rgba(79,142,247,0.35)", cursor: isLoading ? "not-allowed" : "pointer" }}>
              {isLoading ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Creating account...</> : <>Create free account <ArrowRight className="w-4 h-4" /></>}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
              Already have an account?{" "}
              <Link to="/login" style={{ color: "#4F8EF7", fontWeight: 600, textDecoration: "none" }}>Sign in</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
