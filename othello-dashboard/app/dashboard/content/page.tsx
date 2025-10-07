'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { generateContent, getClients } from '@/lib/api';
import { Sparkles, FileText, Target, Users, TrendingUp } from 'lucide-react';

const contentGoals = [
  { value: 'awareness', label: 'Bilinirlik Artırma', icon: '📢', color: 'blue' },
  { value: 'engagement', label: 'Etkileşim', icon: '❤️', color: 'pink' },
  { value: 'sales', label: 'Satış', icon: '💰', color: 'green' },
  { value: 'education', label: 'Bilgilendirme', icon: '��', color: 'purple' },
  { value: 'community', label: 'Topluluk', icon: '👥', color: 'orange' }
];

const platformTypes: Record<string, any> = {
  instagram: {
    types: [
      { value: 'feed', label: 'Feed Post', description: 'Klasik Instagram paylaşımı' },
      { value: 'reel', label: 'Reels', description: 'Kısa video içeriği' },
      { value: 'story', label: 'Story', description: '24 saat görünür içerik' },
      { value: 'carousel', label: 'Carousel', description: 'Çoklu görsel paylaşımı' }
    ]
  },
  facebook: {
    types: [
      { value: 'post', label: 'Post', description: 'Standart paylaşım' },
      { value: 'video', label: 'Video', description: 'Video içeriği' },
      { value: 'event', label: 'Event', description: 'Etkinlik duyurusu' }
    ]
  },
  linkedin: {
    types: [
      { value: 'post', label: 'Post', description: 'Profesyonel paylaşım' },
      { value: 'article', label: 'Article', description: 'Uzun form içerik' },
      { value: 'poll', label: 'Poll', description: 'Anket' }
    ]
  },
  tiktok: {
    types: [
      { value: 'video', label: 'Video', description: 'Kısa video' },
      { value: 'duet', label: 'Duet', description: 'İşbirliği videosu' }
    ]
  }
};

const toneOptions = [
  { value: 'professional', label: 'Profesyonel', emoji: '👔' },
  { value: 'friendly', label: 'Samimi', emoji: '😊' },
  { value: 'casual', label: 'Gündelik', emoji: '��' },
  { value: 'energetic', label: 'Enerjik', emoji: '⚡' },
  { value: 'inspirational', label: 'İlham Verici', emoji: '✨' },
  { value: 'humorous', label: 'Eğlenceli', emoji: '😄' }
];

export default function ContentPage() {
  const [clients, setClients] = useState<any[]>([]);
  const [clientId, setClientId] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [contentType, setContentType] = useState('feed');
  const [goal, setGoal] = useState('awareness');
  const [topic, setTopic] = useState('');
  const [tone, setTone] = useState('professional');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getClients().then(res => setClients(res.data)).catch(console.error);
  }, []);

  const selectedClient = clients.find(c => c.id === clientId);
  const selectedGoal = contentGoals.find(g => g.value === goal);

  const handleGenerate = async () => {
    if (!clientId || !topic) return;
    setLoading(true);
    try {
      const res = await generateContent({
        client_id: clientId,
        platform,
        content_type: contentType,
        topic,
        tone,
        goal
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
      <div>
        <h1 className="text-3xl font-bold">İçerik Üretimi</h1>
        <p className="text-slate-600">AI destekli sosyal medya içeriği oluşturun</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              Yeni İçerik Oluştur
            </CardTitle>
            <CardDescription>Parametreleri seçin ve AI içerik üretsin</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Müşteri Seçimi */}
            <div>
              <label className="text-sm font-medium mb-2 block">Müşteri</label>
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
              {selectedClient && (
                <div className="mt-2 p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm font-medium">{selectedClient.brand_guidelines?.industry}</p>
                  <p className="text-xs text-slate-600 mt-1">
                    {selectedClient.brand_guidelines?.brand_voice}
                  </p>
                </div>
              )}
            </div>

            {/* Amaç Seçimi */}
            <div>
              <label className="text-sm font-medium mb-2 block">İçerik Amacı</label>
              <div className="grid grid-cols-2 gap-2">
                {contentGoals.map(g => (
                  <button
                    key={g.value}
                    onClick={() => setGoal(g.value)}
                    className={`p-3 border-2 rounded-lg text-left transition ${
                      goal === g.value
                        ? `border-${g.color}-600 bg-${g.color}-50`
                        : 'border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{g.icon}</span>
                      <span className="text-sm font-medium">{g.label}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Platform ve Tür */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Platform</label>
                <Select value={platform} onValueChange={(v) => { setPlatform(v); setContentType(platformTypes[v].types[0].value); }}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="instagram">📷 Instagram</SelectItem>
                    <SelectItem value="facebook">📘 Facebook</SelectItem>
                    <SelectItem value="linkedin">💼 LinkedIn</SelectItem>
                    <SelectItem value="tiktok">🎵 TikTok</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">İçerik Türü</label>
                <Select value={contentType} onValueChange={setContentType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {platformTypes[platform]?.types.map((type: any) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <p className="text-xs text-slate-500 mt-1">
                  {platformTypes[platform]?.types.find((t: any) => t.value === contentType)?.description}
                </p>
              </div>
            </div>

            {/* Ton */}
            <div>
              <label className="text-sm font-medium mb-2 block">İçerik Tonu</label>
              <div className="grid grid-cols-3 gap-2">
                {toneOptions.map(t => (
                  <button
                    key={t.value}
                    onClick={() => setTone(t.value)}
                    className={`p-2 border rounded-lg text-sm transition ${
                      tone === t.value
                        ? 'border-pink-600 bg-pink-50'
                        : 'border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    <span className="mr-1">{t.emoji}</span>
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Konu */}
            <div>
              <label className="text-sm font-medium mb-2 block">Konu / Tema</label>
              <Input 
                placeholder="Örn: Bahar mevsimi sağlık ipuçları"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>

            <Button 
              onClick={handleGenerate} 
              disabled={loading || !clientId || !topic}
              className="w-full"
            >
              {loading ? 'Üretiliyor...' : 'İçerik Üret'}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Seçilen Parametreler
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {selectedClient ? (
              <div className="p-3 bg-blue-50 rounded-lg">
                <p className="text-xs text-blue-600">Müşteri</p>
                <p className="text-sm font-semibold">{selectedClient.name}</p>
              </div>
            ) : (
              <div className="p-3 bg-slate-100 rounded-lg text-sm text-slate-500">
                Müşteri seçilmedi
              </div>
            )}

            {selectedGoal && (
              <div className="p-3 bg-purple-50 rounded-lg">
                <p className="text-xs text-purple-600">Amaç</p>
                <p className="text-sm font-semibold">
                  {selectedGoal.icon} {selectedGoal.label}
                </p>
              </div>
            )}

            <div className="p-3 bg-green-50 rounded-lg">
              <p className="text-xs text-green-600">Platform</p>
              <p className="text-sm font-semibold capitalize">{platform} - {contentType}</p>
            </div>

            <div className="p-3 bg-orange-50 rounded-lg">
              <p className="text-xs text-orange-600">Ton</p>
              <p className="text-sm font-semibold">
                {toneOptions.find(t => t.value === tone)?.emoji} {toneOptions.find(t => t.value === tone)?.label}
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Üretilen İçerik
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="bg-slate-50 p-6 rounded-lg whitespace-pre-wrap font-mono text-sm">
              {result.content || result.text}
            </div>
            <div className="flex gap-2 mt-4">
              <Button variant="outline" onClick={() => navigator.clipboard.writeText(result.content || result.text)}>
                📋 Kopyala
              </Button>
              <Button variant="outline">
                💾 Kaydet
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
