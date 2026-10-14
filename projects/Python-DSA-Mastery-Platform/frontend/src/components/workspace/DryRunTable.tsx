import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, PlayCircle, Table, CheckCircle2 } from 'lucide-react';

interface DryRunStep {
  step: number;
  action: string;
  state: Record<string, any>;
}

interface DryRunTableProps {
  steps: DryRunStep[];
}

export const DryRunTable: React.FC<DryRunTableProps> = ({ steps }) => {
  const [currentStepIdx, setCurrentStepIdx] = useState(0);

  if (!steps || steps.length === 0) {
    return (
      <div className="p-6 text-center text-slate-500 text-xs">
        No dry run trace available for this question. Use the coding workspace to trace states.
      </div>
    );
  }

  const activeStep = steps[currentStepIdx] || steps[0];
  const keys = Object.keys(activeStep.state || {});

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Table className="w-4 h-4 text-sky-400" />
          <h3 className="font-bold text-xs sm:text-sm text-white">Interactive State Dry-Run</h3>
        </div>
        <div className="text-xs font-mono text-slate-400">
          Step {currentStepIdx + 1} of {steps.length}
        </div>
      </div>

      {/* Action Description */}
      <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-sky-300 font-mono leading-relaxed">
        <span className="font-bold text-slate-400 mr-2">&gt;</span>
        {activeStep.action}
      </div>

      {/* State Variable Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {keys.map((k) => (
          <div key={k} className="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
            <span className="text-[10px] uppercase font-bold text-slate-500">{k}</span>
            <div className="text-xs font-mono font-bold text-amber-300 truncate">
              {JSON.stringify(activeStep.state[k])}
            </div>
          </div>
        ))}
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between pt-2">
        <button
          type="button"
          disabled={currentStepIdx === 0}
          onClick={() => setCurrentStepIdx((p) => Math.max(0, p - 1))}
          className="px-3 py-1.5 rounded-lg border border-slate-800 text-xs font-semibold text-slate-300 hover:bg-slate-800 transition-colors disabled:opacity-40 cursor-pointer flex items-center gap-1"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Previous Step</span>
        </button>

        <button
          type="button"
          disabled={currentStepIdx === steps.length - 1}
          onClick={() => setCurrentStepIdx((p) => Math.min(steps.length - 1, p + 1))}
          className="px-3.5 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-xs font-bold text-white transition-colors disabled:opacity-40 cursor-pointer flex items-center gap-1 shadow-sm"
        >
          <span>Next State</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
