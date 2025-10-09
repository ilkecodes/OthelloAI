import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Clients
export const getClients = () => api.get('/api/clients');
export const createClient = (data: any) => api.post('/api/clients', data);
export const deleteClient = (id: string) => api.delete(`/api/clients/${id}`);

// Content
export const generateContent = (data: any) => api.post('/api/content/generate', data);

// Trends
export const scanTrends = (data: any) => api.post('/api/trends/scan', data);
export const getClientTrends = (clientId: string) => api.get(`/api/trends/client/${clientId}`);
export const getTopTrends = () => api.get('/api/trends/top');

// Influencers
export const searchInfluencers = (data: any) => api.post('/api/influencers/search', data);

// Campaigns
export const getCampaigns = () => api.get('/api/campaigns');
export const createCampaign = (data: any) => api.post('/api/campaigns', data);

export default api;
