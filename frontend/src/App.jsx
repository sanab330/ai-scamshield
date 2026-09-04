import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import MessageScanner from './pages/MessageScanner';
import ConversationScanner from './pages/ConversationScanner';
import UrlScanner from './pages/UrlScanner';
import PaymentProtection from './pages/PaymentProtection';
import ProfileScanner from './pages/ProfileScanner';
import EmergencyMode from './pages/EmergencyMode';
import History from './pages/History';
import { Shield, Lock, EyeOff } from 'lucide-react';

export default function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-black">
      {/* Top Shield Header */}
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">
        {currentTab === 'dashboard' && <Dashboard onNavigate={setCurrentTab} />}
        {currentTab === 'message_scanner' && <MessageScanner />}
        {currentTab === 'conv_scanner' && <ConversationScanner />}
        {currentTab === 'url_scanner' && <UrlScanner />}
        {currentTab === 'payment_shield' && <PaymentProtection />}
        {currentTab === 'profile_scanner' && <ProfileScanner />}
        {currentTab === 'emergency' && <EmergencyMode />}
        {currentTab === 'history' && <History />}
      </main>

      {/* Cyber Defense Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            <span className="font-semibold text-slate-300">AI ScamShield</span>
            <span>— Privacy-First Offline Edge Safety Shield</span>
          </div>

          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1.5 text-slate-400">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Zero Credential Requests</span>
            </span>
            <span className="flex items-center gap-1.5 text-slate-400">
              <EyeOff className="w-3.5 h-3.5 text-cyan-400" />
              <span>100% On-Device Data Sovereignty</span>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
