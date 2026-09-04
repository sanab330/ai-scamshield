import React, { useState } from 'react';
import { MessageSquare, Shield, AlertTriangle, Sparkles, Send, RefreshCw, CheckCircle2 } from 'lucide-react';
import RiskMeter from '../components/RiskMeter';
import ExplanationCard from '../components/ExplanationCard';
import RecommendationBanner from '../components/RecommendationBanner';
import { scanMessage } from '../services/api';

const SAMPLE_PRESETS = [
  {
    label: 'Bank KYC Threat',
    type: 'threat',
    text: 'URGENT: Your SBI account is suspended due to pending KYC. Click http://sbi-kyc-update.xyz now or face ₹10,000 penalty.',
  },
  {
    label: 'Electricity Cutoff',
    type: 'threat',
    text: 'Dear consumer, your electricity power will be disconnected tonight at 9:30 PM due to unpaid bill. Call electricity officer 9876543210 immediately.',
  },
  {
    label: 'Telegram Job Offer',
    type: 'threat',
    text: 'Earn ₹3000 to ₹8000 daily by simply liking YouTube videos on Telegram. Daily payout to UPI. Contact WhatsApp 9876501234 now.',
  },
  {
    label: 'KBC Lottery Win',
    type: 'threat',
    text: 'CONGRATULATIONS! Your number won ₹25,00,000 in KBC WhatsApp Lucky Draw. Contact Manager Rana on WhatsApp 9811223344 to claim.',
  },
  {
    label: 'Normal: Delivery Alert',
    type: 'legit',
    text: 'Your Amazon order #402-9182301 has been dispatched with delivery partner ATS. Track your package on your Amazon mobile app.',
  },
  {
    label: 'Normal: Friend Chat',
    type: 'legit',
    text: 'Hey, are we still catching up for lunch today at 1 PM near the office cafeteria?',
  },
];

export default function MessageScanner() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (overrideText) => {
    const textToScan = overrideText !== undefined ? overrideText : text;
    if (!textToScan.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const res = await scanMessage(textToScan);
      setResult(res);
    } catch (err) {
      console.error('Scan error:', err);
      setError(err.message || 'Error occurred while scanning message');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPreset = (presetText) => {
    setText(presetText);
    handleScan(presetText);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
            <MessageSquare className="w-6 h-6 text-cyan-400" />
            <span>AI Message & SMS Scanner</span>
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Detects bank impersonation, urgent threats, fake lotteries, and credential solicitation with zero cloud leakage.
          </p>
        </div>
      </div>

      {/* Input Section */}
      <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
          Paste Message Text or SMS:
        </label>
        <textarea
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste suspected SMS, WhatsApp message, Telegram job offer, or bank notification here..."
          className="w-full p-4 rounded-xl bg-slate-950/80 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-sm text-slate-100 placeholder-slate-500 resize-none outline-none font-mono leading-relaxed"
        />

        {/* Quick Sample Presets */}
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
            Quick Test Presets (Click to analyze):
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_PRESETS.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectPreset(preset.text)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all cursor-pointer ${
                  preset.type === 'threat'
                    ? 'bg-red-950/30 text-red-300 border-red-800/40 hover:bg-red-900/40'
                    : 'bg-emerald-950/30 text-emerald-300 border-emerald-800/40 hover:bg-emerald-900/40'
                }`}
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/60">
          <span className="text-[11px] text-slate-500">
            🔒 PII Redaction: Phone numbers & accounts are automatically masked.
          </span>
          <button
            disabled={loading || !text.trim()}
            onClick={() => handleScan()}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 transition cursor-pointer"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Analyzing On-Device...</span>
              </>
            ) : (
              <>
                <Shield className="w-4 h-4" />
                <span>Inspect Safety Risk</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-xl bg-red-950/50 border border-red-800 text-red-300 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Analysis Results Display */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
          {/* Left Column: Risk Meter & Recommendation Banner */}
          <div className="lg:col-span-5 space-y-4">
            <RiskMeter
              score={result.risk_score}
              level={result.risk_level}
              status={result.status}
              confidence={result.confidence}
            />

            <RecommendationBanner
              scanId={result.id}
              recommendation={result.recommendation}
              riskScore={result.risk_score}
            />
          </div>

          {/* Right Column: Explainable AI Attribution Breakdown */}
          <div className="lg:col-span-7">
            <ExplanationCard
              explanation={result.explanation}
              detectedSignals={result.detected_signals}
            />
          </div>
        </div>
      )}
    </div>
  );
}
