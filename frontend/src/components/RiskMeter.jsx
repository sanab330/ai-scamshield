import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, ShieldAlert } from 'lucide-react';

export default function RiskMeter({ score, level, confidence, status }) {
  // Determine color theme based on score
  const getTheme = () => {
    if (score <= 25) {
      return {
        stroke: '#10b981', // Emerald
        bg: 'bg-emerald-500/10',
        text: 'text-emerald-400',
        border: 'border-emerald-500/30',
        badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40',
        icon: ShieldCheck,
        glow: 'cyber-glow-emerald',
      };
    } else if (score <= 50) {
      return {
        stroke: '#f59e0b', // Amber
        bg: 'bg-amber-500/10',
        text: 'text-amber-400',
        border: 'border-amber-500/30',
        badgeBg: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
        icon: AlertTriangle,
        glow: 'cyber-glow-amber',
      };
    } else if (score <= 75) {
      return {
        stroke: '#f97316', // Orange
        bg: 'bg-orange-500/10',
        text: 'text-orange-400',
        border: 'border-orange-500/30',
        badgeBg: 'bg-orange-500/20 text-orange-300 border-orange-500/40',
        icon: AlertOctagon,
        glow: 'cyber-glow-amber',
      };
    } else {
      return {
        stroke: '#ef4444', // Red
        bg: 'bg-red-500/10',
        text: 'text-red-400',
        border: 'border-red-500/30',
        badgeBg: 'bg-red-500/20 text-red-300 border-red-500/40',
        icon: ShieldAlert,
        glow: 'cyber-glow-red',
      };
    }
  };

  const theme = getTheme();
  const Icon = theme.icon;

  // SVG circular gauge calculation
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className={`p-6 rounded-2xl bg-slate-900/90 border ${theme.border} ${theme.glow} flex flex-col items-center justify-center relative overflow-hidden transition-all duration-300`}>
      {/* Background ambient glow */}
      <div className={`absolute -top-12 -right-12 w-36 h-36 rounded-full blur-3xl opacity-20 ${theme.bg}`}></div>
      
      {/* Risk Gauge Header */}
      <div className="flex items-center justify-between w-full mb-3">
        <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">Risk Assessment</span>
        <div className="flex items-center gap-1 text-[11px] text-slate-400 bg-slate-800/60 px-2 py-0.5 rounded-full border border-slate-700/50">
          <span>Confidence:</span>
          <span className="font-mono text-slate-200 font-semibold">{Math.round((confidence || 0.9) * 100)}%</span>
        </div>
      </div>

      {/* SVG Circle Gauge */}
      <div className="relative w-36 h-36 flex items-center justify-center my-2">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
          <circle
            cx="64"
            cy="64"
            r={radius}
            stroke="#1e293b"
            strokeWidth="10"
            fill="transparent"
          />
          <circle
            cx="64"
            cy="64"
            r={radius}
            stroke={theme.stroke}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Score Readout */}
        <div className="absolute flex flex-col items-center justify-center">
          <div className="flex items-baseline">
            <span className={`text-4xl font-extrabold font-mono tracking-tight ${theme.text}`}>
              {score}
            </span>
            <span className="text-xs text-slate-500 font-mono ml-0.5">/100</span>
          </div>
          <span className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">
            Risk Score
          </span>
        </div>
      </div>

      {/* Status Pill */}
      <div className={`mt-3 px-3.5 py-1.5 rounded-full border text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${theme.badgeBg}`}>
        <Icon className="w-3.5 h-3.5" />
        <span>{status || `${level} RISK`}</span>
      </div>
    </div>
  );
}
