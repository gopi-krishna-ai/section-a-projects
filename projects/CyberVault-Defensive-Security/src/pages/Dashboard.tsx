import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';
import { 
  ShieldCheck, 
  AlertTriangle, 
  AlertCircle, 
  Scan, 
  Activity, 
  ArrowRight,
  Shield,
  KeyRound,
  Dna,
  Link as LinkIcon,
  Eye,
  FileText,
  CheckCircle2,
  FileSearch,
  Network,
  Globe,
  MessageSquare
} from 'lucide-react';

const scanData = [
  { name: '2 Fri', value: 1 },
  { name: '3 Sat', value: 3 },
  { name: '4 Sun', value: 2 },
  { name: '5 Mon', value: 0 },
  { name: '6 Tue', value: 4 },
  { name: '7 Wed', value: 5 },
  { name: '8 Thu', value: 3 },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/scans/summary')
      .then((r) => r.json())
      .then((data) => setSummary(data))
      .catch(() => {
        setSummary({
          securityScore: 72,
          mediumFindings: 6,
          highFindings: 3,
          lowFindings: 9,
          totalScans: 18,
          totalSolution: 'Close exposed ports (Telnet/FTP), filter malicious phishing URLs, and mandate 14-character MFA passwords.',
          recentAlerts: [
            {
              type: 'HIGH',
              title: 'Network Scan',
              target: '192.168.1.10',
              message: 'Close ports you do not need and restrict the rest with a firewall.',
              time: '2026-10-12 09:42'
            },
            {
              type: 'HIGH',
              title: 'Phishing Detector',
              target: 'http://secure-login.verify-account.example/update',
              message: 'Do not open this link or enter credentials.',
              time: '2026-10-12 09:15'
            },
            {
              type: 'MEDIUM',
              title: 'Password Analysis',
              target: 'Password (9 characters)',
              message: 'Add special characters or numbers to make it stronger.',
              time: '2026-10-11 18:03'
            }
          ]
        });
      });
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-teal-400">Security Dashboard</h1>
          <p className="text-slate-400 text-sm mt-0.5">Scan results, risk levels, and automated remediation solutions from your toolkit</p>
        </div>
        <Link
          to="/dashboard/report"
          className="px-4 py-2 bg-slate-800 border border-teal-500/50 text-teal-400 rounded-lg text-xs font-semibold hover:bg-slate-700 transition"
        >
          Download PDF report
        </Link>
      </div>

      {/* Total Risk Banner & Solution (Requested Feature) */}
      <div className="bg-gradient-to-r from-slate-900 to-[#0f172a] border border-teal-500/30 rounded-2xl p-5 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1 max-w-3xl">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-teal-400 animate-ping"></span>
            <h2 className="text-sm font-bold text-teal-300 uppercase tracking-wider">
              Total Enterprise Risk Evaluation & Systemic Fix
            </h2>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            {summary?.totalSolution || 'Close exposed ports, isolate unverified phishing links, and configure MFA.'}
          </p>
        </div>
        <Link
          to="/dashboard/history"
          className="px-4 py-2 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-lg text-xs shrink-0 transition"
        >
          View All Scan Records
        </Link>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0f172a] border border-amber-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center gap-2 text-amber-500 mb-2">
            <ShieldCheck size={16} />
            <span className="text-xs font-semibold uppercase tracking-wider">Security Score</span>
          </div>
          <div>
            <span className="text-3xl font-bold text-amber-500">{summary?.securityScore || 72}</span>
            <span className="text-slate-500 text-xs ml-1">out of 100</span>
          </div>
          <p className="text-xs text-slate-500 mt-2">Average across all scans</p>
        </div>

        <div className="bg-[#0f172a] border border-amber-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center gap-2 text-amber-500 mb-2">
            <AlertTriangle size={16} />
            <span className="text-xs font-semibold uppercase tracking-wider">Medium-Risk Findings</span>
          </div>
          <span className="text-3xl font-bold text-amber-500">{summary?.mediumFindings ?? 6}</span>
          <p className="text-xs text-slate-500 mt-2">Worth reviewing</p>
        </div>

        <div className="bg-[#0f172a] border border-rose-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center gap-2 text-rose-500 mb-2">
            <AlertCircle size={16} />
            <span className="text-xs font-semibold uppercase tracking-wider">High-Risk Findings</span>
          </div>
          <span className="text-3xl font-bold text-rose-500">{summary?.highFindings ?? 3}</span>
          <p className="text-xs text-slate-500 mt-2">Fix these first</p>
        </div>

        <div className="bg-[#0f172a] border border-emerald-500/30 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center gap-2 text-emerald-500 mb-2">
            <Scan size={16} />
            <span className="text-xs font-semibold uppercase tracking-wider">Total Scans</span>
          </div>
          <span className="text-3xl font-bold text-emerald-500">{summary?.totalScans ?? 18}</span>
          <p className="text-xs text-slate-500 mt-2">Across 8 security tools</p>
        </div>
      </div>

      {/* Main Grid: Left 2 Cols, Right 1 Col */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Recent Alerts */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></div>
                <h3 className="font-semibold text-slate-200 text-sm">Real-Time Threat Alerts</h3>
              </div>
              <Link to="/dashboard/history" className="text-xs text-teal-400 hover:underline">
                View all
              </Link>
            </div>

            <div className="space-y-3">
              {(summary?.recentAlerts || []).slice(0, 3).map((alt: any, i: number) => (
                <div
                  key={i}
                  className={`p-3.5 border rounded-lg ${
                    alt.type === 'HIGH'
                      ? 'border-rose-500/30 bg-rose-500/5'
                      : 'border-amber-500/30 bg-amber-500/5'
                  }`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <div className="flex items-center gap-2">
                      <AlertTriangle
                        size={14}
                        className={alt.type === 'HIGH' ? 'text-rose-400' : 'text-amber-400'}
                      />
                      <span className={`text-xs font-semibold ${alt.type === 'HIGH' ? 'text-rose-300' : 'text-amber-300'}`}>
                        {alt.title}
                      </span>
                    </div>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${
                        alt.type === 'HIGH' ? 'text-rose-400 bg-rose-500/20' : 'text-amber-400 bg-amber-500/20'
                      }`}
                    >
                      {alt.type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-mono mb-1 truncate">{alt.target}</p>
                  <p className="text-xs text-slate-400">{alt.message}</p>
                  <div className="mt-2 pt-2 border-t border-slate-800/80 flex justify-between items-center text-[10px] text-slate-500">
                    <span>{alt.time}</span>
                    <span className="text-teal-400 font-medium">Fix: {alt.solution}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 text-center border-t border-slate-800 pt-3">
              <span className="text-xs text-teal-500/70">Showing the 3 most recent flagged detections</span>
            </div>
          </div>

          {/* Activity Chart */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg">
            <h3 className="font-semibold text-slate-200 text-sm mb-6 flex items-center gap-2 border-l-2 border-teal-500 pl-2">
              Scan Activity, last 7 days
            </h3>
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={scanData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} dx={-10} />
                  <RechartsTooltip
                    cursor={{ fill: '#1e293b' }}
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px' }}
                  />
                  <Bar dataKey="value" fill="#2dd4bf" radius={[4, 4, 0, 0]} barSize={30} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg">
            <h3 className="font-semibold text-slate-200 text-sm mb-4 border-l-2 border-teal-500 pl-2">Quick Actions</h3>
            <div className="space-y-2">
              <Link
                to="/dashboard/ports"
                className="w-full flex items-center justify-between p-3 bg-teal-900/20 border border-teal-500/30 rounded-lg text-xs text-teal-400 hover:bg-teal-900/40 transition"
              >
                <span className="flex items-center gap-2"><Activity size={16} /> Run port scan</span>
                <ArrowRight size={14} />
              </Link>
              <Link
                to="/dashboard/assistant"
                className="w-full flex items-center justify-between p-3 bg-fuchsia-900/20 border border-fuchsia-500/30 rounded-lg text-xs text-fuchsia-400 hover:bg-fuchsia-900/40 transition"
              >
                <span className="flex items-center gap-2"><MessageSquare size={16} /> Chat with assistant</span>
                <ArrowRight size={14} />
              </Link>
              <Link
                to="/dashboard/report"
                className="w-full flex items-center justify-between p-3 bg-emerald-900/20 border border-emerald-500/30 rounded-lg text-xs text-emerald-400 hover:bg-emerald-900/40 transition"
              >
                <span className="flex items-center gap-2"><ShieldCheck size={16} /> Generate PDF report</span>
                <ArrowRight size={14} />
              </Link>
            </div>
          </div>

          {/* Scans by Tool */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg">
            <h3 className="font-semibold text-slate-200 text-sm mb-4 border-l-2 border-teal-500 pl-2">Scans by Tool</h3>
            <div className="space-y-2.5">
              {[
                { name: 'Password Analysis', count: 5, path: '/dashboard/password' },
                { name: 'URL Analysis', count: 4, path: '/dashboard/url' },
                { name: 'Phishing Detector', count: 3, path: '/dashboard/phishing' },
                { name: 'Network Scan', count: 3, path: '/dashboard/ports' },
                { name: 'Website Scanner', count: 2, path: '/dashboard/website' },
                { name: 'File Hash', count: 2, path: '/dashboard/hash' },
                { name: 'Log Analysis', count: 1, path: '/dashboard/logs' },
              ].map((tool) => (
                <Link
                  key={tool.name}
                  to={tool.path}
                  className="flex justify-between items-center text-xs hover:text-teal-300 transition"
                >
                  <span className="text-slate-400">{tool.name}</span>
                  <span className="text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded font-mono">{tool.count}</span>
                </Link>
              ))}
            </div>
          </div>

          {/* Risk Mix */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
            <h3 className="font-semibold text-slate-200 text-sm border-l-2 border-teal-500 pl-2">Risk Mix</h3>
            <div className="flex h-3 w-full rounded-full overflow-hidden">
              <div className="bg-emerald-500" style={{ width: '50%' }}></div>
              <div className="bg-amber-500" style={{ width: '33%' }}></div>
              <div className="bg-rose-500" style={{ width: '17%' }}></div>
            </div>
            <div className="flex justify-between text-[10px] text-slate-400 font-medium">
              <span className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-emerald-500"></div> Low {summary?.lowFindings || 9}</span>
              <span className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-amber-500"></div> Medium {summary?.mediumFindings || 6}</span>
              <span className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-rose-500"></div> High {summary?.highFindings || 3}</span>
            </div>

            <div className="border-t border-slate-800 pt-3">
              <h4 className="text-xs font-semibold text-slate-300 mb-2">What the Data Shows:</h4>
              <ul className="text-[11px] text-slate-400 space-y-1.5 list-disc pl-4 marker:text-teal-400">
                <li>{summary?.highFindings || 3} high-risk finding(s) require prompt firewall/DNS remediation.</li>
                <li>{summary?.mediumFindings || 6} medium-risk findings need credential and header updates.</li>
                <li>Phishing predictions powered by trained Scikit-Learn NLP and Random Forest models.</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Toolkit Cards Grid */}
      <div className="pt-4">
        <h3 className="font-bold text-slate-200 text-base mb-4 flex items-center gap-2">
          <Shield className="text-teal-400" size={18} /> CyberVault Defensive Toolkit
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'Password analysis', desc: 'Rates strength and says what to fix', icon: KeyRound, path: '/dashboard/password' },
            { name: 'Password generator', desc: 'Random passwords to your rules', icon: Dna, path: '/dashboard/generate' },
            { name: 'URL analysis', desc: 'Flags HTTPS, length and @ tricks', icon: LinkIcon, path: '/dashboard/url' },
            { name: 'Phishing detector', desc: 'Scores email/URL with ML model', icon: Eye, path: '/dashboard/phishing' },
            { name: 'File hashes', desc: 'MD5, SHA-1 and SHA-256 of text', icon: FileText, path: '/dashboard/hash' },
            { name: 'Integrity check', desc: 'Compare text to known hash', icon: CheckCircle2, path: '/dashboard/integrity' },
            { name: 'Log analyzer', desc: 'Failed logins, errors and warnings', icon: FileSearch, path: '/dashboard/logs' },
            { name: 'Port scanner', desc: 'Scans common TCP network ports', icon: Network, path: '/dashboard/ports' },
            { name: 'Website scanner', desc: 'Checks SSL, headers, cookies', icon: Globe, path: '/dashboard/website' },
            { name: 'Scan history', desc: 'Review previous scans & fixes', icon: Activity, path: '/dashboard/history' },
            { name: 'User analytics', desc: 'Operator behavior & session stats', icon: Activity, path: '/dashboard/analytics' },
            { name: 'AI Assistant', desc: 'Automated cybersecurity guidance', icon: MessageSquare, path: '/dashboard/assistant' },
          ].map((card, i) => (
            <Link
              key={i}
              to={card.path}
              className="bg-[#0f172a] hover:bg-slate-800/60 border border-slate-800 hover:border-teal-500/40 p-4 rounded-xl transition space-y-2 group"
            >
              <div className="flex items-center justify-between text-teal-400">
                <card.icon size={20} className="group-hover:scale-110 transition-transform" />
                <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <h4 className="font-semibold text-slate-200 text-xs">{card.name}</h4>
              <p className="text-[11px] text-slate-400 leading-snug">{card.desc}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
