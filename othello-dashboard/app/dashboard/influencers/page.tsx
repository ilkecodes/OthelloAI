'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Instagram, Users, Loader2, MessageCircle, Heart, CheckCircle, Save, X } from 'lucide-react';

interface Influencer {
  username: string;
  full_name: string;
  biography: string;
  followers: number;
  posts_count: number;
  engagement_rate: number;
  avg_likes: number;
  avg_comments: number;
  is_verified: boolean;
  profile_pic: string;
  instagram_url: string;
}

export default function InfluencersPage() {
  const [searchInput, setSearchInput] = useState('');
  const [location, setLocation] = useState('');
  const [results, setResults] = useState<Influencer[]>([]);
  const [loading, setLoading] = useState(false);
  const [compareMode, setCompareMode] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const locations = ["İstanbul", "Ankara", "İzmir", "Turkey", "Dubai", "London"];
  
  const examples = [
    { query: "fitness", label: "💪 Fitness" },
    { query: "food", label: "🍕 Food" },
    { query: "travel", label: "✈️ Travel" },
    { query: "beauty", label: "💄 Beauty" }
  ];

  const handleSearch = async () => {
    if (!searchInput) return;
    
    setLoading(true);
    
    try {
      const res = await fetch('/api/influencer-discovery/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          search_query: searchInput,
          location: location || null
        })
      });
      
      const data = await res.json();
      setResults(data.profiles || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (inf: Influencer) => {
    try {
      const res = await fetch('/api/influencer-stats/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: inf.username,
          full_name: inf.full_name,
          followers: inf.followers,
          engagement_rate: inf.engagement_rate,
          notes: ''
        })
      });
      
      const data = await res.json();
      alert(data.message);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const toggleSelect = (username: string) => {
    const newSet = new Set(selected);
    if (newSet.has(username)) {
      newSet.delete(username);
    } else {
      if (newSet.size < 3) {
        newSet.add(username);
      } else {
        alert('Maksimum 3 influencer seçebilirsiniz!');
      }
    }
    setSelected(newSet);
  };

  const getSelectedInfluencers = () => {
    return results.filter(inf => selected.has(inf.username));
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Influencer Keşfi</h1>
          <p className="text-gray-600">Instagram influencer arama</p>
        </div>
        {results.length > 0 && (
          <Button
            variant={compareMode ? 'default' : 'outline'}
            onClick={() => setCompareMode(!compareMode)}
          >
            {compareMode ? `Karşılaştır (${selected.size})` : 'Karşılaştırma Modu'}
          </Button>
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Ara</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Konu *</label>
              <Input
                placeholder="Örn: fitness, food, travel"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">Konum (Opsiyonel)</label>
              <select
                className="w-full p-2 border rounded"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              >
                <option value="">Tüm Konumlar</option>
                {locations.map((loc) => (
                  <option key={loc} value={loc}>{loc}</option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <Button 
                onClick={handleSearch} 
                disabled={loading || !searchInput}
                className="w-full"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
                {loading ? 'Aranıyor...' : 'Ara'}
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-4 gap-2">
            {examples.map((ex, idx) => (
              <button
                key={idx}
                onClick={() => setSearchInput(ex.query)}
                className="text-sm p-2 rounded border hover:bg-gray-50"
              >
                {ex.label}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Karşılaştırma Paneli */}
      {compareMode && selected.size > 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle>Karşılaştırma ({selected.size}/3)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              {getSelectedInfluencers().map(inf => (
                <div key={inf.username} className="bg-white p-4 rounded-lg relative">
                  <button
                    onClick={() => toggleSelect(inf.username)}
                    className="absolute top-2 right-2 text-gray-400 hover:text-red-500"
                  >
                    <X className="h-4 w-4" />
                  </button>
                  <div className="flex items-center gap-2 mb-3">
                    <img src={inf.profile_pic} alt={inf.username} className="w-12 h-12 rounded-full" />
                    <div>
                      <p className="font-semibold text-sm">{inf.full_name}</p>
                      <p className="text-xs text-gray-500">@{inf.username}</p>
                    </div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Takipçi:</span>
                      <span className="font-semibold">{formatNumber(inf.followers)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Engagement:</span>
                      <span className="font-semibold text-green-600">{inf.engagement_rate}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Avg Likes:</span>
                      <span className="font-semibold">{formatNumber(inf.avg_likes)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {loading && (
        <div className="text-center py-12">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Instagram taranıyor...</p>
          <p className="text-sm text-gray-400 mt-2">Bu 1-2 dakika sürebilir</p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>{results.length} Influencer Bulundu</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              {results.map((inf, idx) => (
                <Card 
                  key={idx} 
                  className={`hover:shadow-lg transition ${
                    compareMode && selected.has(inf.username) ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => compareMode && toggleSelect(inf.username)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start gap-3">
                      {inf.profile_pic && (
                        <img src={inf.profile_pic} alt={inf.username} className="w-16 h-16 rounded-full" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1">
                          <CardTitle className="text-sm truncate">{inf.full_name || inf.username}</CardTitle>
                          {inf.is_verified && <CheckCircle className="h-4 w-4 text-blue-500" />}
                        </div>
                        <p className="text-xs text-gray-500">@{inf.username}</p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <p className="text-xs text-gray-600 line-clamp-2">{inf.biography}</p>
                    
                    <div className="grid grid-cols-3 gap-2 text-center text-xs">
                      <div>
                        <p className="font-bold text-blue-600">{formatNumber(inf.followers)}</p>
                        <p className="text-gray-500">Takipçi</p>
                      </div>
                      <div>
                        <p className="font-bold text-green-600">{inf.engagement_rate}%</p>
                        <p className="text-gray-500">Eng.</p>
                      </div>
                      <div>
                        <p className="font-bold text-purple-600">{inf.posts_count}</p>
                        <p className="text-gray-500">Post</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-1">
                        <Heart className="h-3 w-3 text-red-500" />
                        <span>{formatNumber(inf.avg_likes)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <MessageCircle className="h-3 w-3 text-blue-500" />
                        <span>{inf.avg_comments}</span>
                      </div>
                    </div>

                    {!compareMode && (
                      <div className="flex gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          className="flex-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            window.open(inf.instagram_url, '_blank');
                          }}
                        >
                          <Instagram className="h-3 w-3 mr-1" />
                          Profil
                        </Button>
                        <Button
                          size="sm"
                          className="flex-1"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleSave(inf);
                          }}
                        >
                          <Save className="h-3 w-3 mr-1" />
                          Kaydet
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
