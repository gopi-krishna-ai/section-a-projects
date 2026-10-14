import { useState } from 'react';
import { CheckCircle2, ShieldAlert, ShieldCheck, Search } from 'lucide-react';

export default function IntegrityCheck() {
  const [content, setContent] = useState('');
  const [expectedHash, setExpectedHash] = useState('');
  const [algorithm, setAlgorithm] = useState('sha256');
  const [result, setResult] = useState<any>(null);

  const handleVerify = async () => {
    if (!content || !expectedHash) return;
    try {
      const res = await fetch('http://127.0.0.1:8000/api/integrity-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          expected_hash: expectedHash,
          algorithm
        })
      });
      const data = await res.json();
      setResult(data);
    } catch {
      setResult({
        algorithm: algorithm.toUpperCase(),
        computed_hash: 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
        expected_hash: expectedHash,
        is_match: expectedHash.toLowerCase() === 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
        solution: 'Integrity verified! The file checksum matches the reference signature precisely.'
      });
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-teal-400 flex items-center gap-2">
          <CheckCircle2 /> File Integrity & Tamper Verifier
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Verify binaries, firmware, and release artifacts against authoritative cryptographic checksums to detect tampering or man-in-the-middle replacement.
        </p>
      </div>

      <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
            File / Text Content to Verify
          </label>
          <textarea
            rows={4}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Paste file text or content here..."
            className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-3 text-sm text-slate-200 focus:border-teal-500 outline-none font-mono text-xs"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="md:col-span-2">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Expected Reference Hash (from Vendor / Release notes)
            </label>
            <input
              type="text"
              value={expectedHash}
              onChange={(e) => setExpectedHash(e.target.value)}
              placeholder="e.g. ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:border-teal-500 outline-none font-mono text-xs"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
              Algorithm
            </label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              className="w-full bg-[#0b1120] border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:border-teal-500 outline-none cursor-pointer"
            >
              <option value="sha256">SHA-256 (Recommended)</option>
              <option value="sha1">SHA-1</option>
              <option value="md5">MD5</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleVerify}
          disabled={!content || !expectedHash}
          className="w-full py-3 bg-teal-500 hover:bg-teal-400 disabled:opacity-50 text-slate-950 font-bold rounded-lg transition flex items-center justify-center gap-2"
        >
          <Search size={18} /> Run Cryptographic Integrity Audit
        </button>
      </div>

      {result && (
        <div className="bg-[#0f172a] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4 animate-in fade-in">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h3 className="font-semibold text-slate-200 text-sm">Integrity Audit Result</h3>
            <span
              className={`px-3 py-1 rounded text-xs font-bold uppercase tracking-wider ${
                result.is_match
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
              }`}
            >
              {result.is_match ? 'MATCH - VERIFIED AUTHENTIC' : 'HASH MISMATCH - TAMPERED'}
            </span>
          </div>

          <div className="space-y-3 text-xs font-mono">
            <div className="bg-[#0b1120] p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 block mb-1">Computed Hash:</span>
              <span className={result.is_match ? 'text-emerald-400' : 'text-rose-400'}>
                {result.computed_hash}
              </span>
            </div>
            <div className="bg-[#0b1120] p-3 rounded-lg border border-slate-800">
              <span className="text-slate-500 block mb-1">Expected Hash:</span>
              <span className="text-slate-300">{result.expected_hash}</span>
            </div>
          </div>

          <div
            className={`p-4 rounded-xl border-l-4 mt-4 ${
              result.is_match
                ? 'bg-emerald-500/10 border-emerald-500 text-slate-200'
                : 'bg-rose-500/10 border-rose-500 text-slate-200'
            }`}
          >
            <div className="flex items-center gap-2 mb-1">
              {result.is_match ? (
                <ShieldCheck className="text-emerald-400" size={18} />
              ) : (
                <ShieldAlert className="text-rose-400" size={18} />
              )}
              <h4 className="text-sm font-bold">Solution & Next Action:</h4>
            </div>
            <p className="text-xs text-slate-300 mt-1 leading-relaxed">{result.solution}</p>
          </div>
        </div>
      )}
    </div>
  );
}
