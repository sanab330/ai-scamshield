import React from 'react';
import {
  Shield,
  ShieldAlert,
  Cpu,
  History,
  MessageSquare,
  LayoutDashboard,
  MessageSquareText,
  Link2,
  CreditCard,
  UserX,
  AlertOctagon
} from 'lucide-react';

export default function Navbar({ currentTab, setCurrentTab }) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'message_scanner', label: 'Message Scanner', icon: MessageSquare },
    { id: 'conv_scanner', label: 'Conversation Early Warning', icon: MessageSquareText },
    { id: 'url_scanner', label: 'URL Scanner', icon: Link2 },
    { id: 'payment_shield', label: 'Payment Shield & What-If', icon: CreditCard },
    { id: 'profile_scanner', label: 'Profile Inspector', icon: UserX },
    { id: 'emergency', label: 'Emergency Mode', icon: AlertOctagon, highlight: true },
    { id: 'history', label: 'History', icon: History },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 py-2.5 flex flex-col xl:flex-row items-center justify-between gap-3">
        {/* Brand Logo & Tagline */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('dashboard')}>
          <div className="relative">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 ring-1 ring-white/20">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <span className="absolute -bottom-1 -right-1 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base sm:text-lg tracking-tight text-white">AI ScamShield</span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                PRO
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Think Before You Click. Think Before You Pay.</p>
          </div>
        </div>

        {/* Navigation Tabs - Scrollable on small screens */}
        <nav className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 overflow-x-auto max-w-full">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const active = currentTab === tab.id;

            if (tab.highlight) {
              return (
                <button
                  key={tab.id}
                  onClick={() => setCurrentTab(tab.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition whitespace-nowrap cursor-pointer ${
                    active
                      ? 'bg-red-600 text-white shadow-md shadow-red-500/30 ring-1 ring-red-400'
                      : 'bg-red-950/40 text-red-300 border border-red-800/40 hover:bg-red-900/50'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            }

            return (
              <button
                key={tab.id}
                onClick={() => setCurrentTab(tab.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap cursor-pointer ${
                  active
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-md shadow-blue-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Status indicator */}
        <div className="hidden 2xl:flex items-center gap-2 px-2.5 py-1 rounded-lg bg-emerald-950/40 border border-emerald-800/40 text-emerald-400 text-xs font-mono">
          <Cpu className="w-3.5 h-3.5 animate-pulse" />
          <span>OFFLINE SHIELD ACTIVE</span>
        </div>
      </div>
    </header>
  );
}
