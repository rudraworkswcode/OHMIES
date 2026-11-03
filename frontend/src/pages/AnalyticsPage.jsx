import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  Calendar, Clock, Sparkles, TrendingUp, BarChart3,
  PieChart as PieIcon, Lightbulb, CheckCircle2, Zap
} from 'lucide-react';
import { api } from '../services/api';
import { LoadingState, ErrorState } from '../components/LoadingState';

export default function AnalyticsPage({ activeMeter }) {
  const [range, setRange] = useState('30d');
  const [breakdownMode, setBreakdownMode] = useState('equipment'); // 'equipment' | 'timeslot'
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalytics();
  }, [activeMeter, range]);

  const loadAnalytics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await api.getAnalytics(activeMeter, range);
      setData(res);
    } catch (err) {
      setError(err.message || 'Failed to fetch analytics telemetry.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <LoadingState message="Aggregating historical electricity load curves..." />;
  if (error) return <ErrorState error={error} onRetry={loadAnalytics} />;
  if (!data) return null;

  const {
    daily_trends,
    weekly_data,
    equipment_breakdown,
    time_slot_breakdown,
    smart_tips,
    reporting_period,
    total_energy_kwh,
    subcategory
  } = data;

  const pieData = breakdownMode === 'equipment' ? equipment_breakdown : time_slot_breakdown.map(s => ({
    category: `${s.slot} (${s.time_range})`,
    kwh: s.kwh,
    percentage: s.percentage,
    color: s.slot === 'Night' ? '#6366f1' : s.slot === 'Morning' ? '#f59e0b' : s.slot === 'Afternoon' ? '#06b6d4' : '#10b981'
  }));

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header & Range Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-emerald-400" /> Historical Consumption & Load Analytics
            </h2>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-emerald-400 border border-slate-700">
              Phase 2 Active
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Telemetry span: <strong className="text-slate-200">{reporting_period}</strong> • Total Recorded: <strong className="text-emerald-400">{total_energy_kwh} kWh</strong>
          </p>
        </div>

        {/* Range Selector */}
        <div className="flex items-center gap-2 bg-slate-950 p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
          {['7d', '14d', '30d'].map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition cursor-pointer ${
                range === r
                  ? 'bg-emerald-500 text-slate-950 shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {r === '7d' ? 'Last 7 Days' : r === '14d' ? 'Last 14 Days' : 'Full 30 Days'}
            </button>
          ))}
        </div>
      </div>

      {/* GRAPH 1: DAILY CONSUMPTION & ROLLING TRENDS */}
      <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-4">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              Daily Electricity Consumption & 7-Day Rolling Trend Line
            </h3>
            <p className="text-xs text-slate-400">
              Comparing daily meter draw against smoothed 7-day trailing baseline to identify deviations.
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> Daily kWh
            </span>
            <span className="flex items-center gap-1.5 text-cyan-400">
              <span className="w-3 h-1 bg-cyan-400 inline-block"></span> 7-Day Rolling Avg
            </span>
          </div>
        </div>

        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={daily_trends} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} unit=" kWh" />
              <Tooltip
                contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '12px' }}
                formatter={(val, name) => [`${val} kWh`, name === 'energy_kwh' ? 'Daily Energy' : '7-Day Rolling Avg']}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Line
                type="monotone"
                dataKey="energy_kwh"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 3, fill: '#10b981' }}
                activeDot={{ r: 5 }}
                name="energy_kwh"
              />
              <Line
                type="monotone"
                dataKey="rolling_avg_kwh"
                stroke="#06b6d4"
                strokeWidth={2.5}
                strokeDasharray="4 4"
                dot={false}
                name="rolling_avg_kwh"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* TWO COLUMN ROW: WEEKLY BAR GRAPH & PIE BREAKDOWN */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* GRAPH 2: WEEKLY BAR GRAPH */}
        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="border-b border-slate-800/80 pb-3">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-amber-400" />
              Weekly Aggregation (kWh / Week)
            </h3>
            <p className="text-xs text-slate-400">
              Discrete 7-day intervals with target conservation threshold.
            </p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weekly_data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="week_label" tick={{ fill: '#64748b', fontSize: 11 }} />
                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} unit=" kWh" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '12px' }}
                  formatter={(val, name, item) => [
                    `${val} kWh (Avg ${item.payload.avg_daily_kwh} kWh/d)`,
                    name === 'total_kwh' ? 'Actual Consumed' : 'Weekly Target'
                  ]}
                  labelFormatter={(lbl) => `${lbl}`}
                />
                <Bar dataKey="total_kwh" fill="#10b981" radius={[6, 6, 0, 0]} name="total_kwh" />
                <Bar dataKey="target_kwh" fill="#334155" radius={[6, 6, 0, 0]} name="target_kwh" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-4 gap-2 pt-2 border-t border-slate-800/60 font-mono text-center">
            {weekly_data.map(w => (
              <div key={w.week_number} className="bg-slate-950 p-2 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-500 block">{w.week_label}</span>
                <span className="text-xs font-bold text-slate-200">{w.total_kwh} kWh</span>
                {w.change_vs_prior_pct !== null && (
                  <span className={`text-[10px] block font-semibold ${w.change_vs_prior_pct <= 0 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {w.change_vs_prior_pct <= 0 ? `▼ ${Math.abs(w.change_vs_prior_pct)}%` : `▲ ${w.change_vs_prior_pct}%`}
                  </span>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* GRAPH 3: PIE CHART BREAKDOWN */}
        <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <PieIcon className="w-4 h-4 text-cyan-400" />
                Consumption Distribution
              </h3>
              <p className="text-xs text-slate-400">
                Category proportion breakdown based on verified telemetry.
              </p>
            </div>

            {/* Toggle Breakdown Mode */}
            <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
              <button
                onClick={() => setBreakdownMode('equipment')}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-bold transition cursor-pointer ${
                  breakdownMode === 'equipment' ? 'bg-cyan-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Appliance / Load
              </button>
              <button
                onClick={() => setBreakdownMode('timeslot')}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-mono font-bold transition cursor-pointer ${
                  breakdownMode === 'timeslot' ? 'bg-cyan-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Time of Day
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="kwh"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    innerRadius={45}
                    paddingAngle={3}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '12px' }}
                    formatter={(val, name, entry) => [`${val} kWh (${entry.payload.percentage}%)`, name]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-2">
              {pieData.map((slice, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs p-2 rounded-lg bg-slate-950 border border-slate-800">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: slice.color }}></span>
                    <span className="text-slate-300 font-medium truncate max-w-[130px]">{slice.category}</span>
                  </div>
                  <span className="font-mono text-emerald-400 font-bold">{slice.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>

      {/* SMART TIPS CATALOGUE */}
      <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl space-y-4">
        <div className="border-b border-slate-800/80 pb-4">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-400" />
            <h3 className="text-lg font-black text-white">
              Predefined Smart Tips Catalogue — {subcategory}
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Conservation advice derived from actual load telemetry without fabricated guarantees.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {smart_tips.map((tip) => (
            <div key={tip.id} className="p-5 rounded-2xl bg-slate-950 border border-slate-800 flex flex-col justify-between hover:border-emerald-500/40 transition">
              <div className="space-y-2.5">
                <span className="h-6 w-6 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center justify-center text-xs font-bold font-mono">
                  {tip.id}
                </span>
                <h4 className="text-sm font-bold text-white leading-snug">{tip.title}</h4>
                <p className="text-xs text-slate-300 leading-relaxed">{tip.description}</p>
                <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800/80 text-[11px] text-slate-400 leading-normal">
                  <strong className="text-slate-300 block mb-0.5">Observed Rationale:</strong>
                  {tip.rationale}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800/80">
                <span className="text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  {tip.estimated_impact}
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

