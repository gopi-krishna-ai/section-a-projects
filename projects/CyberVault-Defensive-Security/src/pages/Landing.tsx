import { Link } from 'react-router-dom';
import { Shield, KeyRound, FileSearch, BarChart3 } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#0b1120] text-slate-300 font-sans selection:bg-teal-500/30">
      <header className="flex justify-between items-center p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg border border-teal-500/30 flex items-center justify-center bg-teal-500/10 text-teal-400">
            <Shield size={20} />
          </div>
          <div>
            <h1 className="font-bold text-teal-400 tracking-wide text-lg">CyberVault</h1>
            <p className="text-xs text-slate-500">Defensive security tools</p>
          </div>
        </div>
        <div className="flex gap-4 text-sm font-medium">
          <Link to="/login" className="text-teal-400 hover:text-teal-300 border-b border-teal-500/50 pb-1">User login</Link>
          <Link to="/login" className="text-teal-400 hover:text-teal-300 border-b border-teal-500/50 pb-1">Admin login</Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-20 flex flex-col md:flex-row gap-16 items-center">
        <div className="flex-1 space-y-8">
          <h1 className="text-5xl md:text-6xl font-bold leading-tight">
            <span className="text-teal-400 drop-shadow-[0_0_15px_rgba(45,212,191,0.4)]">Run common</span><br/>
            <span className="text-teal-400 drop-shadow-[0_0_15px_rgba(45,212,191,0.4)]">security checks</span><br/>
            <span className="text-teal-400 drop-shadow-[0_0_15px_rgba(45,212,191,0.4)]">from one</span><br/>
            <span className="text-teal-400 drop-shadow-[0_0_15px_rgba(45,212,191,0.4)]">dashboard.</span>
          </h1>
          
          <p className="text-slate-400 text-lg max-w-lg leading-relaxed">
            Test a password, hash and verify a file, read through a log, check a link for phishing, or scan the ports on a machine you're allowed to test. Every result is saved and can be exported as a PDF.
          </p>

          <div className="flex gap-4">
            <Link to="/login" className="px-6 py-3 bg-teal-600/10 border border-teal-500 text-teal-400 rounded-lg hover:bg-teal-500/20 transition-colors font-medium">
              Sign in
            </Link>
            <Link to="/login" className="px-6 py-3 bg-slate-800 border border-slate-700 text-slate-200 rounded-lg hover:bg-slate-700 transition-colors font-medium">
              Create account
            </Link>
          </div>
        </div>

        <div className="flex-1">
          <div className="bg-[#0f172a]/80 border border-amber-500/30 rounded-xl p-6 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/5 rounded-full blur-3xl"></div>
            <p className="text-xs text-slate-500 font-mono mb-4">example result: password analysis</p>
            
            <div className="flex items-end gap-2 mb-4">
              <span className="text-5xl font-bold text-amber-500">75</span>
              <span className="text-slate-500 mb-1">/ 100</span>
              <span className="ml-auto text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-1 rounded border border-amber-500/20">MODERATE</span>
            </div>
            
            <div className="w-full bg-slate-800 rounded-full h-2 mb-8">
              <div className="bg-amber-500 h-2 rounded-full" style={{ width: '75%' }}></div>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="text-sm font-semibold text-slate-200 mb-1">Weakness found</h4>
                <p className="text-sm text-slate-400">Include at least one special character.</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-slate-200 mb-1">Recommendation</h4>
                <p className="text-sm text-slate-400">Add special characters or numbers to make it stronger.</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border border-teal-500/30 rounded-xl p-6 bg-teal-500/5 hover:bg-teal-500/10 transition-colors">
            <KeyRound className="text-teal-400 mb-4" size={24} />
            <h3 className="text-lg font-semibold text-teal-400 mb-2">Check</h3>
            <p className="text-sm text-slate-400">Password strength, a password generator, URL checks, and a phishing model trained on URL features.</p>
          </div>
          
          <div className="border border-fuchsia-500/30 rounded-xl p-6 bg-fuchsia-500/5 hover:bg-fuchsia-500/10 transition-colors">
            <FileSearch className="text-fuchsia-400 mb-4" size={24} />
            <h3 className="text-lg font-semibold text-fuchsia-400 mb-2">Inspect</h3>
            <p className="text-sm text-slate-400">File hashes and integrity checks, plus a log analyzer that picks out failed logins, errors and warnings.</p>
          </div>

          <div className="border border-emerald-500/30 rounded-xl p-6 bg-emerald-500/5 hover:bg-emerald-500/10 transition-colors">
            <BarChart3 className="text-emerald-400 mb-4" size={24} />
            <h3 className="text-lg font-semibold text-emerald-400 mb-2">Review</h3>
            <p className="text-sm text-slate-400">A dashboard of scan activity and risk, a full history, and a downloadable PDF report.</p>
          </div>
        </div>
        <p className="text-xs text-slate-600 mt-8 text-center">Built for learning and defensive analysis. Only scan systems you have permission to test.</p>
      </section>
    </div>
  );
}
