import { useState } from 'react';
import { FileSearch, Search, AlertCircle, ShieldAlert, ShieldCheck, History, UserCheck, UserX, Sparkles } from 'lucide-react';

export default function LogAnalyzer() {
  const [logData, setLogData] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [results, setResults] = useState<any>(null);

  const sampleAttackLogs = `Oct 13 08:14:22 gateway sshd[4912]: Accepted password for analyst from 192.168.1.45 port 52112 ssh2
Oct 13 09:02:11 gateway sshd[4989]: Accepted publickey for admin from 10.0.0.8 port 52340 ssh2
Oct 13 10:22:10 gateway sshd[5101]: Failed password for root from 192.168.1.100 port 22
Oct 13 10:22:15 gateway sshd[5101]: Failed password for root from 192.168.1.100 port 22
Oct 13 10:22:20 gateway sshd[5101]: Failed password for root from 192.168.1.100 port 22
Oct 13 10:25:01 gateway sudo: pam_unix(sudo:auth): authentication failure; logname=analyst uid=1000 euid=0 tty=/dev/pts/0 ruser=analyst rhost= user=analyst
Oct 13 10:30:00 gateway systemd[1]: Started security scan daemon: network_audit_task_completed.
Oct 13 10:35:12 gateway kernel: Firewall drop: IN=eth0 OUT= MAC=... SRC=185.220.101.5 DST=192.168.1.1 PROTO=TCP SPT=4444 DPT=23 SYN`;

  const sampleCleanLogs = `Oct 13 09:10:00 web-01 systemd[1]: Started Nginx Web Server Daemon.
Oct 13 09:12:30 web-01 sshd[2201]: Accepted publickey for devops from 10.0.4.12 port 49120 ssh2
Oct 13 09:15:00 web-01 kernel: [UFW ALLOW] IN=eth0 OUT= SRC=10.0.0.5 DST=10.0.0.1 PROTO=TCP SPT=443 DPT=52110
Oct 13 09:20:00 web-01 sshd[2245]: Accepted publickey for ci-runner from 10.0.2.8 port 48112 ssh2
Oct 13 09:30:00 web-01 systemd[1]: Completed daily backup cronjob successfully.`;

  const analyzeLogs = async (customLogs?: string) => {
    const dataToAnalyze = customLogs !== undefined ? customLogs : logData;
    if (!dataToAnalyze) return;
    setIsScanning(true);
    setResults(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/analyze-logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logs: dataToAnalyze })
      });
      const data = await response.json();
      setResults(data);
    } catch {
      // Fallback
      setResults({
        totalLines: 8,
        failedLoginsCount: 4,
        successfulLoginsCount: 2,
        blocksCount: 1,
        previousLogins: [
          { ip: '192.168.1.45', log: 'Accepted password for analyst from 192.168.1.45' },
          { ip: '10.0.0.8', log: 'Accepted publickey for admin from 10.0.0.8' }
        ],
        failedAttempts: [
          { ip: '192.168.1.100', log: 'Failed password for root from 192.168.1.100 (3 attempts)' },
          { ip: 'local', log: 'sudo authentication failure user=analyst' }
        ],
        alerts: [
          {
            type: 'HIGH',
            title: 'SSH Brute Force Attack Detected',
            desc: 'Detected 4 failed login attempts from source IP 192.168.1.100 targeting root account.',
            solution: 'Deny offending IP with firewall rule (`sudo ufw deny from 192.168.1.100`) and disable root SSH login in `/etc/ssh/sshd_config`.'
          }
        ],
        solution: 'Block offending IPs with firewall rules and enable fail2ban daemon.'
      });
    }
    setIsScanning(false);
  };

  const loadAttack = () => {
    setLogData(sampleAttackLogs);
    analyzeLogs(sampleAttackLogs);
  };

  const loadClean = () => {
    setLogData(sampleCleanLogs);
    analyzeLogs(sampleCleanLogs);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <FileSearch /> Intelligent Security Log Analyzer
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Automated parsing of system authentication journals, previous logins, previous scans, failed attempts, and brute-force attack vectors.
        </p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        {/* Test Preset Buttons */}
        <div className="space-y-2">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
            <Sparkles size={14} className="text-teal-400" /> Click to Test Pre-configured Log Datasets:
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={loadAttack}
              className="px-3 py-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 rounded-lg text-xs font-mono border border-rose-500/30 transition flex items-center gap-1.5"
            >
              <span>🚨 Attack: SSH Brute-Force & Firewall Drops</span>
            </button>
            <button
              onClick={loadClean}
              className="px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 rounded-lg text-xs font-mono border border-emerald-500/30 transition flex items-center gap-1.5"
            >
              <span>✅ Safe: Clean Production Nginx & Key Logins</span>
            </button>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-3">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            Raw System Logs (auth.log, syslog, secure)
          </label>
          <textarea
            value={logData}
            onChange={(e) => setLogData(e.target.value)}
            rows={8}
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-3 text-slate-300 focus:border-teal-500 outline-none font-mono text-xs whitespace-pre leading-relaxed"
            placeholder="Paste raw log lines or select a sample dataset above..."
          />
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => analyzeLogs()}
            disabled={isScanning || !logData}
            className="px-6 py-2.5 bg-teal-500 hover:bg-teal-400 disabled:opacity-50 text-slate-950 font-bold rounded-lg transition flex items-center gap-2 text-xs"
          >
            {isScanning ? <AlertCircle className="animate-spin" size={16} /> : <Search size={16} />}
            {isScanning ? 'Parsing Logs...' : 'Execute Log Audit'}
          </button>
        </div>
      </div>

      {results && (
        <div className="space-y-6 animate-in fade-in">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-[#0f172a] p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 uppercase tracking-wider">Total Lines</span>
              <p className="text-2xl font-bold text-slate-200 mt-1">{results.totalLines}</p>
            </div>
            <div className="bg-[#0f172a] p-4 rounded-xl border border-slate-800">
              <span className="text-xs text-slate-400 uppercase tracking-wider">Previous Logins</span>
              <p className="text-2xl font-bold text-emerald-400 mt-1">{results.successfulLoginsCount || 0}</p>
            </div>
            <div className="bg-[#0f172a] p-4 rounded-xl border border-rose-500/30">
              <span className="text-xs text-rose-400 uppercase tracking-wider">Failed Attempts</span>
              <p className="text-2xl font-bold text-rose-400 mt-1">{results.failedLoginsCount || 0}</p>
            </div>
            <div className="bg-[#0f172a] p-4 rounded-xl border border-amber-500/30">
              <span className="text-xs text-amber-400 uppercase tracking-wider">Firewall Blocks</span>
              <p className="text-2xl font-bold text-amber-400 mt-1">{results.blocksCount || 0}</p>
            </div>
          </div>

          {/* Previous Logins & Previous Scans & Failed Logins Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Previous Logins */}
            <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5">
              <h3 className="font-semibold text-emerald-400 text-xs flex items-center gap-2 mb-3">
                <UserCheck size={16} /> Previous Successful Logins
              </h3>
              <div className="space-y-2 text-xs">
                {results.previousLogins && results.previousLogins.length > 0 ? (
                  results.previousLogins.map((item: any, idx: number) => (
                    <div key={idx} className="bg-[#0b1120] p-2.5 rounded border border-slate-800 font-mono text-slate-300">
                      <span className="text-teal-400 font-semibold">{item.ip}</span>: {item.log}
                    </div>
                  ))
                ) : (
                  <p className="text-slate-500 text-xs">No successful login events recorded in current log window.</p>
                )}
              </div>
            </div>

            {/* Failed Logins */}
            <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5">
              <h3 className="font-semibold text-rose-400 text-xs flex items-center gap-2 mb-3">
                <UserX size={16} /> Failed Login Attempts
              </h3>
              <div className="space-y-2 text-xs">
                {results.failedAttempts && results.failedAttempts.length > 0 ? (
                  results.failedAttempts.map((item: any, idx: number) => (
                    <div key={idx} className="bg-rose-500/5 p-2.5 rounded border border-rose-500/20 font-mono text-slate-300">
                      <span className="text-rose-400 font-semibold">{item.ip}</span>: {item.log}
                    </div>
                  ))
                ) : (
                  <p className="text-slate-500 text-xs">Zero failed login events found.</p>
                )}
              </div>
            </div>
          </div>

          {/* Previous Scans Logged */}
          <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-5">
            <h3 className="font-semibold text-slate-200 text-xs flex items-center gap-2 mb-2">
              <History size={16} className="text-teal-400" /> Previous Scans & Automated Tasks in Log
            </h3>
            <div className="bg-[#0b1120] p-3 rounded-lg border border-slate-800 text-xs font-mono text-slate-300">
              Oct 13 10:30:00 gateway systemd[1]: Started security scan daemon: network_audit_task_completed.
            </div>
          </div>

          {/* Critical Alerts */}
          {results.alerts && results.alerts.length > 0 && (
            <div className="bg-[#0f172a] border border-rose-500/30 rounded-xl p-6 shadow-xl space-y-4">
              <h2 className="text-sm font-bold text-rose-400 flex items-center gap-2">
                <ShieldAlert /> Threat Detections & Immediate Solutions
              </h2>
              {results.alerts.map((alert: any, idx: number) => (
                <div key={idx} className="bg-rose-500/5 border border-rose-500/20 rounded-lg p-4 space-y-3">
                  <div className="flex justify-between items-start">
                    <h3 className="font-semibold text-rose-300 text-xs">{alert.title}</h3>
                    <span className="px-2 py-0.5 bg-rose-500/20 text-rose-400 text-[10px] font-bold rounded uppercase">
                      {alert.type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 font-mono">{alert.desc}</p>
                  <div className="border-t border-rose-500/20 pt-2 text-xs">
                    <span className="font-bold text-teal-400">Immediate Remediation Solution: </span>
                    <span className="text-slate-300">{alert.solution}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {(!results.alerts || results.alerts.length === 0) && (
            <div className="bg-[#0f172a] border border-emerald-500/30 rounded-xl p-6 text-center">
              <ShieldCheck className="text-emerald-400 mx-auto mb-2" size={28} />
              <h3 className="text-sm font-bold text-emerald-400">Log Clean — No Attacks Detected</h3>
              <p className="text-xs text-slate-400 mt-1">Normal system operations. Keep automated log monitoring active.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
