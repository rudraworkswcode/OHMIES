import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import LoginPage from './pages/LoginPage';
import OverviewPage from './pages/OverviewPage';
import AnalyticsPage from './pages/AnalyticsPage';
import SavingsPage from './pages/SavingsPage';
import Header from './components/Header';
import Navigation from './components/Navigation';
import { LoadingState, ErrorState } from './components/LoadingState';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [overviewData, setOverviewData] = useState(null);
  const [profiles, setProfiles] = useState([]);
  const [selectedMeter, setSelectedMeter] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize session check on load
  useEffect(() => {
    const initAuth = async () => {
      const token = api.getToken();
      if (!token) {
        setIsLoading(false);
        setIsAuthenticated(false);
        return;
      }

      try {
        const user = await api.getMe();
        setCurrentUser(user);
        setSelectedMeter(user.meter_id);
        setIsAuthenticated(true);
        await loadDashboardData(user.meter_id);
      } catch (err) {
        console.warn('Session verification failed, prompting login:', err);
        api.removeToken();
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const loadDashboardData = async (meterId) => {
    setIsLoading(true);
    setError(null);
    try {
      const [overview, profs] = await Promise.all([
        api.getOverview(meterId),
        api.listProfiles().catch(() => [])
      ]);
      setOverviewData(overview);
      setProfiles(profs);
      if (overview?.user) {
        setCurrentUser(prev => ({ ...prev, ...overview.user }));
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch overview metrics.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoginSuccess = async (loginResult) => {
    setIsAuthenticated(true);
    setCurrentUser(loginResult);
    setSelectedMeter(loginResult.meter_id || 'DOM-9821');
    await loadDashboardData(loginResult.meter_id || 'DOM-9821');
  };

  const handleLogout = async () => {
    await api.logout();
    setIsAuthenticated(false);
    setCurrentUser(null);
    setOverviewData(null);
  };

  const handleSwitchProfile = async (meterId) => {
    setSelectedMeter(meterId);
    await loadDashboardData(meterId);
  };

  // If user is not authenticated, display Login Page
  if (!isAuthenticated && !isLoading) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
      {/* Top Header with Welcome User and Goal */}
      <Header
        user={currentUser}
        onLogout={handleLogout}
        activeMeter={selectedMeter}
        onSwitchProfile={handleSwitchProfile}
        profiles={profiles}
      />

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        {/* Navigation Tabs */}
        <Navigation
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />

        {/* Dynamic Tab Content across all phases */}
        {isLoading && !overviewData ? (
          <LoadingState message="Connecting to smart meter telemetry..." />
        ) : error ? (
          <ErrorState error={error} onRetry={() => loadDashboardData(selectedMeter)} />
        ) : (
          <>
            {activeTab === 'overview' && <OverviewPage data={overviewData} />}
            {activeTab === 'analytics' && <AnalyticsPage activeMeter={selectedMeter} />}
            {activeTab === 'savings' && <SavingsPage activeMeter={selectedMeter} user={currentUser} />}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>OHMies Smart Electricity Platform • Central Electricity Authority (CEA) v19 Compliance • All Phases 1, 2 & 3 Active</p>
      </footer>
    </div>
  );
}
