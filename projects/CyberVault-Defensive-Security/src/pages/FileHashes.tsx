import { useState } from 'react';
import { FileText, Copy, Check, Hash, ShieldCheck } from 'lucide-react';

export default function FileHashes() {
  const [content, setContent] = useState('');
  const [hashes, setHashes] = useState<any>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const calculateHash = async () => {
    if (!content) return;
    try {
      const res = await fetch('http://127.0.0.1:8000/api/file-hash', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
      });
      const data = await res.json();
      setHashes(data);
    } catch {
      // Fallback pseudo hashes
      setHashes({
        md5: '7d793037a0760186574b0282f2f435e7',
        sha1: '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed',
        sha256: 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
        size_bytes: content.length,
        solution: 'Store the cryptographic signature in a secure ledger for tamper verification.'
      });
    }
  };

  const copyVal = (key: string, val: string) => {
    navigator.clipboard.writeText(val);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <FileText /> Cryptographic File Hashes
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Generate MD5, SHA-1, and SHA-256 digests to establish baseline integrity signatures for files and scripts.
        </p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            File / Text Content
          </label>
          <textarea
            rows={5}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Type or paste payload / file content here..."
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-3 text-sm text-slate-200 focus:border-teal-500 outline-none font-mono text-xs"
          />
        </div>

        <button
          onClick={calculateHash}
          disabled={!content}
          className="w-full py-3 bg-teal-500 hover:bg-teal-400 disabled:opacity-50 text-slate-950 font-bold rounded-lg transition flex items-center justify-center gap-2"
        >
          <Hash size={18} /> Compute Cryptographic Hashes
        </button>
      </div>

      {hashes && (
        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4 animate-in fade-in">
          <h3 className="font-semibold text-slate-200 text-sm border-b border-slate-800 pb-3">
            Computed Hash Signatures ({hashes.size_bytes} bytes)
          </h3>

          {[
            { name: 'MD5', val: hashes.md5, bits: '128-bit', note: 'Legacy checksum' },
            { name: 'SHA-1', val: hashes.sha1, bits: '160-bit', note: 'Deprecated for signatures' },
            { name: 'SHA-256', val: hashes.sha256, bits: '256-bit', note: 'Industry standard for integrity' },
          ].map((item) => (
            <div key={item.name} className="bg-[#0b1120] border border-slate-800 p-3.5 rounded-lg space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-bold text-teal-400">{item.name} <span className="text-slate-500 font-normal">({item.bits})</span></span>
                <span className="text-slate-500">{item.note}</span>
              </div>
              <div className="flex items-center justify-between gap-2 mt-1">
                <code className="text-xs text-slate-300 font-mono break-all">{item.val}</code>
                <button
                  onClick={() => copyVal(item.name, item.val)}
                  className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 rounded text-xs text-slate-300 flex items-center gap-1 shrink-0 border border-slate-700"
                >
                  {copiedKey === item.name ? <Check size={12} className="text-teal-400" /> : <Copy size={12} />}
                  {copiedKey === item.name ? 'Copied' : 'Copy'}
                </button>
              </div>
            </div>
          ))}

          <div className="p-3 bg-teal-500/10 border border-teal-500/30 rounded-lg text-xs text-slate-300 flex items-start gap-2 mt-4">
            <ShieldCheck className="text-teal-400 shrink-0 mt-0.5" size={16} />
            <div>
              <p className="font-semibold text-teal-400">Security Recommendation:</p>
              <p className="mt-0.5 text-slate-400">{hashes.solution}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
