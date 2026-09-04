import React, { useState } from 'react';
import { MessageSquareText, AlertTriangle, ShieldAlert, Sparkles, RefreshCw, Zap, TrendingUp, CheckCircle2 } from 'lucide-react';
import RiskMeter from '../components/RiskMeter';
import { scanConversation } from '../services/api';

const CONV_PRESETS = [
  {
    label: 'KYC Suspension Trap',
    type: 'threat',
    text: `Person: Hello, I am calling from HDFC Bank Customer Support.
User: Yes, what is the issue?
Person: Your account will be permanently blocked today due to pending KYC verification.
User: Why will it be blocked? I already updated my details last month.
Person: Regulatory audit found discrepancies. Complete KYC immediately within 30 minutes to avoid penalty.
Person: Click this link to update your documents: http://hdfc-verify.top
Person: Pay a small verification fee of Rs 10 to activate your card.`,
  },
  {
    label: 'Cyber Police Threat Trap',
    type: 'threat',
    text: `Caller: Good morning, this is Inspector Rathore from Crime Branch Delhi.
User: Who? What is this regarding?
Caller: An arrest warrant has been issued against your Aadhaar card for illegal fund transfers.
User: I have never done any illegal transfers!
Caller: You must join a mandatory interrogation video call immediately or police team will reach your residence in 1 hour.
Caller: Deposit Rs 50,000 to the court clearance escrow account to pause immediate arrest.`,
  },
  {
    label: 'Normal Project Discussion',
    type: 'legit',
    text: `Alex: Hey, do you have a few minutes to discuss the new dashboard design?
User: Sure! I reviewed the mockups you shared earlier.
Alex: Great! What do you think about the dark mode theme?
User: I think the contrast looks much better and typography is clean.
Alex: Awesome, I will update the pull request and tag you for final review.`,
  },
];

export default function ConversationScanner() {
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
      const res = await scanConversation(textToScan);
      setResult(res);
    } catch (err) {
      console.error('Conversation scan error:', err);
      setError(err.message || 'Error occurred while analyzing conversation');
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
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
          <MessageSquareText className="w-6 h-6 text-cyan-400" />
          <span>Multi-Turn Scam Conversation Analyzer</span>
        </h2>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Analyzes conversational progression across multiple messages to detect developing fraud escalation <strong>before</strong> you transfer funds.
        </p>
      </div>

      {/* Input Box */}
      <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-4">
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
          Paste Conversation Transcript (Speaker: Message):
        </label>
        <textarea
          rows={7}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={`Paste a multi-turn chat transcript here, for example:\n\nPerson: Hello, I am calling from bank support.\nUser: Why?\nPerson: Your account will be blocked today.\nPerson: Click this link to verify.`}
          className="w-full p-4 rounded-xl bg-slate-950/80 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-sm text-slate-100 placeholder-slate-500 resize-none outline-none font-mono leading-relaxed"
        />

        {/* Presets */}
        <div>
          <span className="text-[11px] uppercase font-semibold text-slate-400 tracking-wider block mb-2">
            Test Scenarios (Click to test early warning engine):
          </span>
          <div className="flex flex-wrap gap-2">
            {CONV_PRESETS.map((preset, idx) => (
              <button
                key={idx}
                onClick={() => handleSelectPreset(preset.text)}
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

        {/* Action Button */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/60">
          <span className="text-[11px] text-slate-500">
            ⚡ Analyzes psychological manipulation, urgency shifts, and payment traps.
          </span>
          <button
            disabled={loading || !text.trim()}
            onClick={() => handleScan()}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 text-white text-sm font-semibold shadow-lg shadow-cyan-500/20 transition cursor-pointer"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Evaluating Dialogue Flow...</span>
              </>
            ) : (
              <>
                <Zap className="w-4 h-4" />
                <span>Analyze Conversation Flow</span>
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
        <div className="space-y-6 animate-fade-in">
          {/* Top Result Row: Risk Meter & Early Warning Banner */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-5">
              <RiskMeter
                score={result.conversation_risk}
                level={result.risk_level}
                status={result.status}
                confidence={0.92}
              />
            </div>

            <div className="lg:col-span-7 flex flex-col justify-between gap-4">
              {/* Early Warning Banner */}
              {result.early_warning_triggered ? (
                <div className="p-5 rounded-2xl bg-amber-950/40 border-2 border-amber-500/60 cyber-glow-amber space-y-2">
                  <div className="flex items-center gap-2 text-amber-400 font-extrabold text-sm uppercase tracking-wider">
                    <AlertTriangle className="w-5 h-5 text-amber-400 animate-bounce" />
                    <span>AI Early Warning Triggered!</span>
                  </div>
                  <p className="text-white font-bold text-sm leading-relaxed">
                    {result.early_warning_message}
                  </p>
                  <p className="text-xs text-amber-200/90 leading-relaxed">
                    The AI detected classic social-engineering manipulation (urgency, authority, and fear) prior to the requester explicitly asking for money or credentials.
                  </p>
                </div>
              ) : (
                <div className="p-5 rounded-2xl bg-emerald-950/30 border border-emerald-800/50 space-y-2">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold text-sm">
                    <CheckCircle2 className="w-5 h-5" />
                    <span>No Coercive Escalation Patterns Detected</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    Dialogue follows natural conversational norms without high-pressure manipulation.
                  </p>
                </div>
              )}

              {/* Recommendation Card */}
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Recommended Safety Action:
                </span>
                <p className="text-sm font-semibold text-white leading-relaxed">
                  {result.recommendation}
                </p>
              </div>

              {/* Detected Stages */}
              {result.escalation_stages.length > 0 && (
                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-2">
                    Identified Social Engineering Stages:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {result.escalation_stages.map((stg, i) => (
                      <span
                        key={i}
                        className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-red-950/40 text-red-300 border border-red-800/40"
                      >
                        {i + 1}. {stg}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Turn-by-Turn Escalation Trajectory */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Turn-by-Turn Risk Progression & Escalation Velocity
                </h3>
              </div>
              <span className="text-xs font-mono text-slate-400">{result.total_turns} Turns Analyzed</span>
            </div>

            <div className="space-y-3">
              {result.turns_analysis.map((turn) => {
                const isHigh = turn.running_risk >= 60;
                const isEarlyWarningTurn = result.early_warning_turn === turn.turn_number;

                return (
                  <div
                    key={turn.turn_number}
                    className={`p-3.5 rounded-xl border transition ${
                      isEarlyWarningTurn
                        ? 'bg-amber-950/30 border-amber-500/70 cyber-glow-amber'
                        : 'bg-slate-950/50 border-slate-800/80'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                          Turn {turn.turn_number}
                        </span>
                        <span className="text-xs font-semibold text-slate-200">{turn.speaker}</span>
                        {isEarlyWarningTurn && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40">
                            ⚠️ Early Trigger Point
                          </span>
                        )}
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-xs text-slate-400">Cumulative Risk:</span>
                        <span className={`text-sm font-extrabold font-mono ${
                          isHigh ? 'text-red-400' : 'text-emerald-400'
                        }`}>
                          {turn.running_risk}/100
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-slate-300 font-mono mb-2">
                      "{turn.text_preview}"
                    </p>

                    {/* Progression Bar */}
                    <div className="w-full bg-slate-800/80 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full ${
                          turn.running_risk >= 70 ? 'bg-red-500' :
                          turn.running_risk >= 40 ? 'bg-amber-500' : 'bg-emerald-500'
                        }`}
                        style={{ width: `${turn.running_risk}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
