import React from 'react';
import { Loader2, Zap } from 'lucide-react';

export function LoadingState({ message = "Calculating electricity consumption metrics..." }) {
  return (
    <div className="min-h-[400px] flex flex-col items-center justify-center p-8 bg-slate-900/50 border border-slate-800 rounded-2xl text-center">
      <div className="relative mb-4">
        <div className="h-14 w-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 animate-pulse">
          <Zap className="w-7 h-7" />
        </div>
        <Loader2 className="w-8 h-8 text-emerald-400 animate-spin absolute -top-1 -right-1" />
      </div>
      <h3 className="text-base font-bold text-white mb-1">Loading Energy Analytics</h3>
      <p className="text-xs text-slate-400 font-mono max-w-sm">{message}</p>
    </div>
  );
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="min-h-[350px] flex flex-col items-center justify-center p-8 bg-slate-900 border border-red-900/50 rounded-2xl text-center">
      <div className="h-12 w-12 rounded-2xl bg-red-500/10 border border-red-500/30 flex items-center justify-center text-red-400 mb-4">
        <Zap className="w-6 h-6" />
      </div>
      <h3 className="text-base font-bold text-white mb-2">Unable to Load Metrics</h3>
      <p className="text-xs text-red-400 font-mono max-w-md mb-6">{error || "An unexpected error occurred while communicating with the database."}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-xl border border-slate-700 transition"
        >
          Retry Fetching
        </button>
      )}
    </div>
  );
}

