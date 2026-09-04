import React from 'react';
import { HelpCircle, BarChart3, Info } from 'lucide-react';

export default function ExplanationCard({ explanation, detectedSignals }) {
  if (!explanation) return null;

  const attributions = explanation.attributions || [];

  return (
    <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Why Was This Flagged?
          </h3>
        </div>
        <span className="text-[11px] font-mono text-cyan-400 bg-cyan-950/50 px-2 py-0.5 rounded border border-cyan-800/50">
          Explainable AI (XAI)
        </span>
      </div>

      {/* Summary Headline */}
      <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/60">
        <p className="text-xs text-slate-300 leading-relaxed font-medium">
          {explanation.summary}
        </p>
      </div>

      {/* Detected Scam Signals Chips */}
      {detectedSignals && detectedSignals.length > 0 && (
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
            Detected Fraud Patterns:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {detectedSignals.map((sig, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg text-xs font-medium bg-red-950/40 text-red-300 border border-red-800/50 flex items-center gap-1.5"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                {sig}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Attribution Progress Bars */}
      <div>
        <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
          Signal Contribution Breakdown:
        </span>
        <div className="space-y-3">
          {attributions.map((attr, idx) => {
            // Color variations for bars
            const barColors = [
              'bg-gradient-to-r from-cyan-500 to-blue-500',
              'bg-gradient-to-r from-amber-500 to-orange-500',
              'bg-gradient-to-r from-red-500 to-rose-500',
              'bg-gradient-to-r from-purple-500 to-indigo-500',
            ];
            const color = barColors[idx % barColors.length];

            return (
              <div key={idx} className="bg-slate-950/40 p-2.5 rounded-xl border border-slate-800/50">
                <div className="flex justify-between items-center text-xs mb-1.5">
                  <span className="font-semibold text-slate-200">{attr.factor}</span>
                  <span className="font-mono font-bold text-cyan-400">{attr.percentage}%</span>
                </div>
                {/* Progress bar */}
                <div className="w-full bg-slate-800/80 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${color} transition-all duration-700 ease-out`}
                    style={{ width: `${attr.percentage}%` }}
                  ></div>
                </div>
                <p className="text-[11px] text-slate-400 mt-1.5 leading-normal">
                  {attr.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
