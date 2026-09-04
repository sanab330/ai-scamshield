import React, { useState } from 'react';
import { ShieldCheck, Check, AlertTriangle, ThumbsUp, ThumbsDown, Sparkles } from 'lucide-react';
import { sendFeedback } from '../services/api';

export default function RecommendationBanner({ scanId, recommendation, riskScore }) {
  const [feedbackState, setFeedbackState] = useState(null); // 'submitted' or null
  const [submitting, setSubmitting] = useState(false);

  const handleFeedback = async (type) => {
    if (!scanId || feedbackState) return;
    try {
      setSubmitting(true);
      await sendFeedback(scanId, type);
      setFeedbackState(type);
    } catch (err) {
      console.error('Feedback error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const isThreat = riskScore > 50;

  return (
    <div className={`p-5 rounded-2xl border ${
      isThreat
        ? 'bg-gradient-to-br from-red-950/30 to-slate-900/90 border-red-800/40'
        : 'bg-gradient-to-br from-emerald-950/20 to-slate-900/90 border-emerald-800/40'
    }`}>
      {/* Title */}
      <div className="flex items-center gap-2 mb-2">
        <Sparkles className={`w-4 h-4 ${isThreat ? 'text-red-400' : 'text-emerald-400'}`} />
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
          Recommended Safe Action
        </h4>
      </div>

      {/* Main Advisory */}
      <p className="text-sm font-semibold text-white leading-relaxed mb-4">
        {recommendation}
      </p>

      {/* Probabilistic Safety Disclaimer */}
      <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/60 mb-4">
        <p className="text-[11px] text-slate-400 leading-normal">
          <strong className="text-slate-300">Privacy & Safety Notice:</strong> AI ScamShield provides calibrated risk evaluation. It is designed to assist your judgment—always independently verify unknown requesters through official published channels.
        </p>
      </div>

      {/* User Feedback Mechanism */}
      <div className="pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3">
        <span className="text-xs text-slate-400 font-medium">Was this warning helpful?</span>

        {feedbackState ? (
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-950/40 px-3 py-1 rounded-lg border border-emerald-800/50">
            <Check className="w-3.5 h-3.5" />
            <span>Thank you! Feedback recorded for local tuning.</span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <button
              disabled={submitting}
              onClick={() => handleFeedback('CORRECT')}
              className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-emerald-900/40 hover:text-emerald-300 text-slate-300 border border-slate-700 transition"
            >
              <ThumbsUp className="w-3.5 h-3.5" />
              <span>Helpful</span>
            </button>
            <button
              disabled={submitting}
              onClick={() => handleFeedback('FALSE_ALARM')}
              className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-amber-900/40 hover:text-amber-300 text-slate-300 border border-slate-700 transition"
            >
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>False Alarm</span>
            </button>
            <button
              disabled={submitting}
              onClick={() => handleFeedback('MISSED_SCAM')}
              className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-red-900/40 hover:text-red-300 text-slate-300 border border-slate-700 transition"
            >
              <ThumbsDown className="w-3.5 h-3.5" />
              <span>Missed Scam</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
