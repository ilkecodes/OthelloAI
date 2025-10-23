// lib/api.ts
import axios from 'axios';

export const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  'https://othello-backend-production-2ff4.up.railway.app';

const api = axios.create({
  baseURL: BACKEND_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Clients
export const getClients = () => api.get('/api/clients/');       // ✅ trailing slash
export const createClient = (data: any) => api.post('/api/clients/', data);
export const deleteClient = (id: string) => api.delete(`/api/clients/${id}`); // ✅ no trailing slash

// Content (eski içerik üretici akışı)
export const generateContent = (data: any) => api.post('/api/content/generate', data);

// Trends
export const scanTrends = (data: any) => api.post('/api/trends/scan', data);
export const getClientTrends = (clientId: string) => api.get(`/api/trends/client/${clientId}`);
// export const getTopTrends = () => api.get('/api/trends/top'); // ❌ backend’de yok → kaldır

// Influencers
export const searchInfluencers = (data: any) => api.post('/api/influencers/search', data);

// Campaigns
export const getCampaigns = () => api.get('/api/campaigns/');    // ✅ trailing slash
export const createCampaign = (data: any) => api.post('/api/campaigns/', data);

// Brand Voice (yeni akış)
export const generateFromUrl = (data: any) => api.post('/api/brand-voice/generate-from-url', data);
export const getBrandVoice = (clientId: string) => api.get(`/api/brand-voice/get/${clientId}`);
export const getBrandVoiceStats = (clientId: string) => api.get(`/api/brand-voice/stats/${clientId}`);

export default api;

