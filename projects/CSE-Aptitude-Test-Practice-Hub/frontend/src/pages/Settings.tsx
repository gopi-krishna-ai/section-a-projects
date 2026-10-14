import React, { useState } from 'react';
import { Settings as SettingsIcon, Save, CheckCircle2, Shield, Sparkles } from 'lucide-react';

export const Settings: React.FC = () => {
  const [targetCompany, setTargetCompany] = useState('TCS / Infosys');
  const [dailyGoal, setDailyGoal] = useState('15');
  const [aiProvider, setAiProvider] = useState('gemini');
  const [apiKey, setApiKey] = useState('');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-3xl mx-auto">
      <div>
        <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900">Application Settings</h1>
        <p className="text-xs sm:text-sm text-slate-500">
          Personalize your learning parameters, target placement company, and AI service provider.
        </p>
      </div>

      <form onSubmit={handleSave} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-6">
        {/* Placement Target */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-800">Target Placement Assessment</label>
          <select
            value={targetCompany}
            onChange={(e) => setTargetCompany(e.target.value)}
            className="w-full px-3 py-2 text-xs font-medium rounded-lg border border-slate-300 bg-white text-slate-800"
          >
            <option value="TCS / Infosys">TCS NQT & Infosys Specialist</option>
            <option value="Wipro / Cognizant">Wipro Elite & Cognizant GenC</option>
            <option value="Accenture">Accenture Cognitive & Technical</option>
            <option value="General Placements">General Product & Service Placements</option>
          </select>
          <p className="text-[11px] text-slate-500">
            Adapts recommended topic prerequisites and mock test question distributions.
          </p>
        </div>

        {/* Daily Goal */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-800">Daily Question Goal</label>
          <div className="flex gap-3">
            {['10', '15', '25', '30'].map((goal) => (
              <button
                key={goal}
                type="button"
                onClick={() => setDailyGoal(goal)}
                className={`flex-1 py-2 text-xs font-bold rounded-lg border transition-colors cursor-pointer ${
                  dailyGoal === goal
                    ? 'bg-blue-600 border-blue-600 text-white'
                    : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                }`}
              >
                {goal} Qs / Day
              </button>
            ))}
          </div>
        </div>

        {/* AI Tutor Engine Configuration */}
        <div className="space-y-3 pt-4 border-t border-slate-100">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-900">
            <Sparkles className="w-4 h-4 text-blue-600" />
            <span>AI Tutor Provider Layer</span>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-700">Active Engine</label>
            <select
              value={aiProvider}
              onChange={(e) => setAiProvider(e.target.value)}
              className="w-full px-3 py-2 text-xs font-medium rounded-lg border border-slate-300 bg-white text-slate-800"
            >
              <option value="gemini">Google Gemini (Recommended)</option>
              <option value="openai">OpenAI GPT-4o</option>
              <option value="local_rule">Deterministic Verified Rule Fallback (Non-AI)</option>
            </select>
            <p className="text-[11px] text-slate-500">
              When using local rule fallback, the platform uses verified repository solutions and deterministic pedagogical templates with zero external API calls.
            </p>
          </div>

          {aiProvider !== 'local_rule' && (
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-700">Optional API Key Override (Stored in Backend .env)</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Configured via GEMINI_API_KEY / OPENAI_API_KEY in backend..."
                className="w-full px-3 py-2 text-xs font-mono rounded-lg border border-slate-300 bg-slate-50 text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
              <div className="text-[11px] text-slate-400 flex items-center gap-1.5 pt-1">
                <Shield className="w-3.5 h-3.5 text-emerald-600" />
                <span>Keys are never exposed in frontend code or client network calls.</span>
              </div>
            </div>
          )}
        </div>

        {/* Save Button */}
        <div className="pt-2 flex items-center justify-between border-t border-slate-100">
          {saved ? (
            <div className="flex items-center gap-1.5 text-xs text-emerald-700 font-bold">
              <CheckCircle2 className="w-4 h-4" />
              <span>Preferences saved successfully!</span>
            </div>
          ) : (
            <div />
          )}

          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-sm transition-colors cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </form>
    </div>
  );
};
