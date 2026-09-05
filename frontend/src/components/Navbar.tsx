import React from 'react';
import { Sparkles, Activity, FileCode2, ExternalLink } from 'lucide-react';

interface NavbarProps {
  backendStatus: 'checking' | 'online' | 'offline';
}

export const Navbar: React.FC<NavbarProps> = ({ backendStatus }) => {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-md shadow-indigo-200">
              <Sparkles className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <span className="text-lg font-bold text-slate-900 tracking-tight">
                Resume<span className="text-indigo-600">AI</span>
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
                Career Copilot
              </span>
            </div>
          </div>

          {/* Right Header Navigation & Backend Health Status */}
          <div className="flex items-center space-x-4">
            {/* Backend Connectivity Status Pill */}
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-medium border bg-slate-50 border-slate-200">
              <span className="relative flex h-2 w-2">
                {backendStatus === 'online' && (
                  <>
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                  </>
                )}
                {backendStatus === 'offline' && (
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                )}
                {backendStatus === 'checking' && (
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-400 animate-spin"></span>
                )}
              </span>
              <span className="text-slate-600">
                Backend:
                <strong className={`ml-1 ${backendStatus === 'online' ? 'text-emerald-600' : backendStatus === 'offline' ? 'text-rose-600' : 'text-amber-600'}`}>
                  {backendStatus === 'online' ? 'Online (WAL)' : backendStatus === 'offline' ? 'Offline' : 'Connecting...'}
                </strong>
              </span>
            </div>

            {/* Swagger Docs Link */}
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-slate-700 hover:text-indigo-600 hover:bg-slate-100 transition-colors border border-transparent hover:border-slate-200"
            >
              <FileCode2 className="w-3.5 h-3.5" />
              <span>Swagger Docs</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};
