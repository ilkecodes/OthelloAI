'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Search, TrendingUp, Lightbulb, Target, Hash, Clock,
  Zap, BarChart3, Sparkles, Music, Globe, Trophy, 
  Loader2, RefreshCw, Film, PlayCircle, Award
} from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ContentType {
  type: string;
  percentage: number;
  avg_engagement: number;
  description: string;
  emoji: string;
}

export default function TrendsPage() {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchResult, setSearchResult] = useState<any>(null);

  const examples = [
    "yemek tarifi videolu",
    "fitness motivasyon",
    "moda kombini",
    "teknoloji haberleri"
  ];

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/trends/dashboard`);
      const data = await res.json();
      if (data.success) {
        setDashboardData(data.data);
      }
    } catch (error) {
      console.error('Dashboard error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setSearchLoading(true);
    setSearchResult(null);
    
    try {
      const res = await fetch(`${API_URL}/api/trends/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery })
      });
      
      const data = await res.json();
      if (data.success) {
        setSearchResult(data.result);
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Arama hatası!');
    } finally {
      setSearchLoading(false);
    }
  };

  const getContentTypeColor = (percentage: number) => {
    if (percentage >= 40) return 'from-green-500 to-emerald-600';
    if (percentage >= 25) return 'from-blue-500 to-cyan-600';
    return 'from-purple-500 to-pink-600';
  };

  const getCategoryColor = (category: string) => {
    const colors: {[key: string]: string} = {
      'food': 'bg-orange-100 text-orange-800',
      'fashion': 'bg-pink-100 text-pink-800',
      'fitness': 'bg-green-100 text-green-800',
      'beauty': 'bg-purple-100 text-purple-800',
      'travel': 'bg-blue-100 text-blue-800',
      'tech': 'bg-gray-100 text-gray-800',
      'entertainment': 'bg-yellow-100 text-yellow-800',
      'lifestyle': 'bg-teal-100 text-teal-800',
      'gaming': 'bg-indigo-100 text-indigo-800',
      'genel': 'bg-slate-100 text-slate-800',
      'türkiye': 'bg-red-100 text-red-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">🔥 Trend Analiz Dashboard</h1>
          <p className="text-gray-600">Google Trends + TikTok + İçerik Türü Analizi</p>
        </div>
        <Button variant="outline" onClick={loadDashboard} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Yenile
        </Button>
      </div>

      {/* Search Bar */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="Niş trend aramak için yazın... (örn: yemek tarifi videolu)"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1 h-12 text-lg"
              />
              <Button 
                onClick={handleSearch} 
                disabled={searchLoading || !searchQuery.trim()}
                size="lg"
                className="px-8"
              >
                {searchLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Search className="h-5 w-5" />}
              </Button>
            </div>

            <div className="flex flex-wrap gap-2">
              {examples.map((ex, idx) => (
                <button
                  key={idx}
                  onClick={() => setSearchQuery(ex)}
                  className="text-sm px-3 py-1.5 rounded-full bg-white border hover:bg-gray-50 transition"
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Loading */}
      {searchLoading && (
        <Card>
          <CardContent className="py-12">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
              <p className="font-semibold">Trend analizi yapılıyor...</p>
              <p className="text-sm text-gray-500 mt-2">Google + TikTok + İçerik türleri analiz ediliyor...</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* SEARCH RESULTS */}
      {searchResult && !searchLoading && (
        <div className="space-y-6">
          {/* Niche Detection */}
          <Card className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                Niş Tespiti
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-gray-600 mb-2">Ana Niş</p>
                  <Badge className="text-lg px-4 py-2">{searchResult.niche.niche}</Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-2">Alt Kategori</p>
                  <Badge variant="outline" className="text-lg px-4 py-2">{searchResult.niche.sub_niche}</Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-2">Açıklama</p>
                  <p className="text-sm">{searchResult.niche.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Content Types */}
          {searchResult.content_types && (
            <Card className="bg-gradient-to-r from-orange-50 to-yellow-50 border-orange-200">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Film className="h-5 w-5 text-orange-600" />
                  En Trend İçerik Türleri
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Top Performer */}
                <div className="bg-white rounded-lg p-4 border-2 border-orange-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 text-white text-2xl">
                      {searchResult.content_types.top_performing_type.emoji}
                    </div>
                    <div>
                      <p className="text-xs text-gray-600">🏆 En Yüksek Performans</p>
                      <p className="font-bold text-lg">{searchResult.content_types.top_performing_type.description}</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 mt-3">
                    <div className="text-center p-2 bg-orange-50 rounded">
                      <p className="text-2xl font-bold text-orange-600">
                        %{searchResult.content_types.top_performing_type.percentage}
                      </p>
                      <p className="text-xs text-gray-600">Oran</p>
                    </div>
                    <div className="text-center p-2 bg-green-50 rounded">
                      <p className="text-2xl font-bold text-green-600">
                        {searchResult.content_types.top_performing_type.avg_engagement}x
                      </p>
                      <p className="text-xs text-gray-600">Avg Engagement</p>
                    </div>
                  </div>
                </div>

                {/* Distribution */}
                <div className="space-y-3">
                  <p className="font-semibold text-sm">İçerik Türü Dağılımı:</p>
                  {searchResult.content_types.content_types.distribution.map((ct: ContentType, idx: number) => (
                    <div key={idx} className="bg-white rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="text-2xl">{ct.emoji}</span>
                          <div>
                            <p className="font-semibold text-sm">{ct.description}</p>
                            <p className="text-xs text-gray-500">{ct.type}</p>
                          </div>
                        </div>
                        <Badge className="text-lg px-3 py-1">{ct.percentage}%</Badge>
                      </div>
                      
                      <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className={`h-full bg-gradient-to-r ${getContentTypeColor(ct.percentage)} transition-all duration-500`}
                          style={{ width: `${ct.percentage}%` }}
                        />
                      </div>
                      
                      <div className="flex items-center justify-between mt-2 text-xs text-gray-600">
                        <span>Ortalama Engagement:</span>
                        <span className="font-semibold text-green-600">{ct.avg_engagement}x</span>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Insights */}
                {searchResult.content_types.content_types.insights && (
                  <div className="bg-blue-50 rounded-lg p-4">
                    <p className="font-semibold text-sm mb-2 flex items-center gap-2">
                      <Lightbulb className="h-4 w-4 text-blue-600" />
                      İçgörüler
                    </p>
                    <div className="space-y-1">
                      {searchResult.content_types.content_types.insights.map((insight: string, idx: number) => (
                        <p key={idx} className="text-sm text-gray-700">• {insight}</p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommendations */}
                {searchResult.content_types.recommendations && (
                  <div className="bg-green-50 rounded-lg p-4">
                    <p className="font-semibold text-sm mb-2 flex items-center gap-2">
                      <Award className="h-4 w-4 text-green-600" />
                      Öneriler
                    </p>
                    <div className="space-y-1">
                      {searchResult.content_types.recommendations.map((rec: string, idx: number) => (
                        <p key={idx} className="text-sm text-gray-700">✓ {rec}</p>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Ranked Trends */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="h-5 w-5 text-yellow-600" />
                Top Trendler
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {searchResult.ranked_trends.slice(0, 10).map((trend: any, idx: number) => (
                  <div key={idx} className="flex items-center gap-4 p-4 border rounded-lg hover:bg-gray-50 transition">
                    <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 text-white font-bold">
                      {trend.overall_rank}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-semibold">{trend.keyword}</span>
                        <Badge variant="outline" className="text-xs">{trend.source}</Badge>
                        <span className="text-xl">{trend.growth}</span>
                      </div>
                      
                      {trend.tiktok_views && (
                        <p className="text-sm text-gray-600">
                          {trend.tiktok_views} views • {trend.tiktok_posts?.toLocaleString()} posts
                        </p>
                      )}
                    </div>
                    
                    <div className="text-right">
                      <div className="text-2xl font-bold text-purple-600">{trend.score}</div>
                      <div className="text-xs text-gray-500">skor</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* AI Insights */}
          {searchResult.ai_insights && (
            <Card className="bg-gradient-to-r from-blue-50 to-cyan-50 border-blue-200">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-blue-600" />
                  AI İçgörüler ve Öneriler
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Summary */}
                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold mb-2 flex items-center gap-2">
                    <BarChart3 className="h-4 w-4" />
                    Özet
                  </p>
                  <p className="text-sm text-gray-700">{searchResult.ai_insights.summary}</p>
                </div>

                {/* Opportunities */}
                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold mb-3 flex items-center gap-2">
                    <Zap className="h-4 w-4 text-yellow-600" />
                    Fırsatlar
                  </p>
                  <div className="space-y-2">
                    {searchResult.ai_insights.opportunities.map((opp: string, idx: number) => (
                      <div key={idx} className="flex items-start gap-2">
                        <span className="text-yellow-600">💡</span>
                        <p className="text-sm">{opp}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Content Ideas */}
                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold mb-3 flex items-center gap-2">
                    <Lightbulb className="h-4 w-4 text-purple-600" />
                    İçerik Fikirleri
                  </p>
                  <div className="space-y-3">
                    {searchResult.ai_insights.content_ideas.map((idea: any, idx: number) => (
                      <div key={idx} className="border-l-4 border-purple-500 pl-3 py-2">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="outline">{idea.type}</Badge>
                          <span className="font-semibold text-sm">{idea.title}</span>
                        </div>
                        <p className="text-sm text-gray-700">{idea.description}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Hashtags */}
                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold mb-3 flex items-center gap-2">
                    <Hash className="h-4 w-4 text-blue-600" />
                    Önerilen Hashtag'ler
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {searchResult.ai_insights.hashtag_recommendations.map((tag: string, idx: number) => (
                      <Badge key={idx} className="text-sm px-3 py-1">{tag}</Badge>
                    ))}
                  </div>
                </div>

                {/* Best Time */}
                <div className="bg-white rounded-lg p-4">
                  <p className="font-semibold mb-2 flex items-center gap-2">
                    <Clock className="h-4 w-4 text-green-600" />
                    En İyi Paylaşım Zamanı
                  </p>
                  <Badge className="bg-green-100 text-green-800 text-sm px-3 py-1">
                    {searchResult.ai_insights.best_time === 'morning' ? '🌅 Sabah (8-11)' :
                     searchResult.ai_insights.best_time === 'afternoon' ? '☀️ Öğleden Sonra (12-17)' :
                     '🌙 Akşam (18-22)'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Dashboard */}
      {!searchResult && !searchLoading && !loading && dashboardData && (
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5 text-blue-600" />
                Google Trends
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dashboardData.google_trends?.slice(0, 10).map((trend: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{trend.trend_emoji}</span>
                      <div>
                        <p className="font-semibold">{trend.keyword}</p>
                        <Badge className={`text-xs ${getCategoryColor(trend.category)}`}>
                          {trend.category}
                        </Badge>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-blue-600">{trend.interest}</div>
                      <div className="text-xs text-gray-500">/100</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Music className="h-5 w-5 text-pink-600" />
                TikTok Trends
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dashboardData.tiktok_trends?.slice(0, 10).map((trend: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-pink-500 to-purple-600 text-white text-xs font-bold flex items-center justify-center">
                        {trend.rank}
                      </div>
                      <div>
                        <p className="font-semibold">#{trend.hashtag}</p>
                        <Badge className={`text-xs ${getCategoryColor(trend.category)}`}>
                          {trend.category}
                        </Badge>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-pink-600">{trend.views}</div>
                      <div className="text-xs text-gray-500">{trend.growth}</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {loading && !searchLoading && (
        <div className="text-center py-12">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto" />
        </div>
      )}
    </div>
  );
}
