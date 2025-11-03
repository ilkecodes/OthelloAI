"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Sparkles, Loader2, Info } from "lucide-react";

const contentGoals = [
  { value: "awareness", label: "Bilinirlik", icon: "📢" },
  { value: "engagement", label: "Etkileşim", icon: "❤️" },
  { value: "sales", label: "Satış", icon: "💰" },
  { value: "education", label: "Eğitim", icon: "📚" },
];

const platformTypes: Record<string, any> = {
  instagram: {
    types: [
      { value: "carousel", label: "Carousel", icon: "🎠" },
      { value: "reel", label: "Reel", icon: "🎬" },
      { value: "post", label: "Post", icon: "📸" },
    ],
  },
  linkedin: {
    types: [
      { value: "carousel", label: "Carousel", icon: "📑" },
      { value: "post", label: "Post", icon: "💼" },
    ],
  },
  twitter: {
    types: [
      { value: "thread", label: "Thread", icon: "🧵" },
      { value: "tweet", label: "Tweet", icon: "🐦" },
    ],
  },
};

const CLIENTS = [
  { id: "1", name: "Op. Dr. Murat Önal" },
  { id: "2", name: "Kemerli Ev Restaurant" },
  { id: "3", name: "Basda Cyprus" },
  { id: "4", name: "Baklava Atölyesi" },
  { id: "5", name: "DJ Soydan Korkmaz" },
  { id: "6", name: "Othello Digital" },
  { id: "7", name: "Nesdersan Kıbrıs" },
  { id: "8", name: "Casa De Mellizo" },
];

export default function ContentPage() {
  const [clientId, setClientId] = useState("");
  const [platform, setPlatform] = useState("instagram");
  const [contentType, setContentType] = useState("carousel");
  const [goal, setGoal] = useState("engagement");
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const selectedClient = CLIENTS.find((c) => c.id === clientId);

  const handleGenerate = async () => {
    if (!selectedClient || !topic) return;

    setLoading(true);
    setResult("");

    try {
      const res = await fetch("/api/content/simple-generate", 
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            client_name: selectedClient.name,
            platform,
            content_type: contentType,
            topic,
            goal,
          }),
        },
      );

      const data = await res.json();

      if (data.success && data.content) {
        setResult(data.content);
      } else {
        setResult("❌ İçerik üretilemedi.");
      }
    } catch (error) {
      console.error("Error:", error);
      setResult("❌ Hata oluştu. Backend çalışıyor mu kontrol edin.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold">İçerik Üretimi</h1>
        <p className="text-slate-600">
          Şeffaf akış formatında AI destekli içerik
        </p>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start gap-3">
        <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
        <div className="text-sm text-blue-900">
          <p className="font-semibold mb-1">
            Şeffaf Akış Formatı + Marka Kimliği
          </p>
          <p className="text-blue-700">
            Her içerik detaylı akışla üretilir ve marka renkler/fontları korunur
          </p>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5" />
                İçerik Ayarları
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Müşteri
                </label>
                <Select value={clientId} onValueChange={setClientId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Müşteri seçin" />
                  </SelectTrigger>
                  <SelectContent>
                    {CLIENTS.map((client) => (
                      <SelectItem key={client.id} value={client.id}>
                        {client.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Platform
                </label>
                <Select
                  value={platform}
                  onValueChange={(v) => {
                    setPlatform(v);
                    const types = platformTypes[v]?.types || [];
                    if (types.length > 0) {
                      setContentType(types[0].value);
                    }
                  }}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="instagram">📷 Instagram</SelectItem>
                    <SelectItem value="linkedin">💼 LinkedIn</SelectItem>
                    <SelectItem value="twitter">🐦 Twitter</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Format</label>
                <Select value={contentType} onValueChange={setContentType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {(platformTypes[platform]?.types || []).map((type: any) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.icon} {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Hedef</label>
                <div className="grid grid-cols-2 gap-2">
                  {contentGoals.map((g) => (
                    <button
                      key={g.value}
                      onClick={() => setGoal(g.value)}
                      className={`p-2 border-2 rounded-lg transition text-left ${
                        goal === g.value
                          ? "border-blue-600 bg-blue-50"
                          : "border-slate-200 hover:border-slate-300"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-xl">{g.icon}</span>
                        <span className="text-xs font-medium">{g.label}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Konu / Tema
                </label>
                <Input
                  placeholder="Örn: IVF süreci"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />
              </div>

              <Button
                onClick={handleGenerate}
                disabled={loading || !clientId || !topic}
                className="w-full"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Üretiliyor...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    İçerik Üret
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {selectedClient && (
            <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Seçilenler</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div>
                  <span className="text-gray-600">Müşteri:</span>
                  <p className="font-semibold">{selectedClient.name}</p>
                </div>
                <div>
                  <span className="text-gray-600">Platform:</span>
                  <p className="font-semibold capitalize">{platform}</p>
                </div>
                <div>
                  <span className="text-gray-600">Format:</span>
                  <p className="font-semibold capitalize">{contentType}</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Şeffaf Akış Çıktısı</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex flex-col items-center justify-center py-20">
                <Loader2 className="h-12 w-12 animate-spin text-blue-600 mb-4" />
                <p className="text-gray-600">İçerik üretiliyor...</p>
                <p className="text-sm text-gray-400 mt-2">
                  Bu 10-30 saniye sürebilir
                </p>
              </div>
            ) : result ? (
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-sm bg-gradient-to-br from-gray-50 to-white p-6 rounded-lg border-2 border-gray-200 font-mono leading-relaxed overflow-x-auto">
                  {result}
                </pre>
              </div>
            ) : (
              <div className="text-center py-20 text-gray-400">
                <Sparkles className="h-16 w-16 mx-auto mb-4 opacity-30" />
                <p className="text-lg font-medium mb-2">
                  Sonuç burada görünecek
                </p>
                <p className="text-sm">
                  Sol taraftan ayarları yapıp &quot;İçerik Üret&quot; butonuna
                  tıklayın
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
