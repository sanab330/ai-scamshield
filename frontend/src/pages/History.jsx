import React, { useEffect, useState } from 'react';
import { History as HistoryIcon, Trash2, Shield, AlertTriangle, RefreshCw, CheckCircle2 } from 'lucide-react';
import { getHistory, clearHistory } from '../services/api';

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [clearing, setClearing] = useState(false);
  const [message, setMessage] = useState(null);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleClear = async () => {
    if (!window.confirm('Are you sure you want to purge all local incident records? This cannot be undone.')) {
      return;
    }
    try {
      setClearing(true);
      await clearHistory();
      setHistory([]);
      setMessage('Local history wiped cleanly.');
      setTimeout(() => setMessage(null), 4000);
    } catch (err) {
      console.error('Failed to wipe history:', err);
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-white flex items-center gap-2.5">
            <HistoryIcon className="w-6 h-6 text-cyan-400" />
            <span>Local Incident Log</span>
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Persisted strictly on-device in SQLite. Zero cloud copies exist.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchHistory}
            className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 transition cursor-pointer"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button
            disabled={clearing || history.length === 0}
            onClick={handleClear}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-red-950/40 hover:bg-red-900/50 disabled:opacity-40 text-red-300 text-xs sm:text-sm font-semibold border border-red-800/60 transition cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
            <span>Wipe Local History</span>
          </button>
        </div>
      </div>

      {message && (
        <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs font-medium flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <span>{message}</span>
        </div>
      )}

      {/* History List */}
      {loading ? (
        <div className="p-12 text-center text-slate-500">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-cyan-400" />
          <span>Loading local SQLite records...</span>
        </div>
      ) : history.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-slate-900/40 border border-slate-800/60">
          <Shield className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white">No Incidents Recorded</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Your local database is clean. Any new messages or URLs you scan will be recorded here with masked PII.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {history.map((record) => {
            const isThreat = record.risk_score > 50;
            return (
              <div
                key={record.id}
                className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition space-y-3"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                      isThreat
                        ? 'bg-red-950/60 text-red-300 border-red-800/60'
                        : 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60'
                    }`}>
                      {record.risk_level} RISK
                    </span>
                    <span className="text-xs font-mono text-slate-500">
                      {new Date(record.created_at).toLocaleString()}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-400">Score:</span>
                    <span className={`text-lg font-mono font-extrabold ${
                      isThreat ? 'text-red-400' : 'text-emerald-400'
                    }`}>
                      {record.risk_score}/100
                    </span>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/60">
                  <p className="text-xs font-mono text-slate-300 break-all leading-relaxed">
                    {record.content_preview}
                  </p>
                </div>

                {record.detected_signals && record.detected_signals.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {record.detected_signals.map((sig, idx) => (
                      <span
                        key={idx}
                        className="text-[11px] font-medium px-2 py-0.5 rounded bg-slate-800/80 text-slate-300 border border-slate-700/50"
                      >
                        {sig}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
