import React, { useState } from 'react';
import { Edit3, Trash2, Copy, Check } from 'lucide-react';

interface ScratchpadProps {
  value: string;
  onChange: (val: string) => void;
}

export const Scratchpad: React.FC<ScratchpadProps> = ({ value, onChange }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="px-4 py-2.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-700 uppercase tracking-wider">
          <Edit3 className="w-3.5 h-3.5 text-blue-600" />
          <span>Calculation Scratchpad</span>
        </div>
        <div className="flex items-center gap-2">
          {value && (
            <>
              <button
                type="button"
                onClick={handleCopy}
                className="p-1 text-slate-500 hover:text-slate-800 transition-colors"
                title="Copy notes"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              </button>
              <button
                type="button"
                onClick={() => onChange('')}
                className="p-1 text-slate-400 hover:text-rose-600 transition-colors"
                title="Clear scratchpad"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </>
          )}
        </div>
      </div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Break down your steps here (e.g. Let x = cost price, 1.2x = 240, x = 200)..."
        className="w-full h-32 sm:h-40 p-3 text-xs sm:text-sm font-mono text-slate-800 bg-white resize-none focus:outline-none focus:ring-1 focus:ring-blue-500"
      />
    </div>
  );
};
