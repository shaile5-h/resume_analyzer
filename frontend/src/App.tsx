import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { FileUpload } from './components/FileUpload';
import { resumeApi } from './services/api';
import { BulletRewriteResponse, ResumeUploadResponse } from './types';
import {
  CheckCircle2,
  Terminal,
  Cpu,
  Database,
  Layers,
  ArrowRight,
  Sparkles,
  RefreshCw,
  Copy,
  Check,
  FileText
} from 'lucide-react';

export const App: React.FC = () => {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [healthData, setHealthData] = useState<any>(null);
  const [uploadedResume, setUploadedResume] = useState<ResumeUploadResponse | null>(null);
  
  // Interactive Copilot Test State
  const [sampleBullet, setSampleBullet] = useState('worked on python apis and fixed bugs for user login');
  const [isRewriting, setIsRewriting] = useState(false);
  const [rewriteResult, setRewriteResult] = useState<BulletRewriteResponse | null>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const checkServerHealth = async () => {
    setBackendStatus('checking');
    try {
      const data = await resumeApi.checkHealth();
      setHealthData(data);
      setBackendStatus('online');
    } catch (err) {
      console.warn('Backend currently unreachable', err);
      setBackendStatus('offline');
    }
  };

  useEffect(() => {
    checkServerHealth();
    const interval = setInterval(checkServerHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleTestRewrite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sampleBullet.trim()) return;
    setIsRewriting(true);
    try {
      const res = await resumeApi.rewriteBullet(sampleBullet, 'Full Stack Engineer');
      setRewriteResult(res);
    } catch (err) {
      console.error('Failed to rewrite bullet', err);
    } finally {
      setIsRewriting(false);
    }
  };

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-['Plus_Jakarta_Sans',sans-serif]">
      <Navbar backendStatus={backendStatus} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold mb-4 shadow-sm">
            <span className="flex h-2 w-2 rounded-full bg-emerald-600 animate-pulse"></span>
            <span>Stage 2 Completed: Resume Ingestion & Deterministic ATS Audit</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            AI-Powered Resume Analyzer <br />
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 bg-clip-text text-transparent">
              & Career Copilot
            </span>
          </h1>
          <p className="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed">
            Enterprise-grade ATS compliance auditing, semantic job-description matching, and high-impact resume enhancement built with FastAPI, SQLite WAL mode, and React.js.
          </p>
        </div>

        {/* System Architecture Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-1">FastAPI Backend</h3>
            <p className="text-sm text-slate-600 mb-3">
              Asynchronous Python 3.11+ REST API running via <code className="text-indigo-600 font-mono text-xs bg-slate-100 px-1 py-0.5 rounded">python server.py</code>.
            </p>
            <div className="flex items-center text-xs font-medium text-emerald-600">
              <CheckCircle2 className="w-4 h-4 mr-1" />
              Swagger UI ready at :8000/docs
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-1">SQLite WAL Storage</h3>
            <p className="text-sm text-slate-600 mb-3">
              Zero-latency relational database with Write-Ahead Logging for non-blocking concurrent writes and SHA-256 caching.
            </p>
            <div className="flex items-center text-xs font-medium text-emerald-600">
              <CheckCircle2 className="w-4 h-4 mr-1" />
              Models & Pragmas Configured
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center mb-4">
              <Layers className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-1">React + Vite UI</h3>
            <p className="text-sm text-slate-600 mb-3">
              Modern frontend powered by Tailwind CSS, TypeScript, and Lucide icons running via <code className="text-violet-600 font-mono text-xs bg-slate-100 px-1 py-0.5 rounded">npm run dev</code>.
            </p>
            <div className="flex items-center text-xs font-medium text-emerald-600">
              <CheckCircle2 className="w-4 h-4 mr-1" />
              Components & Typed Services Ready
            </div>
          </div>
        </div>

        {/* Stage 2: Resume Ingestion & Live ATS Audit */}
        <section className="mb-12">
          <div className="flex items-center space-x-2 mb-4">
            <FileText className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-bold text-slate-900">Resume Ingestion & Deterministic ATS Audit</h2>
          </div>
          <FileUpload onUploadSuccess={(data) => setUploadedResume(data)} />
        </section>

        {/* Live Interactive API Test Sandbox */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 mb-12">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                <h2 className="text-xl font-bold text-slate-900">Career Copilot Live Sandbox</h2>
              </div>
              <p className="text-sm text-slate-500 mt-1">
                Test the backend REST endpoint (<code className="font-mono text-xs bg-slate-100 px-1 py-0.5 rounded">POST /api/v1/copilot/rewrite-bullet</code>) live.
              </p>
            </div>
            <button
              onClick={checkServerHealth}
              className="inline-flex items-center space-x-2 px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-600 bg-slate-100 hover:bg-slate-200 transition-colors self-start sm:self-auto"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Ping Server</span>
            </button>
          </div>

          <form onSubmit={handleTestRewrite} className="mt-6">
            <label className="block text-sm font-semibold text-slate-800 mb-2">
              Enter a weak resume bullet point to test AI STAR / XYZ rephrasing:
            </label>
            <div className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={sampleBullet}
                onChange={(e) => setSampleBullet(e.target.value)}
                placeholder="e.g. worked on fixing bugs in python api"
                className="flex-1 px-4 py-3 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-slate-50/50"
              />
              <button
                type="submit"
                disabled={isRewriting || backendStatus !== 'online'}
                className="inline-flex items-center justify-center space-x-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white font-semibold text-sm shadow-md shadow-indigo-200 transition-all cursor-pointer disabled:cursor-not-allowed"
              >
                {isRewriting ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Rewriting...</span>
                  </>
                ) : (
                  <>
                    <span>Enhance Bullet</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
            {backendStatus !== 'online' && (
              <p className="text-xs text-amber-600 mt-2 flex items-center">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5"></span>
                Backend server is currently offline. Start it with <code className="ml-1 font-mono font-bold">python server.py</code> to test live endpoints.
              </p>
            )}
          </form>

          {/* Enhanced Variants Display */}
          {rewriteResult && (
            <div className="mt-6 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                AI Enhanced Bullet Variants:
              </h4>
              <div className="grid grid-cols-1 gap-3">
                {rewriteResult.enhanced_variants.map((v, idx) => (
                  <div key={idx} className="p-4 rounded-xl border border-indigo-100 bg-indigo-50/30 flex flex-col sm:flex-row items-start justify-between gap-3">
                    <div className="space-y-1 flex-1">
                      <span className="inline-block text-[11px] font-bold text-indigo-700 bg-indigo-100/70 px-2 py-0.5 rounded">
                        {v.formula}
                      </span>
                      <p className="text-sm font-medium text-slate-800">{v.text}</p>
                      <p className="text-xs text-slate-500 italic">{v.rationale}</p>
                    </div>
                    <button
                      onClick={() => handleCopy(v.text, idx)}
                      className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-sm transition-all shrink-0"
                    >
                      {copiedIndex === idx ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-600" />
                          <span className="text-emerald-600">Copied!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5 text-slate-400" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Quick Launch Terminal Commands Card */}
        <div className="bg-slate-900 rounded-2xl p-6 text-white shadow-xl">
          <div className="flex items-center space-x-2 mb-4">
            <Terminal className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-bold text-slate-100">Quick Start Commands</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/50">
              <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block mb-2">
                Terminal 1: Backend Server
              </span>
              <pre className="font-mono text-xs text-slate-300 bg-black/40 p-3 rounded-lg overflow-x-auto">
cd backend{'\n'}
.\venv\Scripts\Activate.ps1{'\n'}
python server.py
              </pre>
              <p className="text-xs text-slate-400 mt-2">
                Swagger Docs will open at: <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="text-indigo-400 hover:underline">http://127.0.0.1:8000/docs</a>
              </p>
            </div>

            <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/50">
              <span className="text-xs font-bold text-violet-400 uppercase tracking-wider block mb-2">
                Terminal 2: Frontend Client
              </span>
              <pre className="font-mono text-xs text-slate-300 bg-black/40 p-3 rounded-lg overflow-x-auto">
cd frontend{'\n'}
npm install{'\n'}
npm run dev
              </pre>
              <p className="text-xs text-slate-400 mt-2">
                Application runs at: <a href="http://localhost:5173" target="_blank" rel="noreferrer" className="text-violet-400 hover:underline">http://localhost:5173</a>
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-200 bg-white py-6 mt-12 text-center text-xs text-slate-500">
        AI-Powered Resume Analyzer &bull; Built with FastAPI &bull; SQLite WAL &bull; React.js &bull; Tailwind CSS
      </footer>
    </div>
  );
};
