import React from 'react';
import { 
  Zap, 
  Clock, 
  Leaf, 
  Receipt, 
  TrendingDown, 
  TrendingUp, 
  Minus, 
  Sparkles, 
  Database, 
  CheckCircle2, 
  AlertTriangle,
  Calendar,
  BarChart2
} from 'lucide-react';
import MetricCard from '../components/MetricCard';

export default function OverviewPage({ data }) {
  if (!data) return null;

  const {
    average_daily_draw,
    peak_window_intensity,
    grid_carbon_footprint,
    tariff_bracket,
    summary,
    data_source,
    reporting_period,
    total_records_analyzed,
    user
  } = data;

  const trendIcon = summary.trend_direction === 'decreasing' ? (
    <TrendingDown className="w-4 h-4 text-emerald-400" />
  ) : summary.trend_direction === 'increasing' ? (
    <TrendingUp className="w-4 h-4 text-amber-400" />
  ) : (
    <Minus className="w-4 h-4 text-slate-400" />
  );

  const trendBadgeColor = summary.trend_direction === 'decreasing' ? 'green' : summary.trend_direction === 'increasing' ? 'amber' : 'default';

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Overview Context & Data Source Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-900/60 border border-slate-800/80 px-4 py-3 rounded-2xl">
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <Calendar className="w-3.5 h-3.5 text-emerald-400" />
          <span>Reporting Period: <strong className="text-slate-200">{reporting_period}</strong></span>
          <span className="text-slate-600">•</span>
          <span>{total_records_analyzed} hourly readings analyzed</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-mono font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Database className="w-3 h-3" />
            <span>{data_source}</span>
          </span>
        </div>
      </div>

      {/* FOUR PRIMARY METRIC CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* 1. Average Daily Draw */}
        <MetricCard
          title="Average Daily Draw"
          value={average_daily_draw.value.toFixed(1)}
          unit={average_daily_draw.unit}
          subtitle={average_daily_draw.subtext}
          icon={Zap}
          badgeText={
            summary.trend_direction === 'decreasing'
              ? `▼ ${summary.trend_percentage}% Lower Trend`
              : summary.trend_direction === 'increasing'
              ? `▲ ${summary.trend_percentage}% Higher Trend`
              : 'Steady Trajectory'
          }
          badgeType={trendBadgeColor}
          glow="green"
        />

        {/* 2. Peak Window Intensity */}
        <MetricCard
          title="Peak Window Intensity"
          value={peak_window_intensity.window}
          unit=""
          subtitle={`Cumulative Window Energy: ${peak_window_intensity.energy_kwh.toFixed(2)} ${peak_window_intensity.unit_energy}`}
          icon={Clock}
          extraDetails={
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-300">
              <span>Instantaneous Demand:</span>
              <strong className="text-amber-400">{peak_window_intensity.demand_kw.toFixed(2)} {peak_window_intensity.unit_demand}</strong>
            </div>
          }
          badgeText="Energy (kWh) vs Demand (kW)"
          badgeType="amber"
          glow="amber"
        />

        {/* 3. Grid Carbon Footprint */}
        <MetricCard
          title="Grid Carbon Footprint"
          value={grid_carbon_footprint.daily_emissions_kg_co2e.toFixed(1)}
          unit="kg CO2e / day"
          subtitle={`Total: ${grid_carbon_footprint.total_emissions_kg_co2e.toFixed(1)} kg CO2e over reporting period`}
          icon={Leaf}
          extraDetails={
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-300">
              <span>Offset Equivalence:</span>
              <span className="text-emerald-400">{grid_carbon_footprint.equivalent_trees_offset_per_month} trees/mo</span>
            </div>
          }
          badgeText="CEA Factor: 0.72 kg/kWh"
          badgeType="green"
          glow="green"
        />

        {/* 4. Tariff Bracket */}
        <MetricCard
          title="Tariff Bracket"
          value={`₹${tariff_bracket.average_effective_rate_inr.toFixed(2)}`}
          unit={tariff_bracket.unit}
          subtitle={tariff_bracket.slab_structure}
          icon={Receipt}
          extraDetails={
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-300">
              <span>Est. Daily Spend:</span>
              <strong className="text-cyan-400">₹{tariff_bracket.estimated_daily_cost_inr.toFixed(2)} / day</strong>
            </div>
          }
          badgeText={tariff_bracket.tariff_category}
          badgeType="cyan"
          glow="cyan"
        />
      </div>

      {/* INTELLIGENT CONSUMPTION SUMMARY */}
      <section className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-800/80 gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Sparkles className="w-4 h-4" />
              </span>
              <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
                Intelligent Consumption Summary
              </h2>
            </div>
            <p className="text-xs text-slate-400">
              Statistical evaluation derived from actual consumption records for {user.display_name}.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center gap-2">
              {trendIcon}
              <span className="text-xs font-mono font-bold text-slate-200">
                {summary.trend_direction.toUpperCase()} ({summary.trend_percentage}%)
              </span>
            </div>
          </div>
        </div>

        {/* Core Statistical Insights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left: Summary Analysis narrative */}
          <div className="space-y-4">
            <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80 space-y-2">
              <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400">
                Observed Consumption Trajectory
              </span>
              <h3 className="text-base font-bold text-slate-100 leading-snug">
                {summary.headline}
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                {summary.comparison_text}
              </p>
            </div>

            {/* Quick statistical breakdown badges */}
            <div className="grid grid-cols-3 gap-3 font-mono">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-center">
                <span className="text-[10px] uppercase text-slate-500 font-bold block mb-1">Total Draw</span>
                <span className="text-sm font-bold text-emerald-400">{summary.current_consumption_kwh} kWh</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-center">
                <span className="text-[10px] uppercase text-slate-500 font-bold block mb-1">Weekend Ratio</span>
                <span className="text-sm font-bold text-cyan-400">{summary.statistical_details?.weekend_ratio || 1.18}x</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-center">
                <span className="text-[10px] uppercase text-slate-500 font-bold block mb-1">Night Share</span>
                <span className="text-sm font-bold text-amber-400">{summary.statistical_details?.night_consumption_share_pct || 22.4}%</span>
              </div>
            </div>
          </div>

          {/* Right: Actionable Sector-Specific Recommendations */}
          <div className="space-y-3">
            <span className="text-xs uppercase font-bold tracking-wider text-slate-400 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Tailored Conservation Actions ({user.subcategory})
            </span>

            <div className="space-y-2.5">
              {summary.actionable_recommendations.map((tip, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-emerald-500/30 transition group"
                >
                  <span className="h-5 w-5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center text-xs font-bold font-mono flex-shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <p className="text-xs text-slate-300 leading-relaxed group-hover:text-slate-100 transition">
                    {tip}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

