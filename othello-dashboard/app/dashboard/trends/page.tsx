'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { scanTrends, getClients } from '@/lib/api';
import { TrendingUp, BarChart3, Hash, Users, Activity, Lightbulb, Calendar, Award, Zap, Target, AlertCircle, Globe } from 'lucide-react';

const clientSuggestions: Record<string, string[]> = {
  'Healthcare': ['health', 'wellness', 'ivf', 'pregnancy', 'fertility', 'gynecology', 'women', 'medical'],
  'Restaurant': ['food', 'dining', 'cyprus', 'restaurant', 'meyhane', 'livemusic', 'chef', 'foodie'],
  'Food & Beverage': ['dessert', 'sweet', 'coffee', 'pastry', 'cafe', 'baklava', 'chocolate', 'cake'],
  'Food': ['baklava', 'turkish', 'dessert', 'homemade', 'traditional', 'sweet', 'pastry'],
  'Entertainment': ['dj', 'party', 'nightlife', 'event', 'music', 'cyprus', 'weekend', 'dance'],
  'Digital Marketing': ['marketing', 'seo', 'digital', 'branding', 'socialmedia', 'content', 'ads'],
  'E-commerce': ['shopping', 'online', 'electronics', 'deals', 'Cyprus', 'sale', 'discount'],
  'Real Estate': ['realestate', 'property', 'villa', 'home', 'cyprus', 'modern', 'luxury', 'apartment']
};

const trendCategories = [
  { id: 'hot', label: 'Sıcak Trendler', color: 'red', minScore: 0.08, icon: '🔥' },
  { id: 'rising', label: 'Yükselen', color: 'orange', minScore: 0.05, icon: '📈' },
  { id: 'stable', label: 'Stabil', color: 'blue', minScore: 0.03, icon: '📊' },
  { id: 'emerging', label: 'Gelişen', color: 'green', minScore: 0, icon: '🌱' }
];

const popularTopics = [
  { category: 'Teknoloji', keywords: ['ai', 'tech', 'innovation', 'future', 'digital'] },
  { category: 'Sağlık', keywords: ['health', 'wellness', 'fitness', 'nutrition', 'yoga'] },
  { category: 'Moda', keywords: ['fashion', 'style', 'outfit', 'trends', 'ootd'] },
  { category: 'Yemek', keywords: ['food', 'recipe', 'cooking', 'chef', 'foodie'] },
  { category: 'Seyahat', keywords: ['travel', 'vacation', 'adventure', 'explore', 'wanderlust'] },
  { category: 'Güzellik', keywords: ['beauty', 'skincare', 'makeup', 'cosmetics', 'glow'] }
];

