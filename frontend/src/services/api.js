const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getClients = async () => {
  const response = await fetch(`${API_URL}/clients/`);
  if (!response.ok) throw new Error('Failed to fetch clients');
  return response.json();
};

export const createClient = async (clientData) => {
  const response = await fetch(`${API_URL}/clients/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clientData)
  });
  if (!response.ok) throw new Error('Failed to create client');
  return response.json();
};

export const scanTrends = async (clientId) => {
  const response = await fetch(`${API_URL}/trends/scan?client_id=${clientId}`, {
    method: 'POST'
  });
  if (!response.ok) throw new Error('Failed to scan trends');
  return response.json();
};

export const getTrends = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.client_id) params.append('client_id', filters.client_id);
  if (filters.platform) params.append('platform', filters.platform);
  if (filters.limit) params.append('limit', filters.limit);
  
  const response = await fetch(`${API_URL}/trends/?${params}`);
  if (!response.ok) throw new Error('Failed to fetch trends');
  return response.json();
};

export const getHashtags = async (clientId) => {
  const response = await fetch(`${API_URL}/clients/${clientId}/hashtags`);
  if (!response.ok) throw new Error('Failed to fetch hashtags');
  return response.json();
};

export const getTrendStats = async (clientId = null) => {
  const params = clientId ? `?client_id=${clientId}` : '';
  const response = await fetch(`${API_URL}/trends/stats${params}`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
};
export const updateClient = async (clientId, clientData) => {
  const response = await fetch(`${API_URL}/clients/${clientId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clientData)
  });
  if (!response.ok) throw new Error('Failed to update client');
  return response.json();
};
export const deepScan = async (clientId) => {
  const response = await fetch(`${API_URL}/trends/scan-deep?client_id=${clientId}`, {
    method: 'POST'
  });
  if (!response.ok) throw new Error('Deep scan failed');
  return response.json();
};