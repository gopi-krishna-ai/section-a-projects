import { useState, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  Shield, 
  LayoutDashboard, 
  KeyRound, 
  Dna, 
  Link as LinkIcon, 
  Eye, 
  FileText, 
  CheckCircle2, 
  FileSearch, 
  Network, 
  History, 
  FileDown, 
  MessageSquare,
  Globe,
  Activity,
  Settings,
  LogOut,
  Bell,
  X,
  AlertTriangle,
  Search
} from 'lucide-react';

const navItems = [
  { group: 'check', items: [
    { name: 'Password analysis', icon: KeyRound, path: '/dashboard/password' },
    { name: 'Password generator', icon: Dna, path: '/dashboard/generate' },
    { name: 'URL analysis', icon: LinkIcon, path: '/dashboard/url' },
    { name: 'Phishing detector', icon: Eye, path: '/dashboard/phishing' },
    { name: 'Website scanner', icon: Globe, path: '/dashboard/website' },
  ]},
  { group: 'files', items: [
    { name: 'File hashes', icon: FileText, path: '/dashboard/hash' },
    { name: 'Integrity check', icon: CheckCircle2, path: '/dashboard/integrity' },
    { name: 'Log analyzer', icon: FileSearch, path: '/dashboard/logs' },
  ]},
  { group: 'network', items: [
    { name: 'Port scanner', icon: Network, path: '/dashboard/ports' },
    { name: 'User analytics', icon: Activity, path: '/dashboard/analytics' },
  ]},
  { group: 'records & ai', items: [
    { name: 'Scan history', icon: History, path: '/dashboard/history' },
    { name: 'PDF report', icon: FileDown, path: '/dashboard/report' },
    { name: 'Assistant', icon: MessageSquare, path: '/dashboard/assistant' },
    { name: 'Settings', icon: Settings, path: '/dashboard/settings' },
  ]}
];

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [showAlertsDrawer, setShowAlertsDrawer] = useState(false);
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/alerts')
      .then((r) => r.json())
      .then((d) => setAlerts(d.alerts || []))
      .catch(() => {
        setAlerts([
          { type: 'HIGH', title: 'Network Scan Flag', target: '192.168.1.10', message: 'Telnet port 23 exposed.', solution: 'Close port and enforce SSH.' },
          { type: 'HIGH', title: 'Phishing Detector', target: 'http://secure-login.xyz', message: 'Credential harvester detected.', solution: 'Block link on boundary proxy.' },
          { type: 'MEDIUM', title: 'Password Weakness', target: 'User creds', message: 'Below 12 characters.', solution: 'Enforce 14-char MFA.' },
        ]);
      });
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const query = search.toLowerCase().trim();
    if (!query) return;

    for (const group of navItems) {
      for (const item of group.items) {
        if (item.name.toLowerCase().includes(query)) {
          navigate(item.path);
          setSearch('');
          return;
        }
      }
    }
  };

  return (
    <div className="flex h-screen bg-[#0b1120] text-slate-300 font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 flex flex-col h-full bg-[#0f172a]/60">
        <Link to="/dashboard" className="p-4 flex items-center gap-3 border-b border-slate-800/80">
          <div className="w-8 h-8 rounded-lg border border-teal-500/30 flex items-center justify-center bg-teal-500/10 text-teal-400">
            <Shield size={20} />
          </div>
          <div>
            <h1 className="font-bold text-teal-400 tracking-wide text-sm">CyberVault</h1>
            <p className="text-[11px] text-slate-500">Defensive security tools</p>
          </div>
        </Link>

        <div className="flex-1 overflow-y-auto py-4 px-3 custom-scrollbar">
          <Link 
            to="/dashboard"
            className={`flex items-center gap-3 px-3 py-2 rounded-lg mb-5 transition-colors ${
              location.pathname === '/dashboard' 
                ? 'bg-teal-500/10 text-teal-400 border border-teal-500/30' 
                : 'hover:bg-slate-800/50 hover:text-slate-200 text-slate-400'
            }`}
          >
            <LayoutDashboard size={18} />
            <span className="text-xs font-semibold">Dashboard</span>
          </Link>

          {navItems.map((group, idx) => (
            <div key={idx} className="mb-5">
              <h3 className="px-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                {group.group}
              </h3>
              <ul className="space-y-0.5">
                {group.items.map((item, i) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <li key={i}>
                      <Link
                        to={item.path}
                        className={`flex items-center gap-2.5 px-3 py-2 rounded-lg transition-colors text-xs ${
                          isActive
                            ? 'bg-teal-500/10 text-teal-400 border border-teal-500/30 font-medium'
                            : 'hover:bg-slate-800/50 hover:text-slate-200 text-slate-400'
                        }`}
                      >
                        <item.icon size={15} />
                        <span>{item.name}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </div>

        <div className="p-3 border-t border-slate-800">
          <Link 
            to="/login" 
            className="flex items-center gap-2.5 px-3 py-2 text-xs text-rose-400/80 hover:text-rose-300 hover:bg-rose-500/10 rounded-lg transition"
          >
            <LogOut size={16} />
            <span>Log out</span>
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Header */}
        <header className="h-16 border-b border-slate-800 flex items-center justify-between px-6 bg-[#0b1120]">
          <form onSubmit={handleSearchSubmit} className="relative w-80">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input 
              type="text" 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-800/50 border border-slate-700 text-slate-200 text-xs rounded-lg focus:border-teal-500 block w-full pl-9 pr-3 py-2 outline-none font-sans" 
              placeholder="Jump to a tool (e.g. port, phishing, hash)..." 
            />
          </form>
          
          <div className="flex items-center gap-4">
            {/* Real-time Alert Notification Bell */}
            <button
              onClick={() => setShowAlertsDrawer(!showAlertsDrawer)}
              className="relative p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-300 hover:text-teal-400 border border-slate-700 transition"
              title="Real-Time Alerts"
            >
              <Bell size={16} />
              {alerts.length > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-rose-500 text-white rounded-full text-[9px] font-bold flex items-center justify-center animate-pulse">
                  {alerts.length}
                </span>
              )}
            </button>

            {/* Operator Profile Avatar */}
            <Link to="/dashboard/settings" className="flex items-center gap-3 hover:opacity-80 transition cursor-pointer">
              <div className="text-right hidden sm:block">
                <p className="text-xs font-semibold text-slate-200 leading-tight">student Analyst</p>
                <p className="text-[10px] text-teal-400 font-mono">SOC Operator</p>
              </div>
              <div className="w-8 h-8 rounded-full bg-teal-500/10 border border-teal-500/50 flex items-center justify-center text-teal-400 text-xs font-bold">
                S
              </div>
            </Link>
          </div>
        </header>

        {/* Viewport */}
        <div className="flex-1 overflow-y-auto p-6 bg-[#0b1120] custom-scrollbar">
          <Outlet />
        </div>
      </main>

      {/* Real-time Alert Notification Drawer */}
      {showAlertsDrawer && (
        <div className="fixed inset-y-0 right-0 w-96 bg-[#0f172a] border-l border-slate-800 shadow-2xl z-50 flex flex-col p-5 animate-in slide-in-from-right duration-300">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
              <h3 className="font-bold text-sm text-slate-200">Real-Time Security Alerts</h3>
            </div>
            <button 
              onClick={() => setShowAlertsDrawer(false)}
              className="text-slate-500 hover:text-slate-300"
            >
              <X size={18} />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar text-xs">
            {alerts.map((alt, idx) => (
              <div 
                key={idx}
                className="p-3 bg-[#0b1120] border border-slate-800 rounded-lg space-y-1.5"
              >
                <div className="flex justify-between items-start">
                  <span className="font-bold text-slate-200 flex items-center gap-1.5">
                    <AlertTriangle size={13} className={alt.type === 'HIGH' ? 'text-rose-400' : 'text-amber-400'} />
                    {alt.title}
                  </span>
                  <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                    alt.type === 'HIGH' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {alt.type}
                  </span>
                </div>
                <p className="text-slate-400 font-mono text-[11px] truncate">{alt.target}</p>
                <p className="text-slate-300">{alt.message}</p>
                <div className="pt-1.5 border-t border-slate-800/80 text-teal-400 text-[11px]">
                  <span className="font-semibold">Solution: </span>{alt.solution}
                </div>
              </div>
            ))}
          </div>

          <div className="border-t border-slate-800 pt-3 text-center">
            <Link
              to="/dashboard/history"
              onClick={() => setShowAlertsDrawer(false)}
              className="text-xs text-teal-400 hover:underline font-semibold"
            >
              View Full Incident Logs →
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
