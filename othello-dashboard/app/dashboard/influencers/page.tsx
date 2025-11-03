'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Instagram, Users, Loader2, MessageCircle, Heart, CheckCircle } from 'lucide-react';

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
  const [results, setResults] = useState<Influencer[]>([]);
  const [loading, setLoading] = useState(false);

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
      const res = await fetch('http://localhost:8000/api/influencer-discovery/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ search_query: searchInput })
      });
      
      const data = await res.json();
      setResults(data.profiles || []);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Influencer Keşfi</h1>
        <p className="text-gray-600">Instagram influencer arama</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Ara</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="Örn: fitness, food, travel"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <Button onClick={handleSearch} disabled={loading || !searchInput}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            </Button>
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

      {loading && (
        <div className="text-center py-12">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Aranıyor...</p>
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
                <Card key={idx} className="hover:shadow-lg transition">
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
                        <p className="text-gray-500">Engagement</p>
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

                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full"
                      onClick={() => window.open(inf.instagram_url, '_blank')}
                    >
                      <Instagram className="h-3 w-3 mr-1" />
                      Instagram
                    </Button>
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
