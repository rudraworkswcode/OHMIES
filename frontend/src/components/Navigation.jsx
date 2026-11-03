import React from 'react';
import { LayoutDashboard, LineChart, Sparkles } from 'lucide-react';

export default function Navigation({ activeTab, setActiveTab }) {
  const tabs = [
    { id: 'overview', name: 'Tab 1 — Overview', icon: LayoutDashboard },
    { id: 'analytics', name: 'Tab 2 — Analytics', icon: LineChart },
    { id: 'savings', name: 'Tab 3 — Savings / Green Pass', icon: Sparkles },
  ];

  return (
    <div className="border-b border-slate-800/80 mb-8">
      <div className="flex space-x-2 sm:space-x-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`pb-3 px-4 font-semibold text-sm transition-all border-b-2 flex items-center gap-2 cursor-pointer ${
                isActive
                  ? 'border-emerald-400 text-emerald-400 shadow-sm'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.name}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
