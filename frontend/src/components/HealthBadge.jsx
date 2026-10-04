import React from 'react';
import { Activity, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export default function HealthBadge({ health, loading, onRefresh }) {
  const isHealthy = health && health.status === 'healthy';

  return (
    <div className="flex flex-wrap items-center gap-3 p-3 rounded-xl bg-slate-900/80 border border-slate-800">
      <div className="flex items-center gap-2">
        <span className="relative flex h-3 w-3">
          {isHealthy ? (
            <>
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </>
          ) : (
            <>
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
            </>
          )}
        </span>
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          FastAPI Status:
        </span>
        <span
          className={`text-xs font-bold px-2 py-0.5 rounded-full ${
            isHealthy
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
          }`}
        >
          {loading ? 'Checking...' : isHealthy ? 'HEALTHY' : 'CONNECTING'}
        </span>
      </div>

      {health && (
        <div className="hidden sm:flex items-center gap-3 text-xs text-slate-400 border-l border-slate-800 pl-3">
          <span>
            Env: <strong className="text-slate-200">{health.environment}</strong>
          </span>
          <span>
            v<strong className="text-slate-200">{health.version}</strong>
          </span>
        </div>
      )}

      <button
        onClick={onRefresh}
        disabled={loading}
        title="Refresh backend status"
        className="ml-auto inline-flex items-center gap-1 text-xs text-slate-400 hover:text-emerald-400 transition-colors p-1.5 rounded-lg hover:bg-slate-800/80"
      >
        <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-emerald-400' : ''}`} />
        <span className="hidden md:inline">Sync</span>
      </button>
    </div>
  );
}
