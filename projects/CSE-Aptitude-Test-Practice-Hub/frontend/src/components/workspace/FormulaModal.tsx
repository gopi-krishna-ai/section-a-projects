import React from 'react';
import { X, Book, Sparkles } from 'lucide-react';

interface FormulaModalProps {
  isOpen: boolean;
  onClose: () => void;
  category: string;
  topicName?: string;
}

const COMMON_FORMULAS: Record<string, Array<{ name: string; formula: string; note: string }>> = {
  "Quantitative Aptitude": [
    { name: "Percentage Change", formula: "((Final - Initial) / Initial) × 100%", note: "Initial is ALWAYS the base (denominator)." },
    { name: "Profit % / Loss %", formula: "Profit% = (Profit / CP) × 100", note: "Cost Price (CP) is the default baseline." },
    { name: "Discount %", formula: "Discount% = (Discount / Marked Price) × 100", note: "Discount is always computed on Marked Price." },
    { name: "Time and Work (2 Workers)", formula: "T = (A × B) / (A + B)", note: "Fast shortcut for two workers." },
    { name: "Speed, Distance, Time", formula: "Speed = Distance / Time", note: "1 km/h = 5/18 m/s; 1 m/s = 18/5 km/h." },
    { name: "Simple Interest", formula: "SI = (P × R × T) / 100", note: "P = Principal, R = Annual Rate, T = Years." },
    { name: "Compound Interest", formula: "Amount = P(1 + R/100)^T", note: "Interest = Amount - Principal." }
  ],
  "Logical Reasoning": [
    { name: "Arithmetic Progression (AP)", formula: "T_n = a + (n - 1)d", note: "a = 1st term, d = common difference." },
    { name: "Geometric Progression (GP)", formula: "T_n = a × r^(n - 1)", note: "r = common ratio." },
    { name: "Directions / Shortest Path", formula: "Displacement = sqrt(Δx² + Δy²)", note: "Pythagoras theorem on cardinal coordinates." }
  ],
  "Technical Aptitude": [
    { name: "Bitwise Shift Right", formula: "x >> k = floor(x / 2^k)", note: "Rapid integer division by power of 2." },
    { name: "Bitwise Shift Left", formula: "x << k = x * 2^k", note: "Rapid integer multiplication by power of 2." },
    { name: "Odd / Even Test", formula: "(x & 1) == 0 (Even), 1 (Odd)", note: "Tests least significant bit in O(1)." }
  ]
};

export const FormulaModal: React.FC<FormulaModalProps> = ({
  isOpen,
  onClose,
  category,
  topicName
}) => {
  if (!isOpen) return null;

  const formulas = COMMON_FORMULAS[category] || COMMON_FORMULAS["Quantitative Aptitude"];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
      <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[85vh]">
        <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-2">
            <Book className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-slate-900 text-sm sm:text-base">
              Formula Reference: {topicName || category}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-5 overflow-y-auto space-y-3">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-800 flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
            <span>
              <strong>Golden Rule:</strong> Understand the intuition behind the formula. In placement exams, question wording tests if you know <em>when</em> to use a formula, not just memory.
            </span>
          </div>

          <div className="space-y-3">
            {formulas.map((item, idx) => (
              <div key={idx} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60">
                <div className="text-xs font-bold text-slate-700">{item.name}</div>
                <div className="my-1.5 font-mono text-sm font-semibold text-blue-700 bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 inline-block">
                  {item.formula}
                </div>
                <div className="text-xs text-slate-600">{item.note}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="px-5 py-3 border-t border-slate-200 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-lg bg-slate-800 text-white hover:bg-slate-900 transition-colors"
          >
            Close Reference
          </button>
        </div>
      </div>
    </div>
  );
};
