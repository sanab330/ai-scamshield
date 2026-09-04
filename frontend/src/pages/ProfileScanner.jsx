import React, { useState } from 'react';
import { UserCheck, UserX, AlertTriangle, Sparkles, RefreshCw, Zap, Shield, HelpCircle } from 'lucide-react';
import RiskMeter from '../components/RiskMeter';
import { scanProfile } from '../services/api';

const PROFILE_PRESETS = [
  {
    label: 'Fake SBI Customer Care',
    type: 'threat',
    data: {
      username: 'sbi_official_helpdesk_849204',
      bio: 'Official 24/7 SBI customer support desk. DM to recover blocked money or update KYC. WhatsApp +919876501234',
      account_age_days: 4,
      followers_count: 12,
      following_count: 1450,
      has_external_link: true,
    },
  },
  {
    label: 'Crypto Doubler Bot',
    type: 'threat',
    data: {
      username: 'crypto_profit_guaranteed_99',
      bio: 'Earn 100% guaranteed profit in 24 hours! No risk, daily payouts to UPI. Join Telegram: t.me/fast_crypto_lures',
      account_age_days: 12,
      followers_count: 35,
      following_count: 2100,
      has_external_link: true,
    },
  },
  {
    label: 'Legitimate Everyday Profile',
    type: 'legit',
    data: {
      username: 'ananya_design',
      bio: 'UI/UX Designer in Bengaluru. Coffee enthusiast, watercolor painter, and tech blogger.',
      account_age_days: 730,
      followers_count: 580,
      following_count: 420,
      has_external_link: false,
    },
  },
];

export default function ProfileScanner() {
  const [formData, setFormData] = useState({
    username: 'sbi_official_helpdesk_849204',
    bio: 'Official 24/7 SBI customer support desk. DM to recover blocked money or update KYC.',
    account_age_days: 5,
    followers_count: 18,
    following_count: 1200,
    has_external_link: true,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (overrideData) => {
    const dataToScan = overrideData || formData;
    if (!dataToScan.username.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const res = await scanProfile(dataToScan);
      setResult(res);
    } catch (err) {
      console.error('Profile scan error:', err);
      setError(err.message || 'Error occurred while analyzing profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPreset = (presetData) => {
    setFormData(presetData);
    handleScan(presetData);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
          <UserX className="w-6 h-6 text-cyan-400" />
          <span>Social Media Profile & Impersonation Inspector</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Inspects publicly visible profile metadata, bio claims, and mass-following patterns to detect impersonation risks without bypassing platform privacy.
        </p>
      </div>

      {/* Input Form */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Username Handle:
            </label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              placeholder="@username"
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-sm font-mono text-white outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Account Age (approx. days):
            </label>
            <input
              type="number"
              value={formData.account_age_days}
              onChange={(e) => setFormData({ ...formData, account_age_days: parseInt(e.target.value) || 0 })}
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-sm font-mono text-white outline-none focus:border-cyan-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 mb-1">
            Public Bio / Description:
          </label>
          <textarea
            rows={2}
            value={formData.bio}
            onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
            placeholder="Paste public profile bio or about text..."
            className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white outline-none focus:border-cyan-500"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Followers Count:
            </label>
            <input
              type="number"
              value={formData.followers_count}
              onChange={(e) => setFormData({ ...formData, followers_count: parseInt(e.target.value) || 0 })}
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-sm font-mono text-white outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Following Count:
            </label>
            <input
              type="number"
              value={formData.following_count}
              onChange={(e) => setFormData({ ...formData, following_count: parseInt(e.target.value) || 0 })}
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-sm font-mono text-white outline-none focus:border-cyan-500"
            />
          </div>
        </div>

        {/* Quick Presets */}
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
            Quick Test Presets:
          </span>
          <div className="flex flex-wrap gap-2">
            {PROFILE_PRESETS.map((p, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectPreset(p.data)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition cursor-pointer ${
                  p.type === 'threat'
                    ? 'bg-red-950/30 text-red-300 border-red-800/40 hover:bg-red-900/40'
                    : 'bg-emerald-950/30 text-emerald-300 border-emerald-800/40 hover:bg-emerald-900/40'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
          <span className="text-[11px] text-slate-500">
            🔒 Uses only user-provided public attributes. No private API scraping.
          </span>
          <button
            disabled={loading || !formData.username.trim()}
            onClick={() => handleScan()}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 transition cursor-pointer"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Evaluating Signals...</span>
              </>
            ) : (
              <>
                <Zap className="w-4 h-4" />
                <span>Inspect Profile Risk</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="p-4 rounded-xl bg-red-950/50 border border-red-800 text-red-300 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results View */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
          {/* Left: Risk Meter */}
          <div className="lg:col-span-5 space-y-4">
            <RiskMeter
              score={result.risk_score}
              level={result.risk_level}
              status={result.status}
              confidence={0.90}
            />

            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                Recommended Action:
              </span>
              <p className="text-sm font-semibold text-white leading-relaxed">
                {result.recommendation}
              </p>
              <p className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/80">
                {result.disclaimer}
              </p>
            </div>
          </div>

          {/* Right: Detected Signals & Attribution */}
          <div className="lg:col-span-7 space-y-4">
            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Profile Anomaly Findings:
              </h3>

              {result.signals.length === 0 ? (
                <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-800/40 text-xs text-emerald-300">
                  No anomalous metadata, impersonation terms, or fraudulent lures detected.
                </div>
              ) : (
                <div className="space-y-1.5">
                  {result.signals.map((sig, i) => (
                    <div
                      key={i}
                      className="text-xs p-2.5 rounded-xl bg-red-950/30 text-red-200 border border-red-900/40 flex items-center gap-2"
                    >
                      <span className="w-2 h-2 rounded-full bg-red-500"></span>
                      <span>{sig}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Attribution Breakdown */}
            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                Factor Contribution Breakdown:
              </span>
              <div className="space-y-2">
                {result.attributions.map((attr, idx) => (
                  <div key={idx} className="bg-slate-950/40 p-2.5 rounded-xl border border-slate-800/60">
                    <div className="flex justify-between items-center text-xs mb-1">
                      <span className="font-semibold text-slate-200">{attr.factor}</span>
                      <span className="font-mono font-bold text-cyan-400">{attr.percentage}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                        style={{ width: `${attr.percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
