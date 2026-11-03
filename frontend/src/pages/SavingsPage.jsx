import React, { useState, useEffect } from 'react';
import {
  Sparkles, Target, Trophy, Gift, ArrowRight, CheckCircle2,
  Sliders, TrendingUp, Building2, ShieldCheck, RotateCcw,
  Zap, Award, DollarSign
} from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { api } from '../services/api';
import { LoadingState, ErrorState } from '../components/LoadingState';

export default function SavingsPage({ activeMeter, user }) {
  const isDomestic = user?.sector === 'Domestic';

  // State
  const [streak, setStreak] = useState(3);
  const [peakShift, setPeakShift] = useState(25);
  const [targetReductionPct, setTargetReductionPct] = useState(15);

  const [domesticData, setDomesticData] = useState(null);
  const [commercialData, setCommercialData] = useState(null);
  const [simData, setSimData] = useState(null);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSavingsData();
  }, [activeMeter, streak, peakShift, targetReductionPct]);

  const loadSavingsData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      if (isDomestic) {
        const [domRes, simRes] = await Promise.all([
          api.request(`/savings/domestic?meter_id=${encodeURIComponent(activeMeter || '')}&streak=${streak}`),
          api.request(`/savings/simulate?meter_id=${encodeURIComponent(activeMeter || '')}&reduction_pct=${targetReductionPct}`)
        ]);
        setDomesticData(domRes);
        setSimData(simRes);
      } else {
        const [commRes, simRes] = await Promise.all([
          api.request(`/savings/commercial?meter_id=${encodeURIComponent(activeMeter || '')}&peak_shift=${peakShift}`),
          api.request(`/savings/simulate?meter_id=${encodeURIComponent(activeMeter || '')}&reduction_pct=${targetReductionPct}`)
        ]);
        setCommercialData(commRes);
        setSimData(simRes);
      }
    } catch (err) {
      setError(err.message || 'Failed to load savings calculations.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSimulateStreak = () => {
    setStreak(prev => Math.min(52, prev + 1));
  };

  const handleResetStreak = () => {
    setStreak(1);
  };

  if (isLoading && !domesticData && !commercialData) {
    return <LoadingState message="Computing battlepass milestones and financial OPEX projections..." />;
  }
  if (error) {
    return <ErrorState error={error} onRetry={loadSavingsData} />;
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* ================= SECTION A: DOMESTIC TRACK (THE GREENPASS ROAD) ================= */}
      {isDomestic && domesticData && (
        <div className="space-y-8">
          {/* Header Banner */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-black tracking-tight text-white flex items-center gap-2">
                  <Trophy className="w-6 h-6 text-amber-400" /> The GreenPass Road
                </h2>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono font-bold border border-amber-500/30">
                  SEASON 1: ZERO-WASTE
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Every weekly conservation target met fills your battle-pass bar. Unlock actual items funded directly by your utility bill savings!
              </p>
            </div>

            {/* Streak & Vault Badges */}
            <div className="flex items-center gap-3">
              <div className="px-4 py-2 rounded-2xl bg-slate-950 border border-slate-800 text-right font-mono">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Green Streak</span>
                <span className="text-sm font-black text-emerald-400">{domesticData.streak_weeks} WEEKS ACTIVE 🔥</span>
              </div>
            </div>
          </div>

          {/* Battle Pass Progression Card */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 relative overflow-hidden shadow-2xl space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center font-black font-mono text-amber-300">
                  W{domesticData.streak_weeks}
                </div>
                <div>
                  <div className="text-xs font-bold uppercase tracking-wider text-slate-200">
                    {domesticData.active_tier_label}
                  </div>
                  <div className="text-[11px] text-emerald-400 font-mono font-bold">
                    ₹{domesticData.accumulated_savings_inr} Total Accumulated Savings in Vault
                  </div>
                </div>
              </div>

              {/* Simulation Controls */}
              <div className="flex items-center gap-2">
                <button
                  onClick={handleSimulateStreak}
                  className="px-3.5 py-2 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 border border-emerald-500/40 text-emerald-300 text-xs font-bold flex items-center gap-1.5 transition cursor-pointer shadow-sm"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Simulate 1 Week Goal Hit (+XP)</span>
                </button>
                <button
                  onClick={handleResetStreak}
                  className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white text-xs transition cursor-pointer"
                  title="Reset Streak"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Overall Level Progress Bar */}
            <div className="relative w-full h-3.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 via-amber-400 to-teal-400 transition-all duration-700 relative"
                style={{ width: `${Math.max(5, domesticData.progress_percentage)}%` }}
              >
                <div className="absolute right-0 top-0 bottom-0 w-2 bg-white blur-[2px] animate-pulse"></div>
              </div>
            </div>

            {/* Horizontal Scrollable Rewards Road */}
            <div className="overflow-x-auto pb-4 pt-2">
              <div className="flex items-center gap-4 min-w-max px-1">
                {domesticData.roadmap.map((node) => (
                  <div
                    key={node.week}
                    className={`w-52 p-4 rounded-2xl border transition-all duration-300 flex flex-col justify-between ${
                      node.is_unlocked
                        ? 'bg-slate-950 border-emerald-500/50 glow-green'
                        : 'bg-slate-950/50 border-slate-800 opacity-75'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-2xl">{node.icon}</span>
                        <span
                          className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${
                            node.is_unlocked
                              ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                              : 'bg-slate-800 text-slate-400 border-slate-700'
                          }`}
                        >
                          {node.is_unlocked ? 'UNLOCKED' : `Week ${node.week}`}
                        </span>
                      </div>
                      <h4 className="text-xs font-bold text-white mb-1 leading-snug">{node.title}</h4>
                      <p className="text-[10px] text-slate-400 leading-relaxed mb-3">{node.description}</p>
                    </div>

                    <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between font-mono text-[11px]">
                      <span className="text-slate-400">Target Cost:</span>
                      <strong className={node.is_unlocked ? 'text-emerald-400' : 'text-slate-200'}>₹{node.cost_inr}</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Upcoming Milestone Callout */}
            {domesticData.upcoming_milestone && (
              <div className="p-4 rounded-2xl bg-slate-950 border border-amber-500/30 flex flex-col md:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="text-3xl p-3 bg-slate-900 rounded-2xl border border-slate-800">
                    {domesticData.upcoming_milestone.icon}
                  </div>
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400">
                      Upcoming Milestone (Week {domesticData.upcoming_milestone.week})
                    </span>
                    <h4 className="text-base font-bold text-white">{domesticData.upcoming_milestone.title}</h4>
                    <p className="text-xs text-slate-400">{domesticData.upcoming_milestone.description}</p>
                  </div>
                </div>
                <div className="text-right px-4 py-2 bg-slate-900 rounded-xl border border-slate-800 font-mono">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Needed To Unlock</span>
                  <span className="text-sm font-black text-emerald-400">
                    ₹{domesticData.upcoming_milestone.remaining_inr} More
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Tangible Reward Wishlists */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-pink-400">
                <Gift className="w-4 h-4" />
                <h4 className="font-bold text-sm text-slate-200">Micro-Treats (Weekly)</h4>
              </div>
              <p className="text-xs text-slate-400">Every single week below baseline funds small instant rewards.</p>
              <ul className="text-xs space-y-2 text-slate-300 font-mono">
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• 2x Cold Brew Coffees</span><span className="text-emerald-400">₹180</span></li>
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• Premium OTT Sub Monthly</span><span className="text-emerald-400">₹299</span></li>
                <li className="flex justify-between"><span>• PVR Cinema Popcorn Combo</span><span className="text-emerald-400">₹450</span></li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-cyan-400">
                <Gift className="w-4 h-4" />
                <h4 className="font-bold text-sm text-slate-200">Mid-Tier Gear (Quarterly)</h4>
              </div>
              <p className="text-xs text-slate-400">Accumulated 3-month savings to upgrade your lifestyle gear.</p>
              <ul className="text-xs space-y-2 text-slate-300 font-mono">
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• ANC Wireless Earbuds</span><span className="text-emerald-400">₹1,999</span></li>
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• Weekend Dine-out for 2</span><span className="text-emerald-400">₹2,800</span></li>
                <li className="flex justify-between"><span>• Smart Fitness Tracker</span><span className="text-emerald-400">₹3,499</span></li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-amber-400">
                <Gift className="w-4 h-4" />
                <h4 className="font-bold text-sm text-slate-200">The Grand Prize (Annual)</h4>
              </div>
              <p className="text-xs text-slate-400">Annual cumulative savings to fund an entire domestic escape.</p>
              <ul className="text-xs space-y-2 text-slate-300 font-mono">
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• Goa 3-Day Beach Retreat</span><span className="text-emerald-400">₹14,500</span></li>
                <li className="flex justify-between border-b border-slate-800/80 pb-1.5"><span>• Round-trip Flight Tickets</span><span className="text-emerald-400">₹11,000</span></li>
                <li className="flex justify-between"><span>• High-End HEPA Air Purifier</span><span className="text-emerald-400">₹12,800</span></li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* ================= SECTION B: COMMERCIAL TRACK (FINANCIAL INTELLIGENCE) ================= */}
      {!isDomestic && commercialData && (
        <div className="space-y-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl">
            <div>
              <div className="flex items-center gap-2">
                <Building2 className="w-6 h-6 text-cyan-400" />
                <h2 className="text-2xl font-black tracking-tight text-white">Commercial Financial Analytics</h2>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono font-bold border border-cyan-500/30">
                  OPEX & EBITDA RECOVERY
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Bottom-line financial metrics: direct OPEX reductions, EBITDA margin expansion, and ToD surcharges avoided.
              </p>
            </div>

            {/* Peak Shift Control Slider */}
            <div className="bg-slate-950 border border-slate-800 rounded-2xl p-3 flex items-center gap-4">
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Peak Load Shift Rate</span>
                <span className="text-xs font-bold font-mono text-cyan-400">{peakShift}% Shifted to Off-Peak</span>
              </div>
              <input
                type="range"
                min="0"
                max="60"
                step="5"
                value={peakShift}
                onChange={(e) => setPeakShift(Number(e.target.value))}
                className="w-28 accent-cyan-400 cursor-pointer"
              />
            </div>
          </div>

          {/* 4 Financial KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">Direct OPEX Preserved</span>
              <span className="text-2xl sm:text-3xl font-black font-mono text-emerald-400">₹{commercialData.direct_opex_preserved_inr.toLocaleString()}</span>
              <p className="text-[11px] text-emerald-400 mt-2 font-semibold">Net monthly operational savings</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">Operating Margin Boost</span>
              <span className="text-2xl sm:text-3xl font-black font-mono text-cyan-400">+{commercialData.operating_margin_boost_pct}%</span>
              <p className="text-[11px] text-slate-400 mt-2">Expansion in quarterly net margin</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">Top-Line Revenue Impact</span>
              <span className="text-2xl sm:text-3xl font-black font-mono text-indigo-400">₹{commercialData.equivalent_revenue_inr.toLocaleString()}</span>
              <p className="text-[11px] text-slate-400 mt-2">Based on standard 10% margin multiplier</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <span className="text-[10px] uppercase font-bold text-slate-400 block mb-1">ToD Surcharges Avoided</span>
              <span className="text-2xl sm:text-3xl font-black font-mono text-amber-400">₹{commercialData.tod_surcharges_avoided_inr.toLocaleString()}</span>
              <p className="text-[11px] text-slate-400 mt-2">Peak tariff slab penalties prevented</p>
            </div>
          </div>

          {/* Action Plan & ESG Badge */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-5 h-5" />
                <h4 className="font-bold text-sm text-slate-100">Specific Cluster Action Plan</h4>
              </div>
              <ul className="space-y-2 text-xs text-slate-300">
                {commercialData.action_plan.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2 p-2 rounded-xl bg-slate-950 border border-slate-800">
                    <span className="text-emerald-400 font-bold">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-center gap-2 text-indigo-400 mb-2">
                  <Award className="w-5 h-5" />
                  <h4 className="font-bold text-sm text-slate-100">{commercialData.compliance_badge.title}</h4>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Based on operating energy efficiency in the top 15% tier among peer operators, this facility qualifies for the municipal Clean Energy Compliance Seal.
                </p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs font-mono">
                <div>
                  <span className="text-slate-400 block text-[10px]">Validity</span>
                  <span className="text-emerald-400 font-bold">{commercialData.compliance_badge.valid_through}</span>
                </div>
                <span className="text-[11px] text-slate-300">Certified by {commercialData.compliance_badge.issuing_body}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ================= SECTION C: INTERACTIVE WHAT-IF SAVINGS PLAYGROUND ================= */}
      {simData && (
        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
            <div>
              <h3 className="text-lg font-black text-white flex items-center gap-2">
                <Sliders className="w-5 h-5 text-emerald-400" />
                Interactive Reduction Playground & Financial Simulator
              </h3>
              <p className="text-xs text-slate-400">
                Adjust the reduction slider to model transparent electricity bill savings and emissions abatements.
              </p>
            </div>
            <div className="text-right font-mono">
              <span className="text-xs text-slate-400">Calculated Annualized Gain: </span>
              <span className="text-sm font-black text-emerald-400">₹{simData.annual_saved_inr.toLocaleString()} / yr</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            {/* Slider Control */}
            <div className="space-y-3">
              <div className="flex justify-between text-xs text-slate-300 font-mono">
                <span>Target Conservation Percentage</span>
                <span className="font-bold text-emerald-400">{targetReductionPct}% Cutback</span>
              </div>
              <input
                type="range"
                min="5"
                max="40"
                step="1"
                value={targetReductionPct}
                onChange={(e) => setTargetReductionPct(Number(e.target.value))}
                className="w-full accent-emerald-500 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                <span>5% (Light effort)</span>
                <span>20% (Moderate)</span>
                <span>40% (Aggressive)</span>
              </div>
            </div>

            {/* Calculated Result Cards */}
            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800 flex items-center justify-around text-center font-mono">
              <div>
                <p className="text-[10px] uppercase font-bold text-slate-400">Monthly Saved</p>
                <p className="text-lg font-black text-emerald-400">₹{simData.monthly_saved_inr.toLocaleString()}</p>
              </div>
              <div className="h-8 w-[1px] bg-slate-800"></div>
              <div>
                <p className="text-[10px] uppercase font-bold text-slate-400">CO₂ Avoided</p>
                <p className="text-lg font-black text-teal-400">{simData.co2_avoided_kg_per_month} kg/mo</p>
              </div>
              <div className="h-8 w-[1px] bg-slate-800"></div>
              <div>
                <p className="text-[10px] uppercase font-bold text-slate-400">Equiv. Trees</p>
                <p className="text-lg font-black text-amber-400">{simData.equivalent_trees_monthly} Trees</p>
              </div>
            </div>
          </div>

          {/* Transparent Mathematical Assumptions */}
          <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80 text-[11px] font-mono text-slate-400 grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <span className="text-slate-500 block">Baseline Consumption:</span>
              <strong className="text-slate-200">{simData.baseline_monthly_kwh} kWh/month</strong>
            </div>
            <div>
              <span className="text-slate-500 block">Target Reduced Load:</span>
              <strong className="text-slate-200">{simData.reduced_monthly_kwh} kWh/month</strong>
            </div>
            <div>
              <span className="text-slate-500 block">Applicable Effective Tariff:</span>
              <strong className="text-slate-200">₹{simData.applicable_tariff_rate} / kWh</strong>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

