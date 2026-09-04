import React, { useState, useEffect } from 'react';
import { ShieldCheck, ShieldAlert, Sliders, CheckSquare, AlertOctagon, HelpCircle, ArrowRight, Zap, RefreshCw } from 'lucide-react';
import RiskMeter from '../components/RiskMeter';
import { scanPayment } from '../services/api';

export default function PaymentProtection() {
  const [subTab, setSubTab] = useState('checklist'); // 'checklist' | 'simulator'

  // Checklist State
  const [amount, setAmount] = useState('15000');
  const [isNewRecipient, setIsNewRecipient] = useState(true);
  const [checklist, setChecklist] = useState({
    know_recipient: false,
    user_initiated: false,
    act_urgently: true,
    share_otp_pin: false,
    unexpected_contact: true,
    suspicious_link: false,
    unrealistic_reward: false,
  });
  const [checklistResult, setChecklistResult] = useState(null);
  const [checklistLoading, setChecklistLoading] = useState(false);

  // What-If Simulator State
  const [simAmount, setSimAmount] = useState(35000);
  const [simIsNew, setSimIsNew] = useState(true);
  const [simHour, setSimHour] = useState(2); // 2 AM
  const [simUrgency, setSimUrgency] = useState(true);
  const [simDeviceChanged, setSimDeviceChanged] = useState(false);
  const [simResult, setSimResult] = useState(null);

  // Evaluate Checklist
  const evaluateChecklist = async () => {
    try {
      setChecklistLoading(true);
      const res = await scanPayment({
        amount: parseFloat(amount) || 0,
        is_new_recipient: isNewRecipient,
        recipient_history_count: isNewRecipient ? 0 : 5,
        transaction_hour: new Date().getHours(),
        has_urgency_pressure: checklist.act_urgently,
        checklist_answers: checklist,
      });
      setChecklistResult(res);
    } catch (err) {
      console.error('Checklist eval error:', err);
    } finally {
      setChecklistLoading(false);
    }
  };

  // Run initial checklist evaluation
  useEffect(() => {
    evaluateChecklist();
  }, []);

  // Evaluate What-If Simulator dynamically on slider change
  useEffect(() => {
    const runSim = async () => {
      try {
        const res = await scanPayment({
          amount: simAmount,
          is_new_recipient: simIsNew,
          recipient_history_count: simIsNew ? 0 : 12,
          transaction_hour: simHour,
          has_urgency_pressure: simUrgency,
          is_device_changed: simDeviceChanged,
        });
        setSimResult(res);
      } catch (err) {
        console.error('Sim error:', err);
      }
    };
    runSim();
  }, [simAmount, simIsNew, simHour, simUrgency, simDeviceChanged]);

  const toggleChecklist = (key) => {
    setChecklist((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
            <ShieldAlert className="w-6 h-6 text-cyan-400" />
            <span>Payment Safety & Risk Shield</span>
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Evaluate payment safety before you transfer money. <strong>Never enter UPI PINs or OTPs here.</strong>
          </p>
        </div>

        {/* Sub-Tab Switcher */}
        <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
          <button
            onClick={() => setSubTab('checklist')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              subTab === 'checklist'
                ? 'bg-blue-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <CheckSquare className="w-3.5 h-3.5" />
            <span>Stop Before You Pay</span>
          </button>
          <button
            onClick={() => setSubTab('simulator')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              subTab === 'simulator'
                ? 'bg-blue-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" />
            <span>"What-If?" Simulator</span>
          </button>
        </div>
      </div>

      {/* VIEW 1: STOP BEFORE YOU PAY CHECKLIST */}
      {subTab === 'checklist' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
          {/* Left: 7-Point Checklist Form */}
          <div className="lg:col-span-7 space-y-4">
            <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold uppercase tracking-wider text-white flex items-center gap-2">
                <CheckSquare className="w-4 h-4 text-cyan-400" />
                <span>Pre-Flight Payment Checklist</span>
              </h3>

              {/* Transaction Amount & Recipient */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pb-3 border-b border-slate-800">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    Amount (₹ INR):
                  </label>
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm font-mono text-white outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    Recipient Relationship:
                  </label>
                  <select
                    value={isNewRecipient ? 'new' : 'known'}
                    onChange={(e) => setIsNewRecipient(e.target.value === 'new')}
                    className="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white outline-none focus:border-cyan-500"
                  >
                    <option value="new">Brand-New Recipient (First time)</option>
                    <option value="known">Known Recipient (Transferred before)</option>
                  </select>
                </div>
              </div>

              {/* 7 Verification Questions */}
              <div className="space-y-2.5">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400 block mb-1">
                  Answer Honestly Before Proceeding:
                </span>

                {[
                  { key: 'know_recipient', question: '1. Do you personally know the recipient in real life?', invert: true },
                  { key: 'user_initiated', question: '2. Did YOU initiate this payment independently?', invert: true },
                  { key: 'act_urgently', question: '3. Were you asked to act urgently within minutes?' },
                  { key: 'share_otp_pin', question: '4. Were you asked to enter/share OTP or PIN to receive money?' },
                  { key: 'unexpected_contact', question: '5. Did someone contact you unexpectedly via call/SMS?' },
                  { key: 'suspicious_link', question: '6. Were you sent an external link to complete payment?' },
                  { key: 'unrealistic_reward', question: '7. Are you promised an unrealistic prize or investment return?' },
                ].map((item) => {
                  const isChecked = checklist[item.key];
                  const isRisky = item.invert ? !isChecked : isChecked;

                  return (
                    <div
                      key={item.key}
                      onClick={() => toggleChecklist(item.key)}
                      className={`p-3 rounded-xl border transition cursor-pointer flex items-center justify-between gap-3 ${
                        isRisky
                          ? 'bg-red-950/20 border-red-800/40 hover:bg-red-950/30'
                          : 'bg-slate-950/40 border-slate-800/80 hover:bg-slate-950/70'
                      }`}
                    >
                      <span className="text-xs text-slate-200 font-medium">{item.question}</span>
                      <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                        isChecked
                          ? 'bg-blue-600/30 text-blue-300 border-blue-500/40'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                        {isChecked ? 'YES' : 'NO'}
                      </span>
                    </div>
                  );
                })}
              </div>

              <button
                onClick={evaluateChecklist}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-semibold text-sm shadow-lg shadow-cyan-500/20 transition cursor-pointer"
              >
                {checklistLoading ? 'Recalculating Risk...' : 'Update Risk Assessment'}
              </button>
            </div>
          </div>

          {/* Right: Checklist Assessment Result */}
          <div className="lg:col-span-5 space-y-4">
            {checklistResult && (
              <>
                <RiskMeter
                  score={checklistResult.risk_score}
                  level={checklistResult.risk_level}
                  status={checklistResult.status}
                  confidence={0.95}
                />

                <div className={`p-5 rounded-2xl border ${
                  checklistResult.risk_score > 50
                    ? 'bg-red-950/30 border-red-800/50'
                    : 'bg-emerald-950/30 border-emerald-800/50'
                } space-y-2`}>
                  <div className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                    <AlertOctagon className="w-4 h-4 text-red-400" />
                    <span>Stop Before You Pay Advisory:</span>
                  </div>
                  <p className="text-sm font-semibold text-white leading-relaxed">
                    {checklistResult.recommendation}
                  </p>
                </div>

                {checklistResult.signals && checklistResult.signals.length > 0 && (
                  <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                      Active Payment Risk Drivers:
                    </span>
                    <div className="space-y-1">
                      {checklistResult.signals.map((sig, i) => (
                        <div key={i} className="text-xs text-red-300 bg-red-950/30 px-2.5 py-1 rounded border border-red-900/40">
                          • {sig}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}

      {/* VIEW 2: "WHAT-IF?" INTERACTIVE RISK SIMULATOR */}
      {subTab === 'simulator' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
          {/* Controls Column */}
          <div className="lg:col-span-7 space-y-5 p-6 rounded-2xl bg-slate-900/90 border border-slate-800">
            <div>
              <h3 className="text-sm font-bold uppercase tracking-wider text-white flex items-center gap-2">
                <Sliders className="w-4 h-4 text-cyan-400" />
                <span>"What If?" Dynamic Scenario Simulator</span>
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Drag the sliders to see how individual behavioral factors dynamically alter your fraud exposure score in real-time.
              </p>
            </div>

            {/* Slider 1: Amount */}
            <div className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-300">Transaction Amount</span>
                <span className="font-mono font-bold text-cyan-400 text-sm">₹{simAmount.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min="500"
                max="150000"
                step="2500"
                value={simAmount}
                onChange={(e) => setSimAmount(parseInt(e.target.value))}
                className="w-full accent-cyan-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                <span>₹500 (Low)</span>
                <span>₹75,000 (Medium)</span>
                <span>₹1,50,000 (High)</span>
              </div>
            </div>

            {/* Slider 2: Time of Day */}
            <div className="space-y-2 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-300">Transaction Hour</span>
                <span className="font-mono font-bold text-cyan-400 text-sm">
                  {simHour}:00 {simHour >= 12 ? 'PM' : 'AM'} {simHour >= 1 && simHour <= 5 ? '(⚠️ Unusual Late Night)' : ''}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="23"
                value={simHour}
                onChange={(e) => setSimHour(parseInt(e.target.value))}
                className="w-full accent-cyan-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                <span>12 AM (Midnight)</span>
                <span>12 PM (Noon)</span>
                <span>11 PM (Night)</span>
              </div>
            </div>

            {/* Toggles */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div
                onClick={() => setSimIsNew(!simIsNew)}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  simIsNew ? 'bg-red-950/20 border-red-800/50' : 'bg-slate-950/60 border-slate-800'
                }`}
              >
                <span className="text-xs font-medium text-slate-200">New Recipient</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  simIsNew ? 'bg-red-500/20 text-red-300' : 'bg-slate-800 text-slate-400'
                }`}>
                  {simIsNew ? 'YES' : 'NO'}
                </span>
              </div>

              <div
                onClick={() => setSimUrgency(!simUrgency)}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  simUrgency ? 'bg-red-950/20 border-red-800/50' : 'bg-slate-950/60 border-slate-800'
                }`}
              >
                <span className="text-xs font-medium text-slate-200">Urgency Pressure</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  simUrgency ? 'bg-red-500/20 text-red-300' : 'bg-slate-800 text-slate-400'
                }`}>
                  {simUrgency ? 'YES' : 'NO'}
                </span>
              </div>
            </div>
          </div>

          {/* Simulator Live Feedback Gauge */}
          <div className="lg:col-span-5 space-y-4">
            {simResult && (
              <>
                <RiskMeter
                  score={simResult.risk_score}
                  level={simResult.risk_level}
                  status={simResult.status}
                  confidence={0.95}
                />

                {/* Factor Contribution Bars */}
                <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                    Dynamic Factor Attribution:
                  </span>
                  <div className="space-y-2">
                    {simResult.attributions.map((attr, i) => (
                      <div key={i} className="bg-slate-950/50 p-2 rounded-lg border border-slate-800/60">
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-slate-300 font-medium">{attr.factor}</span>
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
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
