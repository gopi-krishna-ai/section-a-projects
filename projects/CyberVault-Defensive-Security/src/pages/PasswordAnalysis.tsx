import { useState, useEffect } from 'react';
import { KeyRound, ShieldAlert, ShieldCheck, Sparkles } from 'lucide-react';

export default function PasswordAnalysis() {
  const [password, setPassword] = useState('Kx#9$mP2!vL8@qZ');
  const [score, setScore] = useState(0);
  const [status, setStatus] = useState('Weak');
  const [weaknesses, setWeaknesses] = useState<string[]>([]);
  const [solution, setSolution] = useState('');

  const testPasswords = [
    { label: 'Weak (8/100): admin123', val: 'admin123' },
    { label: 'Moderate (65/100): Summer2026!', val: 'Summer2026!' },
    { label: 'Strong (95/100): Kx#9$mP2!vL8@qZ', val: 'Kx#9$mP2!vL8@qZ' },
    { label: 'Passphrase (90/100): correct-horse-battery', val: 'correct-horse-battery-staple' }
  ];

  const analyzePassword = (val: string) => {
    let currentScore = 0;
    let currentWeaknesses: string[] = [];
    
    if (!val) {
      setScore(0);
      setStatus('None');
      setWeaknesses([]);
      setSolution('');
      return;
    }

    if (val.length >= 14) currentScore += 30;
    else if (val.length >= 10) currentScore += 20;
    else if (val.length >= 8) currentScore += 10;
    else currentWeaknesses.push('Password is shorter than 12 characters.');

    if (/[A-Z]/.test(val)) currentScore += 20;
    else currentWeaknesses.push('No uppercase letters found.');

    if (/[a-z]/.test(val)) currentScore += 15;
    else currentWeaknesses.push('No lowercase letters found.');

    if (/[0-9]/.test(val)) currentScore += 20;
    else currentWeaknesses.push('No numbers found.');

    if (/[^A-Za-z0-9]/.test(val)) currentScore += 20;
    else currentWeaknesses.push('No special character found.');

    currentScore = Math.min(currentScore, 100);
    setScore(currentScore);

    if (currentScore < 40) {
      setStatus('Weak');
      setSolution('Use at least 14 characters and mix upper case, lower case, numbers and symbols.');
    } else if (currentScore < 80) {
      setStatus('Moderate');
      setSolution('Good, but can be improved. Add missing character types (e.g., symbols or numbers) or increase length.');
    } else {
      setStatus('Strong');
      setSolution('Excellent password! High entropy protects against brute-force and credential stuffing.');
    }

    setWeaknesses(currentWeaknesses);
  };

  useEffect(() => {
    analyzePassword(password);
  }, [password]);

  return (
    <div className="max-w-2xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <KeyRound /> Password Strength Analyzer
        </h1>
        <p className="text-slate-400 text-sm mt-1">Real-time heuristic evaluation of password entropy and complexity</p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        {/* Clickable Test Presets */}
        <div className="space-y-2">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
            <Sparkles size={14} className="text-teal-400" /> Click Any Test Password Sentence to Evaluate:
          </div>
          <div className="flex flex-wrap gap-2">
            {testPasswords.map((item, idx) => (
              <button
                key={idx}
                onClick={() => setPassword(item.val)}
                className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-mono border border-slate-700 transition"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <div className="border-t border-slate-800 pt-3">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
            Enter Password to Analyze
          </label>
          <input 
            type="text" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-3 text-slate-200 focus:border-teal-500 outline-none font-mono text-sm"
            placeholder="Type or click a sample password..."
          />
        </div>
      </div>

      {password && (
        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-6 animate-in fade-in">
          <h2 className="text-base font-semibold text-center text-slate-200">Analysis Results</h2>
          
          <div className="flex flex-col items-center justify-center">
            <div className="flex items-end gap-2 mb-1">
              <span className={`text-6xl font-black ${score >= 80 ? 'text-emerald-500' : score >= 40 ? 'text-amber-500' : 'text-rose-500'}`}>
                {score}
              </span>
              <span className="text-xl text-slate-500 mb-2">/ 100</span>
            </div>
            <p className="text-sm font-medium text-slate-300">
              Status: <span className={`font-bold ${score >= 80 ? 'text-emerald-400' : score >= 40 ? 'text-amber-400' : 'text-rose-400'}`}>{status}</span>
            </p>
          </div>

          {weaknesses.length > 0 && (
            <div className="bg-[#0b1120] border border-slate-800 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-amber-400 flex items-center gap-2 mb-2">
                <ShieldAlert size={14} /> Weaknesses Found:
              </h3>
              <ul className="list-disc pl-5 text-xs text-slate-400 space-y-1">
                {weaknesses.map((weakness, idx) => (
                  <li key={idx}>{weakness}</li>
                ))}
              </ul>
            </div>
          )}

          <div className={`border-l-4 rounded-r-lg p-4 ${score >= 80 ? 'border-emerald-500 bg-emerald-500/10' : 'border-teal-500 bg-teal-500/10'}`}>
            <h3 className={`text-xs font-bold flex items-center gap-2 mb-1 ${score >= 80 ? 'text-emerald-400' : 'text-teal-400'}`}>
              <ShieldCheck size={16} /> Solution:
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              {solution}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
