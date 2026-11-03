// API Client service for OHMies

const API_BASE = '/api';
const DIRECT_BACKEND_BASE = 'http://127.0.0.1:8000/api';

export const api = {
  // Store & retrieve token
  getToken() {
    return localStorage.getItem('ohmies_token');
  },
  setToken(token) {
    localStorage.setItem('ohmies_token', token);
  },
  removeToken() {
    localStorage.removeItem('ohmies_token');
    localStorage.removeItem('ohmies_user');
  },
  getUser() {
    const raw = localStorage.getItem('ohmies_user');
    return raw ? JSON.parse(raw) : null;
  },
  setUser(user) {
    localStorage.setItem('ohmies_user', JSON.stringify(user));
  },

  // HTTP helper with auth headers & direct backend fallback if proxy fails
  async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    let res;
    try {
      res = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
      });
    } catch (primaryErr) {
      console.warn('Vite proxy connection failed, attempting direct backend connection:', primaryErr);
      try {
        res = await fetch(`${DIRECT_BACKEND_BASE}${endpoint}`, {
          ...options,
          headers,
        });
      } catch (fallbackErr) {
        throw new Error('Backend server is unreachable. Please ensure the backend is running on port 8000.');
      }
    }

    if (res.status === 401) {
      const data = await res.json().catch(() => ({}));
      // Throw error with exact server detail message
      throw new Error(data.detail || 'Invalid UID and Password, pls try again later');
    }

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Server error: ${res.status}`);
    }

    return res.json();
  },

  // Auth endpoints
  async login(userId, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, password }),
    });
    this.setToken(data.access_token);
    this.setUser({
      user_id: data.user_id,
      display_name: data.display_name,
      sector: data.sector,
      subcategory: data.subcategory,
      goal_description: data.goal_description,
    });
    return data;
  },

  async logout() {
    try {
      await this.request('/auth/logout', { method: 'POST' });
    } catch (e) {
      console.warn('Logout notification error:', e);
    } finally {
      this.removeToken();
    }
  },

  async getMe() {
    return this.request('/auth/me');
  },

  // Overview endpoints
  async getOverview(meterId = null) {
    const query = meterId ? `?meter_id=${encodeURIComponent(meterId)}` : '';
    return this.request(`/overview${query}`);
  },

  async listProfiles() {
    return this.request('/overview/profiles');
  },

  // Analytics endpoints (Phase 2)
  async getAnalytics(meterId = null, range = '30d') {
    const params = new URLSearchParams();
    if (meterId) params.append('meter_id', meterId);
    if (range) params.append('range', range);
    return this.request(`/analytics/consumption?${params.toString()}`);
  },

  async getSmartTips(meterId = null) {
    const query = meterId ? `?meter_id=${encodeURIComponent(meterId)}` : '';
    return this.request(`/analytics/tips${query}`);
  },

  async checkHealth() {
    return this.request('/health');
  }
};