export default function TrendsPage() {
  const [clients, setClients] = useState<any[]>([]);
  const [scanMode, setScanMode] = useState<'client' | 'general'>('client');
  const [clientId, setClientId] = useState('');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState('scan');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  useEffect(() => {
    getClients().then(res => setClients(res.data)).catch(console.error);
  }, []);

  const selectedClient = clients.find(c => c.id === clientId);

  useEffect(() => {
    if (scanMode === 'client' && selectedClient) {
      const industry = selectedClient.brand_guidelines?.industry || '';
      const clientKeywords = selectedClient.keywords?.keywords || [];
      const industrySuggestions = clientSuggestions[industry] || [];
      
      const allSuggestions = [...new Set([...clientKeywords, ...industrySuggestions])];
      setSuggestions(allSuggestions);
      
      if (!keywords) {
        setKeywords(allSuggestions.slice(0, 3).join(', '));
      }
    }
  }, [selectedClient, scanMode]);

  const handleScan = async () => {
    if ((scanMode === 'client' && !clientId) || !keywords) return;
    setLoading(true);
    try {
      const res = await scanTrends({
        client_id: scanMode === 'client' ? clientId : 'general',
        keywords: keywords.split(',').map(k => k.trim()),
        limit: 30
      });
      setResults(res.data);
      setHistory(prev => [{...res.data, mode: scanMode}, ...prev.slice(0, 4)]);
    } catch (error) {
      console.error('Trend taraması hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const addSuggestion = (keyword: string) => {
    const currentKeywords = keywords.split(',').map(k => k.trim()).filter(k => k);
    if (!currentKeywords.includes(keyword)) {
      setKeywords([...currentKeywords, keyword].join(', '));
    }
  };

  const categorizeTrend = (score: number) => {
    if (score >= 0.08) return trendCategories[0];
    if (score >= 0.05) return trendCategories[1];
    if (score >= 0.03) return trendCategories[2];
    return trendCategories[3];
  };

  const filteredTrends = results?.trends?.filter((t: any) => {
    if (selectedCategory === 'all') return true;
    const category = categorizeTrend(t.trending_score);
    return category.id === selectedCategory;
  }) || [];

  const getTrendInsight = (trend: any) => {
    const category = categorizeTrend(trend.trending_score);
    if (category.id === 'hot') return 'Şimdi paylaşım yapmak için ideal! 🔥';
    if (category.id === 'rising') return 'Yakında popüler olabilir! 📈';
    if (category.id === 'stable') return 'Güvenilir bir konu 📊';
    return 'Yeni bir fırsat olabilir 🌱';
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Trend Tarama</h1>
        <p className="text-slate-600">Instagram hashtag analizi ile güncel trendleri keşfedin</p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="scan">🔍 Yeni Tarama</TabsTrigger>
          <TabsTrigger value="history">📊 Geçmiş</TabsTrigger>
          <TabsTrigger value="insights">💡 Öneriler</TabsTrigger>
        </TabsList>

        <TabsContent value="scan" className="space-y-6">
          {/* Tarama Modu Seçimi */}
          <div className="flex gap-4">
            <Button
              variant={scanMode === 'client' ? 'default' : 'outline'}
              onClick={() => setScanMode('client')}
              className="flex-1"
            >
              <Users className="mr-2 h-4 w-4" />
              Müşteri Bazlı Tarama
            </Button>
            <Button
              variant={scanMode === 'general' ? 'default' : 'outline'}
              onClick={() => setScanMode('general')}
              className="flex-1"
            >
              <Globe className="mr-2 h-4 w-4" />
              Genel Trend Tarama
            </Button>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Hash className="h-5 w-5" />
                  {scanMode === 'client' ? 'Müşteri Trend Taraması' : 'Genel Trend Tarama'}
                </CardTitle>
                <CardDescription>
                  {scanMode === 'client' 
                    ? 'Müşteri seçin ve keyword\'leri girin'
                    : 'Herhangi bir konuda trend taraması yapın'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {scanMode === 'client' ? (
                  <>
                    <div>
                      <label className="text-sm font-medium mb-2 block">Müşteri Seçin</label>
                      <Select value={clientId} onValueChange={setClientId}>
                        <SelectTrigger>
                          <SelectValue placeholder="Müşteri seçin" />
                        </SelectTrigger>
                        <SelectContent>
                          {clients.map(client => (
                            <SelectItem key={client.id} value={client.id}>
                              {client.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    {selectedClient && suggestions.length > 0 && (
                      <div className="p-3 bg-slate-50 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                          <Lightbulb className="h-4 w-4 text-amber-600" />
                          <p className="text-xs font-medium">Önerilen Keyword'ler</p>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {suggestions.map((kw, i) => (
                            <button
                              key={i}
                              onClick={() => addSuggestion(kw)}
                              className="text-xs px-2 py-1 bg-white border rounded hover:bg-slate-100"
                            >
                              #{kw}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="p-4 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg space-y-3">
                    <div className="flex items-center gap-2 mb-2">
                      <Globe className="h-5 w-5 text-blue-600" />
                      <p className="font-medium">Popüler Kategoriler</p>
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      {popularTopics.map((topic, i) => (
                        <button
                          key={i}
                          onClick={() => setKeywords(topic.keywords.slice(0, 3).join(', '))}
                          className="p-2 bg-white rounded-lg hover:shadow-md transition text-left"
                        >
                          <p className="text-sm font-medium">{topic.category}</p>
                          <p className="text-xs text-slate-600">
                            #{topic.keywords[0]}, #{topic.keywords[1]}
                          </p>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <label className="text-sm font-medium mb-2 block">Keywords (virgülle ayırın)</label>
                  <Input 
                    placeholder="health, wellness, fitness"
                    value={keywords}
                    onChange={(e) => setKeywords(e.target.value)}
                  />
                  <p className="text-xs text-slate-500 mt-1">
                    İngilizce keyword'ler daha iyi sonuç verir
                  </p>
                </div>

                <Button 
                  onClick={handleScan} 
                  disabled={loading || (scanMode === 'client' && !clientId) || !keywords}
                  className="w-full"
                >
                  {loading ? (
                    <>
                      <Activity className="mr-2 h-4 w-4 animate-spin" />
                      Taranıyor...
                    </>
                  ) : (
                    <>
                      <TrendingUp className="mr-2 h-4 w-4" />
                      Tara
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Tarama Özeti
                </CardTitle>
              </CardHeader>
              <CardContent>
                {results ? (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 bg-blue-50 rounded-lg">
                        <p className="text-sm text-blue-600">
                          {scanMode === 'client' ? 'Müşteri' : 'Mod'}
                        </p>
                        <p className="text-lg font-bold text-blue-900 truncate">
                          {scanMode === 'client' ? results.client : 'Genel Tarama'}
                        </p>
                      </div>
                      <div className="p-4 bg-green-50 rounded-lg">
                        <p className="text-sm text-green-600">Trend Sayısı</p>
                        <p className="text-2xl font-bold text-green-900">{results.trends_found}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-2">
                      {trendCategories.map(cat => {
                        const count = results.trends?.filter((t: any) => 
                          categorizeTrend(t.trending_score).id === cat.id
                        ).length || 0;
                        return (
                          <div key={cat.id} className="p-2 bg-slate-50 rounded-lg text-center">
                            <p className="text-xs text-slate-600">{cat.icon} {cat.label}</p>
                            <p className="text-xl font-bold">{count}</p>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8 text-slate-400">
                    <TrendingUp className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>Henüz tarama yapılmadı</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {results && results.trends && results.trends.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">Trend Sonuçları</h2>
                <div className="flex gap-2">
                  <Button
                    variant={selectedCategory === 'all' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedCategory('all')}
                  >
                    Tümü ({results.trends.length})
                  </Button>
                  {trendCategories.map(cat => {
                    const count = results.trends.filter((t: any) => 
                      categorizeTrend(t.trending_score).id === cat.id
                    ).length;
                    return count > 0 && (
                      <Button
                        key={cat.id}
                        variant={selectedCategory === cat.id ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setSelectedCategory(cat.id)}
                      >
                        {cat.icon} ({count})
                      </Button>
                    );
                  })}
                </div>
              </div>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredTrends.map((trend: any, i: number) => {
                  const category = categorizeTrend(trend.trending_score);
                  return (
                    <Card key={i} className="hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <Badge className="w-fit mb-2">
                          {category.icon} {category.label}
                        </Badge>
                        <CardTitle className="text-lg flex items-center gap-2">
                          <Hash className="h-5 w-5 text-pink-600" />
                          {trend.keyword}
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="grid grid-cols-2 gap-2">
                            <div className="p-2 bg-slate-50 rounded text-center">
                              <p className="text-xs text-slate-600">Posts</p>
                              <p className="text-lg font-bold">{trend.post_count}</p>
                            </div>
                            <div className="p-2 bg-blue-50 rounded text-center">
                              <p className="text-xs text-blue-600">Engagement</p>
                              <p className="text-lg font-bold text-blue-900">
                                {trend.avg_engagement?.toFixed(1)}
                              </p>
                            </div>
                          </div>

                          <div className="p-2 bg-purple-50 rounded text-center">
                            <p className="text-xs text-purple-600">Trend Score</p>
                            <p className="text-xl font-bold text-purple-900">
                              {trend.trending_score?.toFixed(3)}
                            </p>
                          </div>

                          <div className="flex items-start gap-2 p-2 bg-amber-50 rounded">
                            <Zap className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                            <p className="text-xs text-amber-900">
                              {getTrendInsight(trend)}
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>Tarama Geçmişi</CardTitle>
            </CardHeader>
            <CardContent>
              {history.length > 0 ? (
                <div className="space-y-2">
                  {history.map((h, i) => (
                    <div key={i} className="flex items-center justify-between p-4 border rounded-lg hover:bg-slate-50">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="outline">
                            {h.mode === 'client' ? '👤 Müşteri' : '🌍 Genel'}
                          </Badge>
                          <p className="font-medium">{h.client || 'Genel Tarama'}</p>
                        </div>
                        <p className="text-sm text-slate-600">
                          {h.keywords?.join(', ')}
                        </p>
                      </div>
                      <Badge>{h.trends_found} trend</Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-slate-400">
                  <Calendar className="h-12 w-12 mx-auto mb-2 opacity-50" />
                  <p>Henüz tarama geçmişi yok</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="insights">
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Tarama İpuçları
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium">İngilizce keyword kullanın</p>
                    <p className="text-xs text-slate-600">Daha geniş kitleye ulaşırsınız</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-purple-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium">3-5 keyword kullanın</p>
                    <p className="text-xs text-slate-600">Optimal sonuç için</p>
                  </div>
                </div>
                <div className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-green-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium">Genel tarama ile pazar araştırması</p>
                    <p className="text-xs text-slate-600">Yeni fırsatları keşfedin</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Award className="h-5 w-5" />
                  Platform Özellikleri
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm font-medium mb-1">✅ Müşteri Bazlı Tarama</p>
                  <p className="text-xs text-slate-600">Müşteriye özel keyword önerileri</p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm font-medium mb-1">✅ Genel Trend Tarama</p>
                  <p className="text-xs text-slate-600">Herhangi bir konuda araştırma</p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm font-medium mb-1">✅ Kategori Filtreleme</p>
                  <p className="text-xs text-slate-600">Sıcak, yükselen, stabil trendler</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
