import axios from 'axios';

// Client-side'da çalışacak
const getApiUrl = () => {
  // Production Vercel
  if (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')) {
    return 'https://othello-backend-production-2ff4.up.railway.app';
  }
  
  // Environment variable
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // Local fallback
  return 'http://localhost:8000';
};

const api = axios.create({
  baseURL: getApiUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Her request'te baseURL'i güncelle (client-side için)
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')) {
    config.baseURL = 'https://othello-backend-production-2ff4.up.railway.app';
  }
  console.log('🚀 Request to:', config.baseURL + config.url);
  return config;
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
