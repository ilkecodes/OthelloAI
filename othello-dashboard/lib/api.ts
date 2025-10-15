import axios from 'axios';

// PRODUCTION URL - hardcoded
const API_URL = typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')
  ? 'https://othello-backend-production-2ff4.up.railway.app'
  : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

console.log('🔍 API_URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getClients = () => api.get('/api/clients');
export const createClient = (data: any) => api.post('/api/clients', data);
export const deleteClient = (id: string) => api.delete(`/api/clients/${id}`);
export const generateContent = (data: any) => api.post('/api/content/generate', data);
export const scanTrends = (data: any) => api.post('/api/trends/scan', data);
export const getClientTrends = (clientId: string) => api.get(`/api/trends/client/${clientId}`);
export const getTopTrends = () => api.get('/api/trends/top');
export const searchInfluencers = (data: any) => api.post('/api/influencers/search', data);
export const getCampaigns = () => api.get('/api/campaigns');
export const createCampaign = (data: any) => api.post('/api/campaigns', data);

export default api;
