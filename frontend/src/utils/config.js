// API configuration
// VITE_API_URL is used in production; fall back to VITE_API_BASE_URL for legacy setups.
export const API_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';