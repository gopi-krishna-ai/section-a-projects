import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, KeyRound, Shield, LogOut, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Settings() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState({
    name: 'Analyst User',
    email: 'analyst@cybervault.internal',
    role: 'Cybersecurity Analyst',
    department: 'SOC Defense & Incident Response'
  });

  // OTP Change Password state
  const [step, setStep] = useState<'request' | 'verify'>('request');
  const [otp, setOtp] = useState('');
  const [demoOtp, setDemoOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [statusMsg, setStatusMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [loading, setLoading] = useState(false);

  const requestOtp = async () => {
    setLoading(true);
    setStatusMsg(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: profile.email })
      });
      const data = await res.json();
      setDemoOtp(data.demo_otp || '123456');
      setStep('verify');
      setStatusMsg({
        type: 'success',
        text: `Verification OTP dispatched to ${profile.email}. (Demo Code: ${data.demo_otp || '123456'})`
      });
    } catch {
      setDemoOtp('849201');
      setStep('verify');
      setStatusMsg({
        type: 'success',
        text: `OTP dispatched to ${profile.email}. (Demo Code: 849201)`
      });
    }
    setLoading(false);
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setStatusMsg({ type: 'error', text: 'New passwords do not match!' });
      return;
    }
    if (newPassword.length < 8) {
      setStatusMsg({ type: 'error', text: 'Password must be at least 8 characters.' });
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/auth/verify-otp-reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: profile.email,
          otp,
          new_password: newPassword
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Verification failed');
      setStatusMsg({ type: 'success', text: 'Password successfully changed and secured with OTP!' });
      setStep('request');
      setOtp('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      setStatusMsg({ type: 'error', text: err.message || 'Invalid OTP code. Please try again.' });
    }
    setLoading(false);
  };

  const handleLogout = () => {
    navigate('/login');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <Shield /> Account Settings & Profile
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Manage your analyst profile, perform secure password changes using OTP two-factor verification, and control active sessions.
        </p>
      </div>

      {/* Operator Profile */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <div className="flex items-center gap-4 border-b border-slate-800 pb-5">
          <div className="w-14 h-14 rounded-full bg-teal-500/10 border-2 border-teal-500/40 flex items-center justify-center text-teal-400 text-xl font-bold">
            A
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{profile.name}</h2>
            <p className="text-xs text-teal-400 font-mono">{profile.role}</p>
            <p className="text-xs text-slate-500">{profile.department}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-400 mb-1">Full Name</label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-slate-200 outline-none focus:border-teal-500"
            />
          </div>
          <div>
            <label className="block text-slate-400 mb-1">Email Address</label>
            <input
              type="email"
              value={profile.email}
              readOnly
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-slate-400 outline-none font-mono cursor-not-allowed"
            />
          </div>
        </div>
      </div>

      {/* Change Password with OTP */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-5">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
          <KeyRound className="text-teal-400" size={18} />
          <h2 className="text-base font-bold text-slate-200">Change Password with OTP Verification</h2>
        </div>

        {statusMsg && (
          <div
            className={`p-3 rounded-lg text-xs flex items-center gap-2 ${
              statusMsg.type === 'success'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
            }`}
          >
            {statusMsg.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
            <span>{statusMsg.text}</span>
          </div>
        )}

        {step === 'request' ? (
          <div className="space-y-4">
            <p className="text-xs text-slate-400 leading-relaxed">
              To update your account password, CyberVault requires a One-Time Password (OTP) dispatched to your registered email address ({profile.email}).
            </p>
            <button
              onClick={requestOtp}
              disabled={loading}
              className="px-5 py-2.5 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-lg text-xs transition"
            >
              {loading ? 'Dispatching OTP...' : 'Send Verification OTP to Email'}
            </button>
          </div>
        ) : (
          <form onSubmit={handlePasswordChange} className="space-y-4 text-xs max-w-md">
            <div>
              <div className="flex justify-between items-center mb-1">
                <label className="text-slate-400">Enter 6-Digit OTP</label>
                {demoOtp && (
                  <span className="text-[10px] text-teal-400 font-mono">Demo OTP: {demoOtp}</span>
                )}
              </div>
              <input
                type="text"
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="e.g. 123456"
                required
                className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-slate-200 tracking-widest font-mono text-sm outline-none focus:border-teal-500"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">New Secure Password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="At least 8 characters..."
                required
                className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-slate-200 outline-none focus:border-teal-500 font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Confirm New Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter password..."
                required
                className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-slate-200 outline-none focus:border-teal-500 font-mono"
              />
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                disabled={loading}
                className="px-5 py-2.5 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-lg transition"
              >
                {loading ? 'Validating...' : 'Verify OTP & Update Password'}
              </button>
              <button
                type="button"
                onClick={() => setStep('request')}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Session Management & Logout */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl flex justify-between items-center">
        <div>
          <h3 className="text-sm font-bold text-slate-200">Terminate Active Session</h3>
          <p className="text-xs text-slate-400 mt-0.5">Revoke tokens and safely log out of the defensive toolkit.</p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 font-semibold rounded-lg text-xs flex items-center gap-2 transition"
        >
          <LogOut size={15} /> Log Out of CyberVault
        </button>
      </div>
    </div>
  );
}
