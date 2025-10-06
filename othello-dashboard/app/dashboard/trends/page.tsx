'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { scanTrends, getClients } from '@/lib/api';
import { TrendingUp } from 'lucide-react';

export default function TrendsPage() {
  const [clientId, setClientId] = useState('');
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    if (!clientId || !keywords) return;
    setLoading(true);
    try {
      const res = await scanTrends({
        client_id: clientId,
        keywords: keywords.split(',').map(k => k.trim()),
        limit: 30
      });
      setResults(res.data);
    } catch (error) {
      console.error('Trend taraması hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Trend Tarama</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Yeni Trend Taraması</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Müşteri ID</label>
            <Input 
              placeholder="Müşteri ID girin"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Keywords (virgülle ayırın)</label>
            <Input 
              placeholder="sağlık, estetik, beauty"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
            />
          </div>
          <Button onClick={handleScan} disabled={loading}>
            {loading ? 'Taranıyor...' : 'Tara'}
          </Button>
        </CardContent>
      </Card>

      {results && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {results.trends?.map((trend: any, i: number) => (
            <Card key={i}>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  #{trend.keyword}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div>
                    <p className="text-sm text-slate-600">Post Sayısı</p>
                    <p className="text-xl font-bold">{trend.post_count}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Ortalama Etkileşim</p>
                    <p className="text-xl font-bold">{trend.avg_engagement?.toFixed(1)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Trend Skoru</p>
                    <p className="text-xl font-bold">{trend.trending_score?.toFixed(2)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
