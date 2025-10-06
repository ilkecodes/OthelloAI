import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Clients
export const getClients = () => api.get('/api/clients/');
export const getClient = (id: string) => api.get(`/api/clients/${id}`);

// Trends
export const scanTrends = (data: any) => api.post('/api/trends/scan', data);
export const getClientTrends = (clientId: string) => api.get(`/api/trends/client/${clientId}`);
export const getTopTrends = (clientId: string) => api.get(`/api/trends/top/${clientId}`);

// Content
export const generateContent = (data: any) => api.post('/api/content/generate', data);
export const getContent = () => api.get('/api/content/');

// Campaigns
export const getCampaigns = () => api.get('/api/campaigns/');
export const createCampaign = (data: any) => api.post('/api/campaigns/', data);
export const getCampaign = (id: string) => api.get(`/api/campaigns/${id}`);

// Influencers
export const searchInfluencers = (data: any) => api.post('/api/campaign-influencer/search-for-campaign', data);
export const getInfluencers = () => api.get('/api/influencers/');
