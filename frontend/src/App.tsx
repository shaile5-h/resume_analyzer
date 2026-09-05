import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { FileUpload } from './components/FileUpload';
import { resumeApi } from './services/api';
import { BulletRewriteResponse, ResumeUploadResponse } from './types';
import {
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
  
  // Interactive Copilot State
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
    const interval = setInterval(checkServerHealth, 15000);
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
        <div className="text-center max-w-3xl mx-auto mb-10">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            AI-Powered Resume Analyzer <br />
            <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 bg-clip-text text-transparent">
              & Career Copilot
            </span>
          </h1>
          <p className="mt-3 text-base sm:text-lg text-slate-600 leading-relaxed">
            Instant ATS parsability auditing, formatting compliance checks, and high-impact resume enhancement.
          </p>
        </div>

        {/* Resume Ingestion & ATS Audit Section */}
        <section className="mb-10">
          <FileUpload onUploadSuccess={(data) => setUploadedResume(data)} />
        </section>

        {/* Career Copilot: Bullet Enhancer */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
            <div>
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                <h2 className="text-xl font-bold text-slate-900">Career Copilot: Bullet Point Enhancer</h2>
              </div>
              <p className="text-sm text-slate-500 mt-1">
                Transform weak bullet points into high-impact, quantified achievement statements using Google XYZ & STAR formulas.
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
              Enter a resume bullet point to optimize:
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
                    <span>Enhancing...</span>
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
      </main>

      <footer className="border-t border-slate-200 bg-white py-6 mt-12 text-center text-xs text-slate-500">
        AI-Powered Resume Analyzer &bull; Built with FastAPI &bull; SQLite WAL &bull; React.js &bull; Tailwind CSS
      </footer>
    </div>
  );
};
