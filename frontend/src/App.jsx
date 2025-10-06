import { useState, useEffect } from 'react';
import { Users, TrendingUp, BarChart3, Plus, Zap, Hash, X } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = {
  getClients: async () => {
    const response = await fetch(`${API_BASE}/clients`);
    if (!response.ok) throw new Error('Failed to fetch clients');
    return response.json();
  },
  
  getTrends: async () => {
    const response = await fetch(`${API_BASE}/trends`);
    if (!response.ok) throw new Error('Failed to fetch trends');
    return response.json();
  },
  
  scanTrends: async (clientId) => {
    const response = await fetch(`${API_BASE}/scan/${clientId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!response.ok) throw new Error('Scan failed');
    return response.json();
  },
  
  deepScan: async (clientId) => {
    const response = await fetch(`${API_BASE}/deep-scan/${clientId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!response.ok) throw new Error('Deep scan failed');
    return response.json();
  },
  
  getHashtags: async (clientId) => {
    const response = await fetch(`${API_BASE}/clients/${clientId}/hashtags`);
    if (!response.ok) throw new Error('Failed to fetch hashtags');
    return response.json();
  },
  
  createClient: async (clientData) => {
    const response = await fetch(`${API_BASE}/clients`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(clientData)
    });
    if (!response.ok) throw new Error('Failed to create client');
    return response.json();
  },
  
  updateClient: async (clientId, clientData) => {
    const response = await fetch(`${API_BASE}/clients/${clientId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(clientData)
    });
    if (!response.ok) throw new Error('Failed to update client');
    return response.json();
  },
  
  generateContent: async (trendId, platform) => {
    const response = await fetch(`${API_BASE}/content/generate?trend_id=${trendId}&platform=${platform}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (!response.ok) throw new Error('Content generation failed');
    return response.json();
  }
};

const StatCard = ({ icon: Icon, label, value, gradient }) => (
  <div style={{
    background: gradient,
    padding: '2rem',
    borderRadius: '1rem',
    color: 'white',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
  }}>
    <Icon size={48} />
    <p style={{ margin: '1rem 0 0', fontSize: '0.875rem', opacity: 0.9 }}>{label}</p>
    <p style={{ fontSize: '3rem', fontWeight: 'bold', margin: 0 }}>{value}</p>
  </div>
);

const WinningPatternsCard = ({ client, patterns, onClose }) => {
  if (!patterns) return null;
  
  let patternData;
  try {
    patternData = typeof patterns === 'string' ? JSON.parse(patterns) : patterns;
  } catch (e) {
    console.error('Error parsing patterns:', e);
    return null;
  }
  
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      borderRadius: '1rem',
      padding: '2rem',
      color: 'white',
      marginBottom: '2rem',
      position: 'relative'
    }}>
      <button 
        onClick={onClose}
        style={{
          position: 'absolute',
          top: '1rem',
          right: '1rem',
          background: 'rgba(255,255,255,0.2)',
          border: 'none',
          borderRadius: '50%',
          width: '2rem',
          height: '2rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          color: 'white'
        }}
      >
        <X size={20} />
      </button>
      
      <h3 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem' }}>
        🎯 Winning Formula for {client.name}
      </h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
        {patternData.best_hook_type && (
          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Best Hook</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', marginTop: '0.5rem' }}>
              {patternData.best_hook_type}
            </div>
          </div>
        )}
        
        {patternData.best_structure && (
          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Structure</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', marginTop: '0.5rem' }}>
              {patternData.best_structure}
            </div>
          </div>
        )}
        
        {patternData.cta_strategy && (
          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>CTA Strategy</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', marginTop: '0.5rem' }}>
              {patternData.cta_strategy}
            </div>
          </div>
        )}
        
        {patternData.optimal_length && (
          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Optimal Length</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', marginTop: '0.5rem' }}>
              {patternData.optimal_length}
            </div>
          </div>
        )}
        
        {patternData.avg_caption_length && (
          <div style={{ background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Avg Length</div>
            <div style={{ fontSize: '1.25rem', fontWeight: '600', marginTop: '0.5rem' }}>
              {patternData.avg_caption_length} chars
            </div>
          </div>
        )}
      </div>
      
      {patternData.emotional_triggers && patternData.emotional_triggers.length > 0 && (
        <div style={{ marginTop: '1rem', background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Emotional Triggers</div>
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
            {patternData.emotional_triggers.map((trigger, i) => (
              <span key={i} style={{
                background: 'rgba(255,255,255,0.2)',
                padding: '0.25rem 0.75rem',
                borderRadius: '9999px',
                fontSize: '0.875rem'
              }}>
                {trigger}
              </span>
            ))}
          </div>
        </div>
      )}
      
      {patternData.content_themes && patternData.content_themes.length > 0 && (
        <div style={{ marginTop: '1rem', background: 'rgba(255,255,255,0.1)', padding: '1rem', borderRadius: '0.5rem' }}>
          <div style={{ fontSize: '0.75rem', opacity: 0.9 }}>Content Themes</div>
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
            {patternData.content_themes.map((theme, i) => (
              <span key={i} style={{
                background: 'rgba(255,255,255,0.2)',
                padding: '0.25rem 0.75rem',
                borderRadius: '9999px',
                fontSize: '0.875rem'
              }}>
                {theme}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const ClientCard = ({ client, onScan, onDeepScan, onViewHashtags, onEdit, onViewPatterns, isScanning }) => (
  <div style={{
    border: '1px solid #e5e7eb',
    borderRadius: '0.75rem',
    padding: '1.5rem',
    background: 'white',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    position: 'relative'
  }}>
    {client.winning_patterns && (
      <div style={{
        position: 'absolute',
        top: '0.5rem',
        right: '0.5rem',
        background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        color: 'white',
        fontSize: '0.75rem',
        padding: '0.25rem 0.5rem',
        borderRadius: '0.25rem',
        fontWeight: '600'
      }}>
        ✨ Analyzed
      </div>
    )}
    
    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
      <div style={{
        width: '3rem',
        height: '3rem',
        borderRadius: '0.5rem',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontWeight: 'bold',
        fontSize: '1.25rem'
      }}>
        {client.name[0].toUpperCase()}
      </div>
      <div style={{ flex: 1 }}>
        <h3 style={{ fontSize: '1.125rem', fontWeight: '600', margin: '0 0 0.25rem 0' }}>
          {client.name}
        </h3>
        <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: 0 }}>
          {client.industry}
        </p>
      </div>
    </div>
    
    {client.winning_patterns && (
      <button 
        onClick={() => onViewPatterns(client)} 
        style={{
          width: '100%',
          background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
          color: 'white',
          padding: '0.75rem',
          borderRadius: '0.5rem',
          border: 'none',
          cursor: 'pointer',
          fontWeight: '600',
          marginBottom: '0.5rem',
          fontSize: '0.875rem'
        }}
      >
        🎯 View Winning Patterns
      </button>
    )}
    
    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
      <button onClick={() => onScan(client.id)} disabled={isScanning} style={{
        flex: 1,
        background: isScanning ? '#9ca3af' : 'linear-gradient(135deg,#f093fb 0%,#f5576c 100%)',
        color: 'white',
        padding: '0.75rem',
        borderRadius: '0.5rem',
        border: 'none',
        cursor: isScanning ? 'not-allowed' : 'pointer',
        fontWeight: '500'
      }}>
        {isScanning ? 'Scanning...' : 'Quick Scan'}
      </button>
      <button onClick={() => onDeepScan(client.id)} disabled={isScanning} style={{
        flex: 1,
        background: isScanning ? '#9ca3af' : 'linear-gradient(135deg,#667eea 0%,#764ba2 100%)',
        color: 'white',
        padding: '0.75rem',
        borderRadius: '0.5rem',
        border: 'none',
        cursor: isScanning ? 'not-allowed' : 'pointer',
        fontWeight: '500',
        fontSize: '0.875rem'
      }}>
        {isScanning ? '⚡' : '🔬'} Deep Scan
      </button>
    </div>
    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
      <button onClick={() => onViewHashtags(client.id)} style={{
        background: 'linear-gradient(135deg,#667eea 0%,#764ba2 100%)',
        color: 'white',
        padding: '0.75rem 1rem',
        borderRadius: '0.5rem',
        border: 'none',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        flex: 1
      }}>
        <Hash size={16} />
        Tags
      </button>
    </div>
    <button onClick={() => onEdit(client)} style={{
      width: '100%',
      background: '#f3f4f6',
      color: '#374151',
      padding: '0.5rem',
      borderRadius: '0.5rem',
      border: '1px solid #e5e7eb',
      cursor: 'pointer',
      fontSize: '0.875rem',
      fontWeight: '500'
    }}>
      Edit Client
    </button>
  </div>
);

const TrendItem = ({ trend, clientName, onGenerateContent }) => {
  const engagement = trend.volume > 50 ? { color: '#10b981', label: 'High' } : 
                     trend.volume > 20 ? { color: '#f59e0b', label: 'Medium' } : 
                     { color: '#6b7280', label: 'Low' };
  const keywords = trend.keywords ? trend.keywords.split(',').slice(0, 5) : [];
  
  return (
    <div style={{
      border: '1px solid #e5e7eb',
      borderRadius: '0.75rem',
      padding: '1.25rem',
      background: 'white',
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <div style={{ flex: 1 }}>
          <span style={{
            background: '#667eea20',
            color: '#667eea',
            padding: '0.25rem 0.5rem',
            borderRadius: '0.25rem',
            fontSize: '0.75rem',
            fontWeight: '600'
          }}>
            #{trend.hashtag}
          </span>
          {clientName && <span style={{ fontSize: '0.75rem', color: '#9ca3af', marginLeft: '0.5rem' }}>{clientName}</span>}
          <p style={{ margin: '0.5rem 0 0', fontSize: '0.95rem', color: '#1f2937' }}>
            {(trend.content || trend.title || '').substring(0, 150)}
          </p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginLeft: '1rem' }}>
          <span style={{
            background: `${engagement.color}20`,
            color: engagement.color,
            padding: '0.25rem 0.75rem',
            borderRadius: '9999px',
            fontSize: '0.75rem',
            fontWeight: '600'
          }}>
            {engagement.label}
          </span>
          <span style={{
            background: '#f3f4f6',
            padding: '0.25rem 0.75rem',
            borderRadius: '9999px',
            fontSize: '0.75rem',
            color: '#6b7280'
          }}>
            {trend.volume}
          </span>
        </div>
      </div>
      {keywords.length > 0 && (
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid #f3f4f6' }}>
          {keywords.map((kw, i) => (
            <span key={i} style={{ background: '#667eea15', color: '#667eea', padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.7rem' }}>
              #{kw.trim()}
            </span>
          ))}
        </div>
      )}
      <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #f3f4f6', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
        <span style={{ fontSize: '0.75rem', color: '#9ca3af', flex: 1 }}>
          {trend.created_at ? new Date(trend.created_at).toLocaleDateString('tr-TR') : 'Recent'}
        </span>
        {trend.url && (
          <a href={trend.url} target="_blank" rel="noopener noreferrer" style={{
            color: '#667eea',
            fontSize: '0.75rem',
            textDecoration: 'none',
            fontWeight: '500'
          }}>
            View Post
          </a>
        )}
        <button 
          onClick={() => onGenerateContent(trend)}
          style={{
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            color: 'white',
            padding: '0.375rem 0.75rem',
            borderRadius: '0.375rem',
            border: 'none',
            fontSize: '0.75rem',
            fontWeight: '500',
            cursor: 'pointer'
          }}
        >
          ✨ Generate Content
        </button>
      </div>
    </div>
  );
};

const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 50 }} onClick={onClose}>
      <div style={{ background: 'white', borderRadius: '1rem', padding: '2rem', width: '90%', maxWidth: '500px', maxHeight: '80vh', overflowY: 'auto' }} onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
};

function App() {
  const [clients, setClients] = useState([]);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [editingClient, setEditingClient] = useState(null);
  const [newClient, setNewClient] = useState({ name: '', industry: '', keywords: '', instagram_url: '' });
  const [generatedContent, setGeneratedContent] = useState(null);
  const [showContentModal, setShowContentModal] = useState(false);
  const [selectedClient, setSelectedClient] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [c, t] = await Promise.all([api.getClients(), api.getTrends()]);
      setClients(c || []);
      setTrends(t || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleScan = async (clientId) => {
    setScanning(prev => ({ ...prev, [clientId]: true }));
    try {
      const result = await api.scanTrends(clientId);
      alert(`Scanned ${result.count} posts`);
      await loadData();
    } catch (error) {
      alert('Error scanning');
    } finally {
      setScanning(prev => ({ ...prev, [clientId]: false }));
    }
  };

  const handleDeepScan = async (clientId) => {
    const confirmed = window.confirm(
      '🔬 Deep Scan Analysis\n\n' +
      'This will:\n' +
      '• Analyze post structures\n' +
      '• Identify winning patterns\n' +
      '• Discover optimal hooks\n' +
      '• Find best content structures\n\n' +
      'Takes 1-2 minutes. Continue?'
    );
    
    if (!confirmed) return;
    
    setScanning(prev => ({ ...prev, [clientId]: true }));
    try {
      const result = await api.deepScan(clientId);
      
      const patternsInfo = result.winning_patterns ? 
        `\n\n📊 Winning Patterns Found:\n` +
        `Hook: ${result.winning_patterns.best_hook_type || 'N/A'}\n` +
        `Structure: ${result.winning_patterns.best_structure || 'N/A'}\n` +
        `Avg Length: ${result.winning_patterns.avg_caption_length || 'N/A'} chars` : '';
      
      alert(
        `✅ Deep Scan Complete!\n\n` +
        `Posts analyzed: ${result.posts_found || 0}` +
        patternsInfo
      );
      await loadData();
    } catch (error) {
      alert('Deep scan failed. Check console for details.');
      console.error(error);
    } finally {
      setScanning(prev => ({ ...prev, [clientId]: false }));
    }
  };

  const handleViewHashtags = async (clientId) => {
    try {
      const data = await api.getHashtags(clientId);
      alert(data.formatted_post);
    } catch (error) {
      alert('Error loading hashtags');
    }
  };

  const handleCreateClient = async () => {
    if (!newClient.name || !newClient.industry) return alert('Fill all fields');
    try {
      if (editingClient) {
        await api.updateClient(editingClient.id, newClient);
      } else {
        await api.createClient(newClient);
      }
      setShowModal(false);
      setEditingClient(null);
      setNewClient({ name: '', industry: '', keywords: '', instagram_url: '' });
      loadData();
    } catch (error) {
      alert(editingClient ? 'Error updating client' : 'Error creating client');
    }
  };

  const handleEditClient = (client) => {
    setEditingClient(client);
    setNewClient({
      name: client.name,
      industry: client.industry,
      keywords: client.keywords || '',
      instagram_url: client.instagram_url || ''
    });
    setShowModal(true);
  };

  const handleGenerateContent = async (trend) => {
    try {
      const result = await api.generateContent(trend.id, 'instagram');
      setGeneratedContent(result.content);
      setShowContentModal(true);
    } catch (error) {
      alert('Error generating content');
    }
  };

  const handleViewPatterns = (client) => {
    setSelectedClient(client);
  };

  if (loading) return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Zap size={48} color="#667eea" /></div>;

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb', fontFamily: 'system-ui' }}>
      <header style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '30px', borderRadius: '20px', margin: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <Zap size={60} color="white" />
          <div>
            <h1 style={{ margin: 0, color: 'white', fontSize: '32px' }}>Othello AI</h1>
            <p style={{ margin: '5px 0 0', color: 'rgba(255,255,255,0.9)' }}>Social Media Intelligence</p>
          </div>
        </div>
      </header>

      <main style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(250px,1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <StatCard icon={Users} label="Clients" value={clients.length} gradient="linear-gradient(135deg,#667eea 0%,#764ba2 100%)" />
          <StatCard icon={TrendingUp} label="Trends" value={trends.length} gradient="linear-gradient(135deg,#f093fb 0%,#f5576c 100%)" />
          <StatCard icon={BarChart3} label="Avg Engagement" value={Math.round(trends.reduce((s, t) => s + (t.volume || 0), 0) / (trends.length || 1))} gradient="linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)" />
        </div>

        {selectedClient && selectedClient.winning_patterns && (
          <WinningPatternsCard 
            client={selectedClient} 
            patterns={selectedClient.winning_patterns}
            onClose={() => setSelectedClient(null)}
          />
        )}

        <div style={{ background: 'white', borderRadius: '1rem', padding: '2rem', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: '600', margin: 0 }}>Clients</h2>
            <button onClick={() => setShowModal(true)} style={{ background: '#2563eb', color: 'white', padding: '0.75rem 1.5rem', borderRadius: '0.5rem', border: 'none', cursor: 'pointer', display: 'flex', gap: '0.5rem' }}>
              <Plus size={20} /> Add
            </button>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(300px,1fr))', gap: '1.5rem' }}>
            {clients.map(c => <ClientCard key={c.id} client={c} onScan={handleScan} onDeepScan={handleDeepScan} onViewHashtags={handleViewHashtags} onEdit={handleEditClient} onViewPatterns={handleViewPatterns} isScanning={scanning[c.id]} />)}
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '1rem', padding: '2rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '1.5rem' }}>Latest Trends</h2>
          <div style={{ display: 'grid', gap: '1rem' }}>
            {trends.map((t, i) => <TrendItem key={i} trend={t} clientName={clients.find(c => c.id === t.client_id)?.name} onGenerateContent={handleGenerateContent} />)}
          </div>
        </div>
      </main>

      <Modal isOpen={showModal} onClose={() => { setShowModal(false); setEditingClient(null); setNewClient({ name: '', industry: '', keywords: '', instagram_url: '' }); }}>
        <h2 style={{ marginBottom: '1.5rem' }}>{editingClient ? 'Edit Client' : 'Add Client'}</h2>
        <input placeholder="Name" value={newClient.name} onChange={e => setNewClient({ ...newClient, name: e.target.value })} style={{ width: '100%', padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: '0.5rem', marginBottom: '1rem', boxSizing: 'border-box' }} />
        <input placeholder="Industry" value={newClient.industry} onChange={e => setNewClient({ ...newClient, industry: e.target.value })} style={{ width: '100%', padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: '0.5rem', marginBottom: '1rem', boxSizing: 'border-box' }} />
        <input placeholder="Keywords" value={newClient.keywords} onChange={e => setNewClient({ ...newClient, keywords: e.target.value })} style={{ width: '100%', padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: '0.5rem', marginBottom: '1rem', boxSizing: 'border-box' }} />
        <input placeholder="Instagram URL (örn: instagram.com/username)" value={newClient.instagram_url} onChange={e => setNewClient({ ...newClient, instagram_url: e.target.value })} style={{ width: '100%', padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: '0.5rem', marginBottom: '1.5rem', boxSizing: 'border-box' }} />
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button onClick={() => { setShowModal(false); setEditingClient(null); setNewClient({ name: '', industry: '', keywords: '', instagram_url: '' }); }} style={{ flex: 1, padding: '0.75rem', border: '1px solid #e5e7eb', borderRadius: '0.5rem', background: 'white', cursor: 'pointer' }}>Cancel</button>
          <button onClick={handleCreateClient} style={{ flex: 1, background: '#2563eb', color: 'white', padding: '0.75rem', borderRadius: '0.5rem', border: 'none', cursor: 'pointer' }}>{editingClient ? 'Update' : 'Create'}</button>
        </div>
      </Modal>

      <Modal isOpen={showContentModal} onClose={() => setShowContentModal(false)}>
        {generatedContent && (
          <>
            <h2 style={{ marginBottom: '1rem' }}>Generated Content for {generatedContent.client_name}</h2>
            <div style={{ background: '#f9fafb', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              <strong>Caption:</strong>
              <p style={{ marginTop: '0.5rem' }}>{generatedContent.caption}</p>
            </div>
            <div style={{ background: '#f9fafb', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              <strong>Hashtags:</strong>
              <p style={{ marginTop: '0.5rem', color: '#667eea' }}>{generatedContent.hashtags}</p>
            </div>
            <div style={{ background: '#f9fafb', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1rem' }}>
              <strong>CTA:</strong>
              <p style={{ marginTop: '0.5rem' }}>{generatedContent.cta}</p>
            </div>
            <p style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
              Inspired by: {generatedContent.inspired_by}
            </p>
            <button onClick={() => navigator.clipboard.writeText(`${generatedContent.caption}\n\n${generatedContent.hashtags}`)} style={{
              width: '100%',
              background: '#10b981',
              color: 'white',
              padding: '0.75rem',
              borderRadius: '0.5rem',
              border: 'none',
              cursor: 'pointer',
              marginTop: '1rem'
            }}>
              📋 Copy to Clipboard
            </button>
          </>
        )}
      </Modal>
    </div>
  );
}

export default App;