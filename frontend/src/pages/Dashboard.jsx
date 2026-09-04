import React, { useEffect, useState } from 'react';
import {
  Shield,
  ShieldAlert,
  CheckCircle2,
  Clock,
  RefreshCw,
  Zap,
  ArrowUpRight,
  Cpu,
  MessageSquare,
  MessageSquareText,
  Link2,
  CreditCard,
  UserX,
  AlertOctagon
} from 'lucide-react';
import { getDashboardStats } from '../services/api';

export default function Dashboard({ onNavigate }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const total = stats?.total_scans || 0;
  const threats = stats?.threats_detected || 0;
  const safe = stats?.safe_scans || 0;
  const recent = stats?.recent_scans || [];

  const quickModules = [
    { id: 'message_scanner', title: 'AI Message Scanner', desc: 'Scan SMS, WhatsApp, & job offers', icon: MessageSquare, color: 'text-cyan-400', border: 'hover:border-cyan-500/50' },
    { id: 'conv_scanner', title: 'Conversation Early Warning', desc: 'Detect escalating scam dialogue', icon: MessageSquareText, color: 'text-amber-400', border: 'hover:border-amber-500/50' },
    { id: 'url_scanner', title: 'Phishing URL Scanner', desc: 'Inspect typosquatting & links', icon: Link2, color: 'text-blue-400', border: 'hover:border-blue-500/50' },
    { id: 'payment_shield', title: 'Payment Safety Shield', desc: 'Pre-flight checklist & What-If', icon: CreditCard, color: 'text-emerald-400', border: 'hover:border-emerald-500/50' },
    { id: 'profile_scanner', title: 'Profile Inspector', desc: 'Social fake account signals', icon: UserX, color: 'text-purple-400', border: 'hover:border-purple-500/50' },
    { id: 'emergency', title: 'Emergency Mode', desc: 'Crisis containment & helplines', icon: AlertOctagon, color: 'text-red-400', border: 'hover:border-red-500/50' },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Protection Banner */}
      <div className="relative overflow-hidden p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-blue-950/40 to-slate-900 border border-slate-800 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-semibold">
              <Shield className="w-3.5 h-3.5" />
              <span>Real-Time Device Shield Enabled</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Personal Fraud & Phishing Defense
            </h1>
            <p className="text-slate-400 text-sm max-w-xl leading-relaxed">
              Continuous multi-layer offline safety intelligence inspecting SMS, conversations, links, and payments before you interact.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch gap-3 w-full md:w-auto">
            <button
              onClick={() => onNavigate('message_scanner')}
              className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold text-sm shadow-lg shadow-cyan-500/20 transition cursor-pointer"
            >
              <Zap className="w-4 h-4" />
              <span>Scan Message</span>
            </button>
            <button
              onClick={() => onNavigate('emergency')}
              className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-red-950/50 hover:bg-red-900/60 text-red-300 font-semibold text-sm border border-red-800/60 transition cursor-pointer"
            >
              <AlertOctagon className="w-4 h-4" />
              <span>Emergency Mode</span>
            </button>
          </div>
        </div>
      </div>

      {/* Stat Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Total Scans</span>
            <Clock className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-white">{total}</div>
          <p className="text-[11px] text-slate-400 mt-1">Processed locally on-device</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-red-900/30">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Threats Flagged</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-red-400">{threats}</div>
          <p className="text-[11px] text-red-400/80 mt-1">High & critical risk alerts</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-emerald-900/30">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Safe Messages</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold font-mono text-emerald-400">{safe}</div>
          <p className="text-[11px] text-emerald-400/80 mt-1">Normal delivery & chats</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-blue-900/30">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider">Privacy Engine</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-xl font-bold font-mono text-cyan-400">100% OFFLINE</div>
          <p className="text-[11px] text-slate-400 mt-1">Zero cloud data transmission</p>
        </div>
      </div>

      {/* Quick Protection Modules Grid */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Active Safety Shield Modules
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {quickModules.map((mod) => {
            const Icon = mod.icon;
            return (
              <div
                key={mod.id}
                onClick={() => onNavigate(mod.id)}
                className={`p-4 rounded-2xl bg-slate-900/70 border border-slate-800 ${mod.border} transition-all cursor-pointer flex items-center justify-between group hover:bg-slate-900`}
              >
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-xl bg-slate-950 border border-slate-800 ${mod.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition">
                      {mod.title}
                    </h4>
                    <p className="text-xs text-slate-400">{mod.desc}</p>
                  </div>
                </div>
                <ArrowUpRight className="w-4 h-4 text-slate-500 group-hover:text-white transition" />
              </div>
            );
          })}
        </div>
      </div>

      {/* Risk Distribution & Recent Scans Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Breakdown */}
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Risk Tier Distribution
          </h3>
          <div className="space-y-3">
            {[
              { level: 'CRITICAL (76-100)', key: 'CRITICAL', color: 'bg-red-500', count: stats?.distribution?.CRITICAL || 0 },
              { level: 'HIGH RISK (51-75)', key: 'HIGH', color: 'bg-orange-500', count: stats?.distribution?.HIGH || 0 },
              { level: 'CAUTION (26-50)', key: 'MODERATE', color: 'bg-amber-500', count: stats?.distribution?.MODERATE || 0 },
              { level: 'LOW / SAFE (0-25)', key: 'LOW', color: 'bg-emerald-500', count: stats?.distribution?.LOW || 0 },
            ].map((item) => {
              const pct = total > 0 ? Math.round((item.count / total) * 100) : 0;
              return (
                <div key={item.key} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-slate-300">{item.level}</span>
                    <span className="font-mono text-slate-400">{item.count} ({pct}%)</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div className={`h-full ${item.color}`} style={{ width: `${pct}%` }}></div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="pt-3 border-t border-slate-800/80">
            <p className="text-[11px] text-slate-400 leading-normal">
              Scores are calibrated continuously using on-device ML models and deterministic heuristics to minimize false alarms.
            </p>
          </div>
        </div>

        {/* Recent Scans Feed */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Recent Scans Feed
              </h3>
              <button
                onClick={() => onNavigate('history')}
                className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-medium transition cursor-pointer"
              >
                <span>View Full History</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {recent.length === 0 ? (
              <div className="p-8 text-center rounded-xl bg-slate-950/40 border border-slate-800/60">
                <Shield className="w-8 h-8 text-slate-600 mx-auto mb-2" />
                <p className="text-sm text-slate-400 font-medium">No recent scans recorded.</p>
                <p className="text-xs text-slate-500 mt-1">Scan an SMS, conversation, or link to view results here.</p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {recent.map((scan) => {
                  const isHigh = scan.risk_score > 50;
                  return (
                    <div
                      key={scan.id}
                      className="p-3 rounded-xl bg-slate-950/50 border border-slate-800/80 hover:border-slate-700 transition flex items-center justify-between gap-4"
                    >
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                            isHigh
                              ? 'bg-red-950/60 text-red-400 border-red-800/60'
                              : 'bg-emerald-950/60 text-emerald-400 border-emerald-800/60'
                          }`}>
                            {scan.risk_level}
                          </span>
                          <span className="text-[10px] font-mono text-slate-400 uppercase">
                            [{scan.scan_type}]
                          </span>
                          <span className="text-[11px] text-slate-500">
                            {new Date(scan.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300 truncate font-mono">
                          {scan.content_preview}
                        </p>
                      </div>

                      <div className="text-right flex-shrink-0">
                        <div className={`text-base font-extrabold font-mono ${
                          isHigh ? 'text-red-400' : 'text-emerald-400'
                        }`}>
                          {scan.risk_score}/100
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
