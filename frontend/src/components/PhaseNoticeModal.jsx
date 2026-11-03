import React from 'react';
import { Lock, AlertCircle, X, CheckCircle2 } from 'lucide-react';

export default function PhaseNoticeModal({ isOpen, onClose, tabName, priority }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="h-12 w-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 mb-4">
          <Lock className="w-6 h-6" />
        </div>

        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-3">
          {priority}
        </div>

        <h3 className="text-xl font-bold text-white mb-2">
          {tabName} Locked
        </h3>

        <p className="text-xs text-slate-400 leading-relaxed mb-4">
          According to the project execution instructions in <strong>Phases.md</strong>, development strictly follows a 3-stage sequence:
        </p>

        <div className="space-y-2 p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs text-slate-300 font-mono mb-6">
          <div className="flex items-center gap-2 text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Phase 1 — Tab 1: Overview (Currently Active)</span>
          </div>
          <div className="flex items-center gap-2 text-slate-400">
            <Lock className="w-3.5 h-3.5" />
            <span>Phase 2 — Tab 2: Analytics (Pending Approval)</span>
          </div>
          <div className="flex items-center gap-2 text-slate-500">
            <Lock className="w-3.5 h-3.5" />
            <span>Phase 3 — Tab 3: Savings / Green Pass Road</span>
          </div>
        </div>

        <p className="text-[11px] text-slate-400 mb-6">
          Once Tab 1 is reviewed and approved by the user, Phase 2 will be activated.
        </p>

        <button
          onClick={onClose}
          className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-emerald-500/20 transition cursor-pointer"
        >
          Return to Tab 1 Overview
        </button>
      </div>
    </div>
  );
}

