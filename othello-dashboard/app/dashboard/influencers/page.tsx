'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Search, Instagram, Loader2, MessageCircle, Heart, CheckCircle, Save, X, Shield, Award, AlertTriangle } from 'lucide-react';

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
  quality_score: number;
  tier: string;
  badge: string;
  reasons: string[];
  score_breakdown: {
    bio_match: number;
    content_match: number;
    engagement: number;
    authenticity: number;
    activity: number;
  };
  authenticity: {
    authenticity_score: number;
    status: string;
    status_color: string;
    red_flags: string[];
    warnings: string[];
    is_authentic: boolean;
  };
}

export default function InfluencersPage() {
  const [searchInput, setSearchInput] = useState('');
  const [location, setLocation] = useState('');
  const [results, setResults] = useState<Influencer[]>([]);
  const [loading, setLoading] = useState(false);
  const [compareMode, setCompareMode] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [selectedInfluencer, setSelectedInfluencer] = useState<Influencer | null>(null);
  const [searchMode, setSearchMode] = useState<'basic' | 'advanced'>('advanced');
  const [minQualityScore, setMinQualityScore] = useState('40');

  const locations = ["İstanbul", "Ankara", "İzmir", "Turkey", "Dubai", "London"];
  
  const examples = [
    { query: "food blogger", label: "🍕 Yemek Blogger" },
    { query: "fitness trainer", label: "💪 Fitness Antrenör" },
    { query: "travel photographer", label: "✈️ Seyahat Fotoğrafçı" },
    { query: "beauty influencer", label: "💄 Güzellik" }
  ];

  const handleSearch = async () => {
    if (!searchInput) return;
    
    setLoading(true);
    
    try {
      const endpoint = searchMode === 'advanced' 
        ? 'http://localhost:8000/api/advanced-search/advanced-search'
        : 'http://localhost:8000/api/influencer-discovery/search';
      
      const body = searchMode === 'advanced'
        ? {
            search_query: searchInput,
            location: location || null,
            min_quality_score: parseInt(minQualityScore)
          }
        : {
            search_query: searchInput,
            location: location || null
          };
      
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      
      const data = await res.json();
      setResults(data.profiles || []);
    } catch (error) {
      console.error('Error:', error);
      alert('Arama hatası!');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (inf: Influencer) => {
    try {
      const res = await fetch('http://localhost:8000/api/influencer-stats/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: inf.username,
          full_name: inf.full_name,
          followers: inf.followers,
          engagement_rate: inf.engagement_rate,
          notes: `Kalite Skoru: ${inf.quality_score || 'Yok'}`
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

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-800 border-green-300';
    if (score >= 60) return 'bg-blue-100 text-blue-800 border-blue-300';
    if (score >= 40) return 'bg-orange-100 text-orange-800 border-orange-300';
    return 'bg-gray-100 text-gray-800 border-gray-300';
  };

  const getAuthenticityColor = (color: string) => {
    if (color === 'green') return 'bg-green-100 text-green-800';
    if (color === 'yellow') return 'bg-yellow-100 text-yellow-800';
    if (color === 'orange') return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  // Türkçe çeviri fonksiyonu
  const translateStatus = (status: string) => {
    const translations: {[key: string]: string} = {
      "✅ Authentic": "✅ Güvenilir",
      "⚠️ Mostly Authentic": "⚠️ Çoğunlukla Güvenilir",
      "🤔 Questionable": "🤔 Şüpheli",
      "🚫 Suspicious": "🚫 Kuşkulu"
    };
    return translations[status] || status;
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">🎯 Gelişmiş Influencer Keşfi</h1>
          <p className="text-gray-600">AI destekli arama, kalite puanı ve güvenilirlik kontrolü</p>
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
          <CardTitle className="flex items-center justify-between">
            <span>Ara</span>
            <div className="flex gap-2">
              <Button
                size="sm"
                variant={searchMode === 'basic' ? 'default' : 'outline'}
                onClick={() => setSearchMode('basic')}
              >
                Basit
              </Button>
              <Button
                size="sm"
                variant={searchMode === 'advanced' ? 'default' : 'outline'}
                onClick={() => setSearchMode('advanced')}
              >
                🚀 Gelişmiş
              </Button>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {searchMode === 'advanced' && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm">
              <p className="font-semibold text-blue-800 mb-1">🚀 Gelişmiş Mod Aktif</p>
              <p className="text-blue-700">AI hashtag üretimi, içerik analizi, kalite puanlama ve güvenilirlik kontrolü</p>
            </div>
          )}

          <div className="grid md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <label className="text-sm font-medium mb-2 block">Arama *</label>
              <Input
                placeholder="Örn: yemek blogger, fitness antrenör"
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
                {loading ? 'Analiz ediliyor...' : 'Ara'}
              </Button>
            </div>
          </div>

          {searchMode === 'advanced' && (
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">Minimum Kalite Puanı:</label>
              <input
                type="range"
                min="0"
                max="100"
                step="10"
                value={minQualityScore}
                onChange={(e) => setMinQualityScore(e.target.value)}
                className="flex-1"
              />
              <span className="text-sm font-semibold w-12">{minQualityScore}</span>
            </div>
          )}

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
                    {inf.quality_score && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Kalite Puanı:</span>
                        <span className="font-bold text-purple-600">{inf.quality_score}/100</span>
                      </div>
                    )}
                    <div className="flex justify-between">
                      <span className="text-gray-600">Takipçi:</span>
                      <span className="font-semibold">{formatNumber(inf.followers)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Etkileşim:</span>
                      <span className="font-semibold text-green-600">{inf.engagement_rate}%</span>
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
          <p className="text-gray-600 font-semibold">
            {searchMode === 'advanced' ? '🤖 AI profilleri analiz ediyor...' : 'Instagram aranıyor...'}
          </p>
          <p className="text-sm text-gray-400 mt-2">
            {searchMode === 'advanced' 
              ? 'Hashtag üretimi, içerik analizi ve kalite puanlama yapılıyor...'
              : 'Bu 1-2 dakika sürebilir'}
          </p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>{results.length} Nitelikli Influencer Bulundu</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              {results.map((inf, idx) => (
                <Card 
                  key={idx} 
                  className={`hover:shadow-lg transition cursor-pointer ${
                    compareMode && selected.has(inf.username) ? 'ring-2 ring-blue-500' : ''
                  }`}
                  onClick={() => compareMode ? toggleSelect(inf.username) : setSelectedInfluencer(inf)}
                >
                  <CardHeader className="pb-3">
                    {inf.quality_score !== undefined && (
                      <div className="flex items-center justify-between mb-2">
                        <Badge className={`${getScoreColor(inf.quality_score)} border`}>
                          {inf.tier || inf.badge} - {inf.quality_score}/100
                        </Badge>
                        {inf.authenticity && (
                          <Badge className={getAuthenticityColor(inf.authenticity.status_color)}>
                            <Shield className="h-3 w-3 mr-1" />
                            {inf.authenticity.authenticity_score}
                          </Badge>
                        )}
                      </div>
                    )}

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
                    
                    {inf.reasons && inf.reasons.length > 0 && (
                      <div className="bg-green-50 p-2 rounded text-xs">
                        <p className="font-semibold text-green-800 mb-1">✓ Neden uygun:</p>
                        {inf.reasons.slice(0, 2).map((reason, i) => (
                          <p key={i} className="text-green-700">• {reason}</p>
                        ))}
                      </div>
                    )}

                    {inf.authenticity?.warnings && inf.authenticity.warnings.length > 0 && (
                      <div className="bg-yellow-50 p-2 rounded text-xs">
                        <p className="font-semibold text-yellow-800 flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3" />
                          Uyarılar:
                        </p>
                        {inf.authenticity.warnings.slice(0, 1).map((warning, i) => (
                          <p key={i} className="text-yellow-700">• {warning}</p>
                        ))}
                      </div>
                    )}
                    
                    <div className="grid grid-cols-3 gap-2 text-center text-xs">
                      <div>
                        <p className="font-bold text-blue-600">{formatNumber(inf.followers)}</p>
                        <p className="text-gray-500">Takipçi</p>
                      </div>
                      <div>
                        <p className="font-bold text-green-600">{inf.engagement_rate}%</p>
                        <p className="text-gray-500">Etkileşim</p>
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

      {/* Detaylı Modal */}
      {selectedInfluencer && !compareMode && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-6 z-50" onClick={() => setSelectedInfluencer(null)}>
          <Card className="max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <CardHeader>
              <div className="flex items-start gap-4">
                <img src={selectedInfluencer.profile_pic} alt={selectedInfluencer.username} className="w-20 h-20 rounded-full" />
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <CardTitle>{selectedInfluencer.full_name}</CardTitle>
                    {selectedInfluencer.quality_score !== undefined && (
                      <Badge className={`${getScoreColor(selectedInfluencer.quality_score)} text-lg px-4 py-2`}>
                        {selectedInfluencer.quality_score}/100
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-gray-500">@{selectedInfluencer.username}</p>
                  {selectedInfluencer.badge && (
                    <p className="text-sm font-semibold text-purple-600 mt-1">{selectedInfluencer.badge}</p>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm">{selectedInfluencer.biography}</p>
              
              {selectedInfluencer.score_breakdown && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-3 text-sm flex items-center gap-2">
                    <Award className="h-4 w-4" />
                    Kalite Puanı Detayı
                  </h4>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Bio Uyumu:</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" 
                            style={{ width: `${(selectedInfluencer.score_breakdown.bio_match / 30) * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold w-12 text-right">{selectedInfluencer.score_breakdown.bio_match.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>İçerik Uyumu:</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" 
                            style={{ width: `${(selectedInfluencer.score_breakdown.content_match / 30) * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold w-12 text-right">{selectedInfluencer.score_breakdown.content_match.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Etkileşim:</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" 
                            style={{ width: `${(selectedInfluencer.score_breakdown.engagement / 20) * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold w-12 text-right">{selectedInfluencer.score_breakdown.engagement.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Güvenilirlik:</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" 
                            style={{ width: `${(selectedInfluencer.score_breakdown.authenticity / 10) * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold w-12 text-right">{selectedInfluencer.score_breakdown.authenticity.toFixed(1)}</span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Aktivite:</span>
                      <div className="flex items-center gap-2">
                        <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" 
                            style={{ width: `${(selectedInfluencer.score_breakdown.activity / 10) * 100}%` }}
                          />
                        </div>
                        <span className="font-semibold w-12 text-right">{selectedInfluencer.score_breakdown.activity.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {selectedInfluencer.authenticity && (
                <div className={`p-4 rounded-lg ${getAuthenticityColor(selectedInfluencer.authenticity.status_color)}`}>
                  <h4 className="font-semibold mb-2 text-sm flex items-center gap-2">
                    <Shield className="h-4 w-4" />
                    Güvenilirlik Kontrolü: {translateStatus(selectedInfluencer.authenticity.status)}
                  </h4>
                  {selectedInfluencer.authenticity.red_flags && selectedInfluencer.authenticity.red_flags.length > 0 && (
                    <div className="mt-2">
                      <p className="font-semibold text-xs">🚫 Kırmızı Bayraklar:</p>
                      {selectedInfluencer.authenticity.red_flags.map((flag, i) => (
                        <p key={i} className="text-xs">• {flag}</p>
                      ))}
                    </div>
                  )}
                  {selectedInfluencer.authenticity.warnings && selectedInfluencer.authenticity.warnings.length > 0 && (
                    <div className="mt-2">
                      <p className="font-semibold text-xs">⚠️ Uyarılar:</p>
                      {selectedInfluencer.authenticity.warnings.map((warning, i) => (
                        <p key={i} className="text-xs">• {warning}</p>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {selectedInfluencer.reasons && selectedInfluencer.reasons.length > 0 && (
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2 text-sm text-green-800">✓ Neden Mükemmel Bir Eşleşme</h4>
                  <ul className="space-y-1">
                    {selectedInfluencer.reasons.map((reason, i) => (
                      <li key={i} className="text-sm text-green-700">• {reason}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <p className="text-2xl font-bold text-blue-600">{formatNumber(selectedInfluencer.followers)}</p>
                  <p className="text-sm text-gray-600">Takipçi</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-green-600">{selectedInfluencer.engagement_rate}%</p>
                  <p className="text-sm text-gray-600">Etkileşim Oranı</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-purple-600">{selectedInfluencer.posts_count}</p>
                  <p className="text-sm text-gray-600">Toplam Post</p>
                </div>
              </div>

              <Button className="w-full" onClick={() => window.open(selectedInfluencer.instagram_url, '_blank')}>
                <Instagram className="h-4 w-4 mr-2" />
                Instagram Profilini Görüntüle
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
