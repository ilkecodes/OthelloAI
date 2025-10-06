'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { searchInfluencers } from '@/lib/api';
import { Users, TrendingUp } from 'lucide-react';

export default function InfluencersPage() {
  const [campaignId, setCampaignId] = useState('');
  const [sector, setSector] = useState('Gıda ve İçecek');
  const [location, setLocation] = useState('Cyprus');
  const [minFollowers, setMinFollowers] = useState('5000');
  const [maxFollowers, setMaxFollowers] = useState('100000');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!campaignId) return;
    setLoading(true);
    try {
      const res = await searchInfluencers({
        campaign_id: campaignId,
        sector,
        goals: ['Marka Bilinirliği'],
        age_range: '18-65',
        gender: 'Tümü',
        location,
        min_followers: parseInt(minFollowers),
        max_followers: parseInt(maxFollowers),
        platforms: ['instagram'],
        sales_goal: 'Satış Odaklı'
      });
      setResults(res.data);
    } catch (error) {
      console.error('Influencer arama hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Influencer Keşfi</h1>
        <p className="text-slate-600">Kampanyanız için en uygun influencer'ları bulun</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Arama Kriterleri</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Kampanya ID</label>
              <Input 
                placeholder="Kampanya ID"
                value={campaignId}
                onChange={(e) => setCampaignId(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Sektör</label>
              <Input 
                value={sector}
                onChange={(e) => setSector(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Lokasyon</label>
              <Input 
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Min Takipçi</label>
              <Input 
                type="number"
                value={minFollowers}
                onChange={(e) => setMinFollowers(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium">Max Takipçi</label>
              <Input 
                type="number"
                value={maxFollowers}
                onChange={(e) => setMaxFollowers(e.target.value)}
              />
            </div>
          </div>
          <Button onClick={handleSearch} disabled={loading}>
            {loading ? 'Aranıyor...' : 'Influencer Ara'}
          </Button>
        </CardContent>
      </Card>

      {results && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">
              {results.total_found} Influencer Bulundu
            </h2>
            <div className="text-right">
              <p className="text-sm text-slate-600">Toplam Tahmini Maliyet</p>
              <p className="text-2xl font-bold">${results.total_estimated_cost?.toFixed(2)}</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.recommended_influencers?.map((inf: any, i: number) => (
              <Card key={i} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">@{inf.username}</CardTitle>
                      <Badge className="mt-2">{inf.tier}</Badge>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-slate-600">Skor</p>
                      <p className="text-2xl font-bold">{inf.score}</p>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-slate-600" />
                      <span className="text-sm font-semibold">
                        {inf.followers?.toLocaleString()} takipçi
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-slate-600" />
                      <span className="text-sm">
                        %{inf.engagement_rate} etkileşim
                      </span>
                    </div>
                    {inf.biography && (
                      <p className="text-xs text-slate-600 line-clamp-2">
                        {inf.biography}
                      </p>
                    )}
                    <div className="pt-2 border-t">
                      <p className="text-xs text-slate-600">Tahmini Maliyet</p>
                      <p className="text-lg font-bold">${inf.estimated_cost?.toFixed(2)}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
