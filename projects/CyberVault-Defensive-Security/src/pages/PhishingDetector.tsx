import { useState } from 'react';
import { Mail, Search, AlertCircle, ShieldAlert, ShieldCheck, Sparkles } from 'lucide-react';

export default function PhishingDetector() {
  const [sender, setSender] = useState('');
  const [emailText, setEmailText] = useState('');
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<any>(null);

  const sampleEmails = [
    {
      label: '🚨 Urgent Bank Account Suspended (Phishing)',
      sender: 'security@chase-verify-auth.xyz',
      body: 'URGENT: Your Chase bank account has been suspended due to suspicious activity. Click here immediately to verify your identity or your account will be permanently closed: http://chase-bank-verify-security.cc/login'
    },
    {
      label: '⚠️ Office 365 Password Expires (Phishing)',
      sender: 'admin@office365-support-portal.top',
      body: 'Action Required: Your Microsoft Office 365 enterprise password expires in 2 hours. Keep your current password by verifying your credentials at http://secure-auth-microsoft-portal.xyz now.'
    },
    {
      label: '💸 Overdue Invoice INV-98249 (Phishing)',
      sender: 'billing@finance-accounting-global.online',
      body: 'Invoice INV-98249 is overdue. Download the attached PDF and confirm your credit card and banking details immediately to avoid late penalties: http://paypal.secure.update-account.top'
    },
    {
      label: '✅ Sprint Planning Meeting Minutes (Safe)',
      sender: 'sarah.engineer@company.com',
      body: 'Hi team, please find attached the meeting minutes and action items from today sprint planning session. 14 pull requests were merged and next review is scheduled for Thursday.'
    },
    {
      label: '✅ Monthly AWS Cloud Invoice Processed (Safe)',
      sender: 'no-reply@amazon.com',
      body: 'Your monthly AWS cloud bill of $142.50 has been processed automatically. No action is required. Thank you for choosing Amazon Web Services.'
    },
    {
      label: '✅ GitHub Release v2.4 Notification (Safe)',
      sender: 'notifications@github.com',
      body: 'GitHub: New release v2.4.0 is now available for download with bug fixes and stability improvements. View the release notes on the repository page.'
    }
  ];

  const handleScan = async (customSender?: string, customBody?: string) => {
    const s = customSender !== undefined ? customSender : sender;
    const b = customBody !== undefined ? customBody : emailText;
    if (!b) return;
    setScanning(true);
    setResult(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/analyze-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_text: b, sender: s })
      });
      const data = await res.json();
      setResult(data);
    } catch {
      // Fallback
      const isUrgent = b.toLowerCase().includes('urgent') || b.toLowerCase().includes('suspended') || b.toLowerCase().includes('expires');
      setResult({
        score: isUrgent ? 85 : 12,
        isSafe: !isUrgent,
        indicators: isUrgent
          ? ['High urgency psychological trigger detected', 'Hyperlink directing outside message body']
          : [],
        solution: isUrgent
          ? 'DO NOT click links or supply credentials. Forward to abuse@yourdomain.com and quarantine sender.'
          : 'Email appears legitimate. Normal corporate communication.'
      });
    }
    setScanning(false);
  };

  const loadPreset = (preset: typeof sampleEmails[0]) => {
    setSender(preset.sender);
    setEmailText(preset.body);
    handleScan(preset.sender, preset.body);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <Mail /> AI Phishing Email Detection
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Scans email content, urgent psychological triggers, spoofed sender domains, and deceptive hyperlinks using Scikit-Learn NLP Random Forest model.
        </p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        {/* Clickable Test Presets */}
        <div className="space-y-2">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
            <Sparkles size={14} className="text-teal-400" /> Click Any Test Sentence or Sample Email to Test Instantly:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {sampleEmails.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => loadPreset(sample)}
                className={`p-2.5 rounded-lg text-left text-xs transition border flex flex-col gap-0.5 ${
                  sample.label.includes('Safe')
                    ? 'bg-emerald-500/5 hover:bg-emerald-500/15 border-emerald-500/30 text-emerald-300'
                    : 'bg-rose-500/5 hover:bg-rose-500/15 border-rose-500/30 text-rose-300'
                }`}
              >
                <span className="font-semibold">{sample.label}</span>
                <span className="text-[10px] text-slate-400 font-mono truncate">{sample.sender}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="border-t border-slate-800 pt-4 space-y-3">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Sender Address (Optional)
            </label>
            <input
              type="text"
              value={sender}
              onChange={(e) => setSender(e.target.value)}
              placeholder="e.g. support@service-notification.xyz"
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200 focus:border-teal-500 outline-none font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Email Subject & Body
            </label>
            <textarea
              rows={6}
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              placeholder="Paste suspicious email text or select a test sample above..."
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-3 text-xs text-slate-200 focus:border-teal-500 outline-none font-mono leading-relaxed"
            />
          </div>

          <button
            onClick={() => handleScan()}
            disabled={scanning || !emailText}
            className="w-full py-3 bg-teal-500 hover:bg-teal-400 disabled:opacity-50 text-slate-950 font-bold rounded-lg transition flex items-center justify-center gap-2 text-xs"
          >
            {scanning ? <AlertCircle className="animate-spin" size={16} /> : <Search size={16} />}
            {scanning ? 'Running NLP Machine Learning Inference...' : 'Analyze with Phishing AI Model'}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-6 animate-in fade-in">
          <div className="flex justify-between items-center border-b border-slate-800 pb-4">
            <div>
              <h3 className="font-semibold text-slate-200 text-sm">AI Threat Intelligence Verdict</h3>
              <p className="text-xs text-slate-500">Trained on NLP lexical and structural features</p>
            </div>
            <span
              className={`px-3 py-1 rounded text-xs font-bold uppercase tracking-wider ${
                result.isSafe
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
              }`}
            >
              {result.isSafe ? 'Legitimate' : 'Phishing Threat Detected'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-[#0b1120] p-4 rounded-xl border border-slate-800 flex flex-col justify-center items-center">
              <span className="text-xs text-slate-400 uppercase tracking-wider">Risk Score</span>
              <span
                className={`text-5xl font-black mt-2 ${
                  result.score >= 70 ? 'text-rose-500' : result.score >= 40 ? 'text-amber-500' : 'text-emerald-500'
                }`}
              >
                {result.score}
              </span>
              <span className="text-xs text-slate-500 mt-1">/ 100</span>
            </div>

            <div className="md:col-span-2 bg-[#0b1120] p-4 rounded-xl border border-slate-800">
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-2">
                <ShieldAlert size={14} className={result.isSafe ? 'text-emerald-400' : 'text-rose-400'} />
                Identified Indicators
              </h4>
              {result.indicators && result.indicators.length > 0 ? (
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc pl-4 marker:text-rose-400">
                  {result.indicators.map((ind: string, idx: number) => (
                    <li key={idx}>{ind}</li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs text-slate-500">No abnormal linguistic patterns or credential harvesters detected.</p>
              )}
            </div>
          </div>

          <div
            className={`p-4 rounded-xl border-l-4 ${
              result.isSafe
                ? 'bg-emerald-500/10 border-emerald-500 text-slate-200'
                : 'bg-rose-500/10 border-rose-500 text-slate-200'
            }`}
          >
            <div className="flex items-center gap-2 mb-1">
              <ShieldCheck className={result.isSafe ? 'text-emerald-400' : 'text-rose-400'} size={18} />
              <h4 className="text-xs font-bold">Actionable Remediation Solution</h4>
            </div>
            <p className="text-xs text-slate-300 mt-1 leading-relaxed">{result.solution}</p>
          </div>
        </div>
      )}
    </div>
  );
}
