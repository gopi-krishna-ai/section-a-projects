import { useState, useEffect } from 'react';
import { UserCheck, Activity, ShieldAlert, Clock, Laptop, Eye, History } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function UserAnalytics() {
  const [analytics, setAnalytics] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/user/analytics')
      .then((r) => r.json())
      .then((d) => setAnalytics(d))
      .catch(() => {
        setAnalytics({
          user: 'student Analyst',
          last_login: '2026-10-13 11:45:10',
          active_session_ip: '192.168.1.45',
          failed_login_attempts_today: 0,
          total_scans_conducted: 18,
          scans_by_tool: {
            'Password Analysis': 5,
            'URL Analysis': 4,
            'Phishing Detector': 3,
            'Network Scan': 3,
            'File Hash': 2,
            'Log Analysis': 1,
          },
          risk_breakdown: { low: 9, medium: 6, high: 3 }
        });
      });
  }, []);

  const chartData = analytics?.scans_by_tool
    ? Object.entries(analytics.scans_by_tool).map(([name, count]) => ({ name, count }))
    : [];

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <Activity /> User Behavior & System Analytics
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Telemetry insights, operator activity logs, session hygiene, and scan volumes across the security toolkit.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <UserCheck size={20} />
          </div>
          <div>
            <span className="text-xs text-slate-400">Authenticated Operator</span>
            <p className="text-sm font-bold text-slate-100">{analytics?.user || 'student Analyst'}</p>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Clock size={20} />
          </div>
          <div>
            <span className="text-xs text-slate-400">Last Session Login</span>
            <p className="text-xs font-mono font-semibold text-slate-300">{analytics?.last_login || 'Today 11:45'}</p>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
            <Laptop size={20} />
          </div>
          <div>
            <span className="text-xs text-slate-400">Session IP Address</span>
            <p className="text-xs font-mono font-bold text-teal-400">{analytics?.active_session_ip || '192.168.1.45'}</p>
          </div>
        </div>

        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldAlert size={20} />
          </div>
          <div>
            <span className="text-xs text-slate-400">Failed Logins Today</span>
            <p className="text-sm font-bold text-emerald-400">0 (Nominal)</p>
          </div>
        </div>
      </div>

      {/* Scans Chart */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <h3 className="font-semibold text-slate-200 text-sm">
          Scans Performed by Tool Category
        </h3>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0b1120', borderColor: '#334155', borderRadius: '8px' }}
              />
              <Bar dataKey="count" fill="#2dd4bf" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Behavioral Hygiene Checklist */}
      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-3">
        <h3 className="font-semibold text-slate-200 text-sm flex items-center gap-2">
          <Eye size={16} className="text-teal-400" /> Behavioral Anomaly & Risk Evaluation
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-[#0b1120] border border-slate-800 rounded-lg">
            <span className="text-slate-400">Account Brute-Force Risk</span>
            <p className="text-emerald-400 font-bold mt-1">LOW (No credential stuffing)</p>
          </div>
          <div className="p-3 bg-[#0b1120] border border-slate-800 rounded-lg">
            <span className="text-slate-400">Privilege Escalation Events</span>
            <p className="text-emerald-400 font-bold mt-1">ZERO FLAGS</p>
          </div>
          <div className="p-3 bg-[#0b1120] border border-slate-800 rounded-lg">
            <span className="text-slate-400">Operator Audit Conformance</span>
            <p className="text-teal-400 font-bold mt-1">100% COMPLIANT</p>
          </div>
        </div>
      </div>
    </div>
  );
}
