import { useState, useEffect } from 'react';
import { History, Search, ShieldCheck, ShieldAlert, ArrowUpDown } from 'lucide-react';

export default function ScanHistory() {
  const [history, setHistory] = useState<any[]>([]);
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/scans/history');
      const data = await res.json();
      setHistory(data.history || []);
    } catch {
      // Fallback sample history
      setHistory([
        { id: '1', tool: 'Network Scan', target: '192.168.1.10', risk: 'HIGH', score: 85, timestamp: '2026-10-12 09:42', findings: ['Port 23 (Telnet) unencrypted open'], solution: 'Close unused ports and enforce SSH.' },
        { id: '2', tool: 'Phishing Detector', target: 'http://secure-login.xyz', risk: 'HIGH', score: 92, timestamp: '2026-10-12 09:15', findings: ['Credential harvester'], solution: 'Block URL on perimeter firewall.' },
        { id: '3', tool: 'Password Analysis', target: 'Password (9 chars)', risk: 'MEDIUM', score: 55, timestamp: '2026-10-11 18:03', findings: ['Below 12 characters'], solution: 'Enforce minimum 14-char policy.' },
      ]);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const filtered = history.filter((item) => {
    const matchesFilter = filter === 'ALL' || item.risk === filter;
    const matchesSearch =
      item.tool.toLowerCase().includes(search.toLowerCase()) ||
      item.target.toLowerCase().includes(search.toLowerCase()) ||
      item.solution.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
            <History /> System Scan History & Records
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Complete audit trail of previous defensive security scans conducted across all modules.
          </p>
        </div>
        <button
          onClick={fetchHistory}
          className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-xs text-slate-300 transition"
        >
          Refresh Log
        </button>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-4 flex flex-col md:flex-row gap-3 justify-between items-center">
        <div className="relative w-full md:w-80">
          <Search size={16} className="absolute left-3 top-3 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search scans, targets, or solutions..."
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 outline-none focus:border-teal-500"
          />
        </div>

        <div className="flex gap-2 w-full md:w-auto">
          {['ALL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
            <button
              key={lvl}
              onClick={() => setFilter(lvl)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                filter === lvl
                  ? 'bg-teal-500 text-slate-950'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        {filtered.map((scan) => (
          <div
            key={scan.id}
            className="bg-[#0f172a] border border-slate-800 hover:border-slate-700 transition rounded-xl p-5 space-y-3 shadow-lg"
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-200 text-sm">{scan.tool}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                      scan.risk === 'HIGH'
                        ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                        : scan.risk === 'MEDIUM'
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}
                  >
                    {scan.risk}
                  </span>
                </div>
                <p className="text-xs text-teal-400 font-mono mt-0.5">{scan.target}</p>
              </div>
              <span className="text-[11px] text-slate-500">{scan.timestamp}</span>
            </div>

            {scan.findings && (
              <div className="bg-[#0b1120] p-3 rounded-lg border border-slate-800 text-xs text-slate-400 space-y-1">
                <span className="font-semibold text-slate-300">Identified Findings:</span>
                <ul className="list-disc pl-4 space-y-0.5 marker:text-teal-400">
                  {scan.findings.map((f: string, i: number) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="border-t border-slate-800/80 pt-2 text-xs flex items-start gap-1.5">
              <ShieldCheck size={14} className="text-teal-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-teal-400">Immediate Solution: </span>
                <span className="text-slate-300">{scan.solution}</span>
              </div>
            </div>
          </div>
        ))}

        {filtered.length === 0 && (
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-12 text-center text-slate-500 text-sm">
            No previous scans match the specified query.
          </div>
        )}
      </div>
    </div>
  );
}
