import React, { useState } from 'react';
import { X, Sparkles, ChevronRight, CheckCircle2, HelpCircle, ArrowRight } from 'lucide-react';
import { api } from '../../api/client';
import { StepGuidance } from '../../types';

interface StepTutorModalProps {
  isOpen: boolean;
  onClose: () => void;
  questionId: string;
  questionText: string;
}

const STEPS = [
  { id: 'understand', label: '1. Understand', icon: HelpCircle },
  { id: 'identify', label: '2. Identify Given', icon: CheckCircle2 },
  { id: 'plan', label: '3. Plan Approach', icon: Sparkles },
  { id: 'solve', label: '4. Step-by-Step Solve', icon: ArrowRight },
  { id: 'verify', label: '5. Sanity Check', icon: CheckCircle2 },
  { id: 'generalize', label: '6. Generalize Pattern', icon: Sparkles },
  { id: 'transfer', label: '7. Transfer Challenge', icon: ChevronRight },
];

export const StepTutorModal: React.FC<StepTutorModalProps> = ({
  isOpen,
  onClose,
  questionId,
  questionText
}) => {
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [stepData, setStepData] = useState<Record<string, StepGuidance>>({});
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const currentStepDef = STEPS[activeStepIndex];

  const loadStep = async (index: number) => {
    setActiveStepIndex(index);
    const stepDef = STEPS[index];
    if (stepData[stepDef.id]) return;

    setLoading(true);
    try {
      const res = await api.getStepGuidance(questionId, stepDef.id);
      setStepData((prev) => ({ ...prev, [stepDef.id]: res }));
    } catch (err) {
      console.error('Failed to load step guidance', err);
    } finally {
      setLoading(false);
    }
  };

  // Ensure first step is loaded
  if (!stepData[currentStepDef.id] && !loading) {
    loadStep(activeStepIndex);
  }

  const currentContent = stepData[currentStepDef.id];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm sm:text-base">Interactive AI Coach</h3>
              <p className="text-xs text-slate-500">7-Step Problem Solving Mastery Cycle</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step Tabs */}
        <div className="flex border-b border-slate-200 bg-slate-100/70 overflow-x-auto text-xs font-semibold">
          {STEPS.map((s, idx) => (
            <button
              key={s.id}
              onClick={() => loadStep(idx)}
              className={`px-3 py-2.5 whitespace-nowrap transition-colors border-b-2 flex items-center gap-1.5 ${
                activeStepIndex === idx
                  ? 'border-indigo-600 text-indigo-700 bg-white font-bold'
                  : 'border-transparent text-slate-500 hover:text-slate-800'
              }`}
            >
              <span>{s.label}</span>
            </button>
          ))}
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto space-y-4">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700">
            <span className="font-bold text-slate-900">Current Question:</span> {questionText}
          </div>

          {loading ? (
            <div className="py-12 flex flex-col items-center justify-center text-slate-400 gap-2">
              <div className="w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
              <p className="text-xs">Consulting pedagogical coach...</p>
            </div>
          ) : currentContent ? (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-indigo-50/70 border border-indigo-100">
                <h4 className="text-sm font-bold text-indigo-900 mb-2">{currentContent.title}</h4>
                <p className="text-xs sm:text-sm text-indigo-950 leading-relaxed whitespace-pre-line font-medium">
                  {currentContent.content}
                </p>
              </div>

              {currentContent.guiding_question && (
                <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl">
                  <div className="text-xs font-bold text-amber-900 mb-1">Coach Reflection Check:</div>
                  <div className="text-xs text-amber-950 font-medium">
                    {currentContent.guiding_question}
                  </div>
                </div>
              )}
            </div>
          ) : null}
        </div>

        {/* Footer Navigation */}
        <div className="px-5 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
          <button
            disabled={activeStepIndex === 0}
            onClick={() => loadStep(activeStepIndex - 1)}
            className="px-3.5 py-2 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-200 disabled:opacity-40"
          >
            Previous Step
          </button>

          {activeStepIndex < STEPS.length - 1 ? (
            <button
              onClick={() => loadStep(activeStepIndex + 1)}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 flex items-center gap-1.5 transition-colors"
            >
              <span>Next: {STEPS[activeStepIndex + 1].label}</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors"
            >
              Ready to Solve Independently
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
