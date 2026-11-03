import React from 'react';

export default function MetricCard({
  title,
  value,
  unit,
  subtitle,
  badgeText,
  badgeType = 'default',
  icon: Icon,
  extraDetails,
  glow = 'green'
}) {
  const badgeColors = {
    green: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    default: 'bg-slate-800 text-slate-300 border-slate-700'
  };

  const glowClass = glow === 'amber' ? 'glow-amber' : glow === 'cyan' ? 'glow-cyan' : 'glow-green';

  return (
    <div className={`bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-5 shadow-xl transition-all duration-300 relative overflow-hidden flex flex-col justify-between group`}>
      {/* Decorative top blur glow */}
      <div className="absolute top-0 right-0 w-28 h-28 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-emerald-500/10 transition"></div>

      <div>
        {/* Header row */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-xs uppercase font-bold tracking-wider text-slate-400">
            {title}
          </span>
          {Icon && (
            <div className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-400 group-hover:text-emerald-400 transition">
              <Icon className="w-4 h-4" />
            </div>
          )}
        </div>

        {/* Big metric value */}
        <div className="flex items-baseline gap-2 mb-2">
          <span className="text-2xl sm:text-3xl font-black font-mono text-white tracking-tight">
            {value}
          </span>
          {unit && (
            <span className="text-xs font-mono font-semibold text-slate-400">
              {unit}
            </span>
          )}
        </div>

        {/* Subtitle / context */}
        {subtitle && (
          <p className="text-xs text-slate-400 leading-relaxed">
            {subtitle}
          </p>
        )}
      </div>

      {/* Extra details & Badge Footer */}
      {(extraDetails || badgeText) && (
        <div className="mt-4 pt-3 border-t border-slate-800/80 flex flex-col gap-2">
          {extraDetails && (
            <div className="text-[11px] font-mono text-slate-300">
              {extraDetails}
            </div>
          )}
          {badgeText && (
            <span className={`inline-flex items-center self-start text-[10px] font-mono font-bold px-2 py-0.5 rounded-md border ${badgeColors[badgeType] || badgeColors.default}`}>
              {badgeText}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

