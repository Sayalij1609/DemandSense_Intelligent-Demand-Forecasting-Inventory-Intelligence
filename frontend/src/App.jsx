import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Boxes,
  Cpu,
  Database,
  BarChart3,
  Layers,
  ShieldCheck,
  Zap,
  Terminal,
  Server,
  FolderGit2,
  ExternalLink,
} from 'lucide-react';
import HealthBadge from './components/HealthBadge';
import { fetchHealthStatus } from './services/api';

const INVENTORY_DECISION_PILLARS = [
  {
    title: 'Expected Demand',
    desc: 'Point forecasts with trend and cyclical decomposition across SKUs and distribution centers.',
    icon: TrendingUp,
    badge: 'Forecast Core',
  },
  {
    title: 'Forecast Uncertainty',
    desc: 'Calibrated probabilistic prediction intervals (p10, p50, p90) quantifying variance.',
    icon: BarChart3,
    badge: 'Quantile / Bayesian',
  },
  {
    title: 'Safety Stock & ROP',
    desc: 'Dynamic safety buffer and reorder point calculation factoring supplier lead-time variability.',
    icon: Boxes,
    badge: 'Inventory Logic',
  },
  {
    title: 'Risk Minimization',
    desc: 'Proactive stockout risk and overstock holding cost mitigation using asymmetric loss.',
    icon: ShieldCheck,
    badge: 'Cost Optimization',
  },
];

const DIRECTORY_MAPPING = [
  { path: 'backend/', desc: 'FastAPI REST service, SQLAlchemy ORM, Pydantic schemas, and API v1 endpoints.' },
  { path: 'frontend/', desc: 'React 18 + Vite + Tailwind CSS dashboard with interactive decision visualizers.' },
  { path: 'ml/', desc: 'Feature engineering, time-series forecasting models, and inventory intelligence engine.' },
  { path: 'data/', desc: 'Raw ingestion, processed parquet/csv datasets, and pipeline artifacts.' },
  { path: 'docker/', desc: 'Multi-stage Dockerfiles and PostgreSQL init scripts for local and cloud deploys.' },
  { path: 'docs/', desc: 'System architecture, API specifications, and developer workflow guidelines.' },
  { path: 'tests/', desc: 'Pytest suite for verification of architecture, API contracts, and ML logic.' },
];

export default function App() {
  const [healthData, setHealthData] = useState(null);
  const [loadingHealth, setLoadingHealth] = useState(false);
  const [healthError, setHealthError] = useState(null);

  const loadHealth = async () => {
    setLoadingHealth(true);
    setHealthError(null);
    const { data, error } = await fetchHealthStatus();
    if (error) {
      setHealthError(error);
      setHealthData(null);
    } else {
      setHealthData(data);
      setHealthError(null);
    }
    setLoadingHealth(false);
  };

  useEffect(() => {
    loadHealth();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100 flex flex-col">
      {/* Top Navbar */}
      <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold shadow-lg shadow-emerald-500/10">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <div className="font-extrabold text-base tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
                DemandSense
              </div>
              <div className="text-[10px] text-slate-400 font-mono tracking-wider">
                FOUNDATION PHASE v0.1.0
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <HealthBadge
              health={healthData}
              loading={loadingHealth}
              onRefresh={loadHealth}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full space-y-10">
        {/* Hero Section */}
        <section className="text-center space-y-4 max-w-3xl mx-auto pt-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Production Foundation Initialized
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Intelligent Demand Forecasting &{' '}
            <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              Inventory Intelligence
            </span>
          </h1>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            DemandSense transforms raw historical time series and promotional signals into probabilistic demand forecasts and automated inventory replenishment decisions.
          </p>
        </section>

        {/* Live Diagnostics Card */}
        <section className="glass-card rounded-2xl p-6 border border-slate-800 shadow-xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl -z-10"></div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
                <Server className="w-4 h-4 text-emerald-400" />
                Backend Connection Live Check
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Real-time handshake with the FastAPI microservice (<code className="text-emerald-300">/api/v1/health</code>)
              </p>
            </div>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-400 hover:text-emerald-300 transition-colors bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20 hover:bg-emerald-500/20"
            >
              Open API Swagger Docs <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>

          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Service Name</span>
              <div className="text-sm font-semibold text-slate-200 mt-1">
                {healthData?.app_name || 'DemandSense API'}
              </div>
            </div>
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Environment & Version</span>
              <div className="text-sm font-semibold text-slate-200 mt-1">
                {healthData ? `${healthData.environment} (v${healthData.version})` : 'Connecting...'}
              </div>
            </div>
            <div className="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Reported Timestamp</span>
              <div className="text-xs font-mono text-emerald-400/90 mt-1 truncate">
                {healthData?.timestamp ? new Date(healthData.timestamp).toUTCString() : (healthError || 'Awaiting API response...')}
              </div>
            </div>
          </div>
        </section>

        {/* Inventory Intelligence Pillars */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-200 flex items-center gap-2">
              <Boxes className="w-5 h-5 text-emerald-400" />
              Core Capabilities in Roadmap
            </h2>
            <span className="text-xs text-slate-400 font-mono">Phase 1 Foundations Active</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {INVENTORY_DECISION_PILLARS.map((pillar, idx) => {
              const Icon = pillar.icon;
              return (
                <div
                  key={idx}
                  className="glass-card glass-card-hover rounded-xl p-5 border border-slate-800 flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="w-9 h-9 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="text-[10px] font-semibold font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                        {pillar.badge}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-slate-100">{pillar.title}</h3>
                    <p className="text-xs text-slate-400 leading-relaxed">{pillar.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Clean Modular Architecture Directory Overview */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-200 flex items-center gap-2">
              <FolderGit2 className="w-5 h-5 text-emerald-400" />
              Modular Directory Breakdown
            </h2>
            <span className="text-xs text-slate-400 font-mono">7 Clean Modules</span>
          </div>

          <div className="glass-card rounded-2xl border border-slate-800 divide-y divide-slate-800/80 overflow-hidden">
            {DIRECTORY_MAPPING.map((item, idx) => (
              <div key={idx} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2 hover:bg-slate-900/40 transition-colors">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded border border-emerald-500/20">
                    {item.path}
                  </span>
                  <span className="text-xs text-slate-300">{item.desc}</span>
                </div>
                <span className="text-[10px] font-mono text-slate-500 uppercase">Independent module</span>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-6 bg-slate-950 text-center text-xs text-slate-500">
        DemandSense — Intelligent Demand Forecasting & Inventory Intelligence &copy; 2026
      </footer>
    </div>
  );
}
