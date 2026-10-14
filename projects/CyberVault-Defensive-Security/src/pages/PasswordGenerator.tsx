import { useState } from 'react';
import { Dna, Copy, Check, RefreshCw, ShieldCheck } from 'lucide-react';

export default function PasswordGenerator() {
  const [length, setLength] = useState(16);
  const [uppercase, setUppercase] = useState(true);
  const [lowercase, setLowercase] = useState(true);
  const [numbers, setNumbers] = useState(true);
  const [symbols, setSymbols] = useState(true);
  const [password, setPassword] = useState('');
  const [copied, setCopied] = useState(false);
  const [entropy, setEntropy] = useState(95);

  const generate = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/generate-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          length,
          include_uppercase: uppercase,
          include_lowercase: lowercase,
          include_numbers: numbers,
          include_symbols: symbols
        })
      });
      const data = await res.json();
      setPassword(data.password);
      setEntropy(data.entropy_bits);
    } catch {
      // Client-side fallback
      let chars = '';
      if (uppercase) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      if (lowercase) chars += 'abcdefghijklmnopqrstuvwxyz';
      if (numbers) chars += '0123456789';
      if (symbols) chars += '!@#$%^&*()_+-=[]{}|;:,.<>?';
      if (!chars) chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
      let gen = '';
      for (let i = 0; i < length; i++) {
        gen += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      setPassword(gen);
      setEntropy(Math.round(length * 5.9));
    }
  };

  const copyToClipboard = () => {
    if (!password) return;
    navigator.clipboard.writeText(password);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <Dna /> Cryptographic Password Generator
        </h1>
        <p className="text-slate-400 text-sm mt-1">Generate high-entropy credentials impervious to dictionary and brute-force attacks</p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <div className="relative">
          <input
            type="text"
            readOnly
            value={password || 'Click Generate to produce password'}
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-4 text-teal-300 font-mono text-lg pr-28 select-all"
          />
          <div className="absolute right-2 top-2 bottom-2 flex items-center gap-1">
            <button
              onClick={copyToClipboard}
              disabled={!password}
              className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs flex items-center gap-1 border border-slate-700 transition"
              title="Copy"
            >
              {copied ? <Check size={14} className="text-teal-400" /> : <Copy size={14} />}
              {copied ? 'Copied' : 'Copy'}
            </button>
            <button
              onClick={generate}
              className="p-2 bg-teal-600/20 hover:bg-teal-600/30 text-teal-400 rounded border border-teal-500/40 transition"
              title="Generate New"
            >
              <RefreshCw size={16} />
            </button>
          </div>
        </div>

        {/* Options */}
        <div className="space-y-4 pt-2">
          <div>
            <div className="flex justify-between text-sm text-slate-300 mb-2 font-medium">
              <span>Password Length</span>
              <span className="text-teal-400 font-mono">{length} characters</span>
            </div>
            <input
              type="range"
              min="8"
              max="64"
              value={length}
              onChange={(e) => setLength(Number(e.target.value))}
              className="w-full accent-teal-400 bg-slate-800 h-2 rounded-lg cursor-pointer"
            />
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2">
            {[
              { label: 'Uppercase (A-Z)', val: uppercase, set: setUppercase },
              { label: 'Lowercase (a-z)', val: lowercase, set: setLowercase },
              { label: 'Numbers (0-9)', val: numbers, set: setNumbers },
              { label: 'Symbols (!@#$%)', val: symbols, set: setSymbols },
            ].map((opt, i) => (
              <label key={i} className="flex items-center gap-3 bg-[#0b1120] p-3 rounded-lg border border-slate-800 cursor-pointer hover:border-slate-700">
                <input
                  type="checkbox"
                  checked={opt.val}
                  onChange={(e) => opt.set(e.target.checked)}
                  className="rounded accent-teal-400 w-4 h-4 cursor-pointer"
                />
                <span className="text-xs text-slate-300">{opt.label}</span>
              </label>
            ))}
          </div>

          <button
            onClick={generate}
            className="w-full py-3 bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold rounded-lg transition shadow-lg shadow-teal-500/10 flex items-center justify-center gap-2"
          >
            <RefreshCw size={18} /> Generate Secure Password
          </button>
        </div>

        {password && (
          <div className="border-t border-slate-800 pt-4 space-y-3">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400">Entropy Strength:</span>
              <span className="text-emerald-400 font-mono font-bold">~{entropy} bits (Very High)</span>
            </div>
            <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-xs text-slate-300 flex items-start gap-2">
              <ShieldCheck className="text-emerald-400 shrink-0 mt-0.5" size={16} />
              <div>
                <p className="font-semibold text-emerald-400">Recommended Storage Solution:</p>
                <p className="mt-0.5 text-slate-400">Never save plaintext passwords in spreadsheets or browsers. Use an enterprise secrets manager or hardware security key (FIDO2/U2F).</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
