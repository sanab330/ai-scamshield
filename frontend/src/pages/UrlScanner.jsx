import React, { useState } from 'react';
import { Link2, Shield, AlertTriangle, ExternalLink, Globe, Lock, Unlock, RefreshCw, Zap } from 'lucide-react';
import RiskMeter from '../components/RiskMeter';
import { scanUrl } from '../services/api';

const URL_PRESETS = [
  {
    label: 'SBI Bank Phishing (.xyz)',
    type: 'threat',
    url: 'http://sbi-kyc-verification.xyz/login.php?verify=1',
  },
  {
    label: 'PayPal Typosquatting (paypa1)',
    type: 'threat',
    url: 'http://paypa1-security-check.top/update',
  },
  {
    label: 'IP Host + Malicious APK',
    type: 'threat',
    url: 'http://192.168.1.55/bank/verify-update.apk',
  },
  {
    label: 'Safe: Amazon Store',
    type: 'legit',
    url: 'https://www.amazon.in/gp/goldbox',
  },
  {
    label: 'Safe: Google Search',
    type: 'legit',
    url: 'https://www.google.com/search?q=cybersecurity',
  },
];

export default function UrlScanner() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (overrideUrl) => {
    const urlToScan = overrideUrl !== undefined ? overrideUrl : url;
    if (!urlToScan.trim()) return;

    try {
      setLoading(true);
      setError(null);
      const res = await scanUrl(urlToScan);
      setResult(res);
    } catch (err) {
      console.error('URL scan error:', err);
      setError(err.message || 'Error occurred while analyzing URL');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPreset = (presetUrl) => {
    setUrl(presetUrl);
    handleScan(presetUrl);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
          <Link2 className="w-6 h-6 text-cyan-400" />
          <span>Structural URL & Phishing Link Scanner</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Inspects web links completely offline for brand typosquatting, suspicious TLDs, punycode, direct IP addresses, and malicious download payloads.
        </p>
      </div>

      {/* Input Box */}
      <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
          Enter or Paste URL:
        </label>
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="e.g. http://sbi-kyc-verification.xyz/login"
            className="flex-1 p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-sm text-slate-100 placeholder-slate-500 outline-none font-mono"
          />
          <button
            disabled={loading || !url.trim()}
            onClick={() => handleScan()}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 transition cursor-pointer"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Inspecting...</span>
              </>
            ) : (
              <>
                <Zap className="w-4 h-4" />
                <span>Inspect URL</span>
              </>
            )}
          </button>
        </div>

        {/* Quick Presets */}
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
            Quick Test URLs (Click to analyze):
          </span>
          <div className="flex flex-wrap gap-2">
            {URL_PRESETS.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectPreset(preset.url)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition cursor-pointer ${
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
          {/* Left: Risk Gauge & Recommendation */}
          <div className="lg:col-span-5 space-y-4">
            <RiskMeter
              score={result.risk_score}
              level={result.risk_level}
              status={result.status}
              confidence={result.confidence}
            />

            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                Recommended Action:
              </span>
              <p className="text-sm font-semibold text-white leading-relaxed">
                {result.recommendation}
              </p>
              <p className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/80">
                AI ScamShield performs offline structural decomposition. No external DNS or cloud lookups leak your browsing target.
              </p>
            </div>
          </div>

          {/* Right: Structural Findings & Signal Attribution */}
          <div className="lg:col-span-7 space-y-4">
            {/* Structural Parameters Card */}
            <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Globe className="w-4 h-4 text-cyan-400" />
                <span>Structural Security Inspection</span>
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800/80 flex items-center gap-2.5">
                  {result.is_https ? (
                    <Lock className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <Unlock className="w-4 h-4 text-red-400" />
                  )}
                  <div>
                    <div className="text-[11px] text-slate-400">Protocol</div>
                    <div className="text-xs font-mono font-bold text-white">
                      {result.is_https ? 'HTTPS Encrypted' : 'Insecure HTTP'}
                    </div>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/50 border border-slate-800/80 flex items-center gap-2.5">
                  <Globe className="w-4 h-4 text-cyan-400" />
                  <div>
                    <div className="text-[11px] text-slate-400">Target Hostname</div>
                    <div className="text-xs font-mono font-bold text-white truncate max-w-[180px]">
                      {result.hostname}
                    </div>
                  </div>
                </div>
              </div>

              {result.impersonated_brand && (
                <div className="p-3 rounded-xl bg-red-950/40 border border-red-800/50 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
                  <span className="text-xs font-semibold text-red-300">
                    Target Brand Impersonation Flagged: <strong>{result.impersonated_brand}</strong>
                  </span>
                </div>
              )}

              {/* Detected Structural Signals */}
              {result.signals && result.signals.length > 0 && (
                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                    Observed Structural Threat Indicators:
                  </span>
                  <div className="space-y-1.5">
                    {result.signals.map((sig, i) => (
                      <div
                        key={i}
                        className="text-xs p-2 rounded-lg bg-red-950/30 text-red-200 border border-red-900/40 flex items-center gap-2"
                      >
                        <span className="w-1.5 h-1.5 rounded-full bg-red-400"></span>
                        <span>{sig}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Attribution Progress Bars */}
            {result.attribution && result.attribution.length > 0 && (
              <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
                  Risk Attribution Breakdown:
                </span>
                <div className="space-y-2.5">
                  {result.attribution.map((attr, idx) => (
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
            )}
          </div>
        </div>
      )}
    </div>
  );
}
