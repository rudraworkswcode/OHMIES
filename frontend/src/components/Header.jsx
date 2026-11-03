import React from 'react';
import { Zap, Target, LogOut, ShieldCheck, Building2, Home } from 'lucide-react';

export default function Header({ user, onLogout, activeMeter, onSwitchProfile, profiles = [] }) {
  const isDomestic = user?.sector === 'Domestic';

  return (
    <header className="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Branding & Profile Navigation Bar */}
        <div className="h-16 flex items-center justify-between border-b border-slate-800/50">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-amber-400 p-[2px] shadow-lg shadow-emerald-500/20">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Zap className="w-5 h-5 text-emerald-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-black text-xl tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-400 bg-clip-text text-transparent">
                  OHMies
                </span>
                <span className="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 bg-slate-800 text-emerald-400 rounded border border-slate-700">
                  Smart Grid v1.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Smart Electricity Monitoring & Conservation</p>
            </div>
          </div>

          {/* Archetype / Meter Selector & User Logout */}
          <div className="flex items-center gap-3">
            {profiles && profiles.length > 0 && (
              <div className="hidden md:flex items-center gap-2 bg-slate-950/80 px-3 py-1.5 rounded-xl border border-slate-800 text-xs">
                <span className="text-slate-400 font-mono text-[11px]">Archetype:</span>
                <select
                  value={activeMeter || user?.meter_id}
                  onChange={(e) => onSwitchProfile(e.target.value)}
                  className="bg-transparent text-emerald-300 font-semibold focus:outline-none cursor-pointer"
                >
                  <optgroup label="Domestic Households">
                    {profiles.filter(p => p.sector === 'Domestic').map(p => (
                      <option key={p.meter_id} value={p.meter_id} className="bg-slate-900 text-slate-200">
                        🏠 {p.display_name} ({p.subcategory})
                      </option>
                    ))}
                  </optgroup>
                  <optgroup label="Commercial / Industrial">
                    {profiles.filter(p => p.sector === 'Commercial').map(p => (
                      <option key={p.meter_id} value={p.meter_id} className="bg-slate-900 text-slate-200">
                        🏭 {p.display_name} ({p.subcategory})
                      </option>
                    ))}
                  </optgroup>
                </select>
              </div>
            )}

            <button
              onClick={onLogout}
              className="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-xs text-slate-300 hover:text-white transition flex items-center gap-1.5 shadow-sm"
              title="Sign Out"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span>Exit</span>
            </button>
          </div>
        </div>

        {/* PRD Mandated Dashboard Header: Welcome User on Left | Goal on Extreme Right */}
        <div className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2">
              <span>Welcome {user?.display_name || 'User'}</span>
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {isDomestic ? <Home className="w-3 h-3" /> : <Building2 className="w-3 h-3" />}
                {user?.sector} • {user?.subcategory}
              </span>
            </h1>
            <p className="text-xs text-slate-400 font-mono">
              Meter ID: <strong className="text-slate-200">{user?.meter_id || 'DOM-9821'}</strong>
            </p>
          </div>

          {/* Goal on Extreme Right */}
          <div className="bg-slate-950/90 border border-amber-500/30 p-3.5 rounded-2xl flex items-center gap-3.5 min-w-[260px] shadow-lg">
            <div className="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 flex-shrink-0">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-wider text-amber-400 font-bold">Goal</p>
              <p className="text-sm font-black text-white font-mono">
                {user?.goal_description || 'Cut 14.5 kWh this week'}
              </p>
              <p className="text-[11px] text-emerald-400 font-semibold font-mono">
                Target: {user?.goal_kwh_per_week || 14.5} kWh reduction
              </p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

