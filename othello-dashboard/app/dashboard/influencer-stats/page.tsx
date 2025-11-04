'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, TrendingUp, BarChart3, Target } from 'lucide-react';

export default function InfluencerStatsPage() {
  const [stats, setStats] = useState<any>(null);
  const [influencers, setInfluencers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, influencersRes] = await Promise.all([
        fetch('/api/influencer-stats/stats'),
        fetch('/api/influencer-stats/saved')
      ]);
      
      const statsData = await statsRes.json();
      const influencersData = await influencersRes.json();
      
      setStats(statsData);
      setInfluencers(influencersData.influencers || []);
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

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Influencer Dashboard</h1>
        <p className="text-gray-600">Kaydedilen influencer istatistikleri</p>
      </div>

      <div className="grid md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Toplam Influencer</p>
                <p className="text-2xl font-bold">{stats?.total_influencers || 0}</p>
              </div>
              <Users className="h-8 w-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Toplam Erişim</p>
                <p className="text-2xl font-bold">{formatNumber(stats?.total_reach || 0)}</p>
              </div>
              <Target className="h-8 w-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Ort. Engagement</p>
                <p className="text-2xl font-bold">{stats?.avg_engagement || 0}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Kategoriler</p>
                <p className="text-2xl font-bold">{stats?.top_categories?.length || 0}</p>
              </div>
              <BarChart3 className="h-8 w-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Kaydedilen Influencer&apos;lar</CardTitle>
        </CardHeader>
        <CardContent>
          {influencers.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>Henüz kayıtlı influencer yok</p>
              <p className="text-sm mt-2">Influencer Keşfi sayfasından ekleyin</p>
            </div>
          ) : (
            <div className="space-y-2">
              {influencers.map((inf, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                  <div>
                    <p className="font-semibold">{inf.full_name}</p>
                    <p className="text-sm text-gray-500">@{inf.username}</p>
                  </div>
                  <div className="text-right text-sm">
                    <p className="font-semibold text-blue-600">{formatNumber(inf.followers)} takipçi</p>
                    <p className="text-gray-500">{inf.engagement_rate}% engagement</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
