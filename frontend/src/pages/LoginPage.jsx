import React, { useState } from 'react';
import { Zap, Lock, User, Eye, EyeOff, ShieldCheck, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

export default function LoginPage({ onLoginSuccess }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [validationErrors, setValidationErrors] = useState({});

  const validate = () => {
    const errors = {};
    if (!userId.trim()) {
      errors.userId = 'Please enter your User ID or Name.';
    }
    if (!password) {
      errors.password = 'Please enter your password.';
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    
    if (!validate()) {
      return;
    }

    setIsLoading(true);
    try {
      const data = await api.login(userId.trim(), password);
      onLoginSuccess(data);
    } catch (err) {
      // PRD Section 3 Requirement: Exact message in dark red text
      setErrorMessage(err.message || 'Invalid UID and Password, pls try again later');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFillDemo = () => {
    setUserId('JEEVAN KRISHNA');
    setPassword('JAI RNSIT');
    setErrorMessage('');
    setValidationErrors({});
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden">
      {/* Decorative background glows */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="h-14 w-14 mx-auto rounded-2xl bg-gradient-to-tr from-emerald-600 via-teal-500 to-amber-400 p-[2px] shadow-lg shadow-emerald-500/20 mb-4">
            <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
              <Zap className="w-7 h-7 text-emerald-400" />
            </div>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            OHMies
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Smart Electricity Monitoring & Conservation Platform
          </p>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mt-3">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Secure Authentication Gateway</span>
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5" noValidate>
          {/* User ID / Name Field */}
          <div>
            <label className="block text-xs uppercase font-bold tracking-wider text-slate-400 mb-2">
              User ID / Name
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter User ID (e.g. JEEVAN KRISHNA)"
                className={`w-full pl-10 pr-4 py-2.5 bg-slate-950 border ${
                  validationErrors.userId ? 'border-red-500/80 focus:border-red-500' : 'border-slate-800 focus:border-emerald-500'
                } rounded-xl text-sm text-white placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono`}
              />
            </div>
            {validationErrors.userId && (
              <p className="text-red-400 text-[11px] mt-1.5 flex items-center gap-1">
                <AlertCircle className="w-3 h-3" /> {validationErrors.userId}
              </p>
            )}
          </div>

          {/* Password Field */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs uppercase font-bold tracking-wider text-slate-400">
                Password
              </label>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-[11px] text-slate-400 hover:text-slate-200 transition flex items-center gap-1"
              >
                {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                <span>{showPassword ? 'Hide' : 'Show'}</span>
              </button>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className={`w-full pl-10 pr-10 py-2.5 bg-slate-950 border ${
                  validationErrors.password ? 'border-red-500/80 focus:border-red-500' : 'border-slate-800 focus:border-emerald-500'
                } rounded-xl text-sm text-white placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono`}
              />
            </div>
            {validationErrors.password && (
              <p className="text-red-400 text-[11px] mt-1.5 flex items-center gap-1">
                <AlertCircle className="w-3 h-3" /> {validationErrors.password}
              </p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 rounded-xl font-bold text-sm bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/25 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {isLoading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>Sign In to Dashboard</span>
                <Zap className="w-4 h-4" />
              </>
            )}
          </button>

          {/* PRD Mandated Invalid Credentials Error Message: Dark red text clearly visible below form */}
          {errorMessage && (
            <div
              id="login-error-message"
              className="p-3.5 rounded-xl bg-red-950/40 border border-red-900/60 text-center animate-fade-in"
            >
              <p className="text-red-600 font-bold text-sm tracking-wide">
                {errorMessage}
              </p>
            </div>
          )}
        </form>

        {/* Quick Demo Credentials Helper */}
        <div className="mt-6 pt-6 border-t border-slate-800/80 text-center">
          <p className="text-[11px] text-slate-500 mb-2">Development Identity Reference:</p>
          <button
            type="button"
            onClick={handleFillDemo}
            className="px-3 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 border border-slate-800 text-[11px] text-emerald-400 font-mono transition"
          >
            Auto-fill: JEEVAN KRISHNA
          </button>
        </div>
      </div>
    </div>
  );
}

