import React from 'react';
import { AlertOctagon, PhoneCall, ShieldAlert, FileText, Lock, ExternalLink, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function EmergencyMode() {
  const steps = [
    {
      num: '1',
      title: 'Stop Communicating Immediately',
      desc: 'Hang up the call or block the sender on WhatsApp, Telegram, and SMS. Do not engage in further arguments or negotiations.',
      urgent: true,
    },
    {
      num: '2',
      title: 'Do Not Send Any More Money',
      desc: 'Never pay "cancellation fees", "tax deposits", or "refund activation fees" to get previously lost money back. These are secondary recovery scams.',
      urgent: true,
    },
    {
      num: '3',
      title: 'Never Share Any OTP or Banking PIN',
      desc: 'If anyone asks for a 6-digit code or tells you to enter your UPI PIN to "receive money", decline immediately. Money is received without entering a PIN.',
      urgent: true,
    },
    {
      num: '4',
      title: 'Call Your Bank Emergency Fraud Desk',
      desc: 'Contact your bank immediately to block your debit/credit card and freeze the affected account. Use official numbers from the back of your card, not from Google search ads.',
    },
    {
      num: '5',
      title: 'Preserve All Digital Evidence',
      desc: 'Take screenshots of the chat messages, transaction UTR numbers, caller phone numbers, and web links before they are deleted by the scammer.',
    },
    {
      num: '6',
      title: 'File an Official Cybercrime Complaint',
      desc: 'Report the incident immediately on official national portals so law enforcement can coordinate with financial intermediaries to freeze stolen funds.',
    },
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-fade-in">
      {/* Emergency Crisis Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-red-950/80 via-red-900/30 to-slate-950 border-2 border-red-500/80 shadow-2xl cyber-glow-red space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-red-600 flex items-center justify-center text-white shadow-lg shadow-red-500/30 animate-pulse">
            <AlertOctagon className="w-7 h-7" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-red-300">
              Crisis Containment Protocol
            </span>
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
              "I Think I'm Being Scammed"
            </h1>
          </div>
        </div>
        <p className="text-sm text-red-100/90 leading-relaxed font-medium">
          Take a deep breath. Scammers rely on manufactured panic to force rapid mistakes. Follow these 6 containment steps immediately to secure your finances.
        </p>
      </div>

      {/* 6 Containment Steps */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">
          Immediate Action Checklist:
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {steps.map((step) => (
            <div
              key={step.num}
              className={`p-4 rounded-2xl border ${
                step.urgent
                  ? 'bg-red-950/20 border-red-800/40'
                  : 'bg-slate-900/80 border-slate-800'
              } space-y-1.5`}
            >
              <div className="flex items-center gap-2.5">
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-mono ${
                  step.urgent ? 'bg-red-500 text-white' : 'bg-slate-800 text-slate-300'
                }`}>
                  {step.num}
                </span>
                <h4 className="text-sm font-bold text-white">{step.title}</h4>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed pl-8">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Official Government Cybercrime Helplines */}
      <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
        <h3 className="text-sm font-bold uppercase tracking-wider text-white flex items-center gap-2">
          <PhoneCall className="w-4 h-4 text-cyan-400" />
          <span>Official National Cybercrime Helplines</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {/* India Helpline */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-slate-300">India: National Cyber Crime</span>
              <span className="text-xs font-mono font-extrabold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/60">
                1930
              </span>
            </div>
            <p className="text-xs text-slate-400">
              National Cyber Financial Fraud Reporting Helpline. Call within the "Golden Hour" to freeze fund transfers.
            </p>
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              <span>cybercrime.gov.in</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          {/* RBI Helpline */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-slate-300">RBI Banking Ombudsman</span>
              <span className="text-xs font-mono font-extrabold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/60">
                14448
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Reserve Bank of India banking complaint helpline for unauthorized financial transactions.
            </p>
            <a
              href="https://cms.rbi.org.in"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              <span>cms.rbi.org.in</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
