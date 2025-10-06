'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { generateContent } from '@/lib/api';

export default function ContentPage() {
  const [clientId, setClientId] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [topic, setTopic] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!clientId || !topic) return;
    setLoading(true);
    try {
      const res = await generateContent({
        client_id: clientId,
        platform,
        topic,
        tone: 'professional'
      });
      setResult(res.data);
    } catch (error) {
      console.error('İçerik üretimi hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">İçerik Üretimi</h1>
      
      <Card>
        <CardHeader>
          <CardTitle>Yeni İçerik Oluştur</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium">Müşteri ID</label>
            <Input 
              placeholder="Müşteri ID"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
            />
          </div>
          <div>
            <label className="text-sm font-medium">Platform</label>
            <Select value={platform} onValueChange={setPlatform}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="instagram">Instagram</SelectItem>
                <SelectItem value="facebook">Facebook</SelectItem>
                <SelectItem value="linkedin">LinkedIn</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-sm font-medium">Konu</label>
            <Input 
              placeholder="Örn: Bahar mevsimi sağlık ipuçları"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Üretiliyor...' : 'İçerik Üret'}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Üretilen İçerik</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-50 p-4 rounded-lg whitespace-pre-wrap">
              {result.content || result.text}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
