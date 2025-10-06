'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { createCampaign } from '@/lib/api';
import { Badge } from '@/components/ui/badge';

export default function NewCampaignPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    client_id: '',
    campaign_type: '',
    sector: '',
    goals: [] as string[],
    budget: '',
    start_date: '',
    end_date: '',
    sales_goal: '',
    awareness_goal: '',
  });

  const sectors = [
    'Gıda ve İçecek',
    'Moda ve Giyim',
    'Güzellik ve Kişisel Bakım',
    'Sağlık ve Fitness',
    'Teknoloji ve Elektronik',
    'Otomotiv ve Elektrikli Araçlar'
  ];

  const campaignGoals = [
    { value: 'awareness', label: 'Bilinirlik Artırma' },
    { value: 'sales', label: 'Satış Odaklı' }
  ];

  const awarenessMetrics = [
    'Erişim Sayısı',
    'Etkileşim Sayısı',
    'Link Tıklama Sayısı',
    'Yorum Sayısı',
    'Beğeni Sayısı',
    'Paylaşım Sayısı'
  ];

  const salesGoals = [
    'Perakende Satış',
    'Toptan Satış',
    'Yüz yüze Satış',
    'Online Satış',
    'Pazaryeri Satışı',
    'Abonelik Satışı',
    'Kiralama Satışı'
  ];

  const altSalesGoals = {
    'Perakende Satış': ['Fiziksel Mağaza Satışı', 'Pop-up Mağaza Satışı', 'Konsiye Satış'],
    'Online Satış': ['E-ticaret Sitesi', 'Sosyal Medya Satışı', 'Mobil Uygulama'],
  };

  const handleNext = () => setStep(step + 1);
  const handleBack = () => setStep(step - 1);

  const handleSubmit = async () => {
    try {
      await createCampaign({
        ...formData,
        campaign_type: formData.campaign_type,
        budget: parseFloat(formData.budget),
        start_date: `${formData.start_date}T00:00:00`,
        end_date: `${formData.end_date}T00:00:00`,
        status: 'planning'
      });
      router.push('/dashboard/campaigns');
    } catch (error) {
      console.error('Kampanya oluşturma hatası:', error);
    }
  };

  const toggleGoal = (goal: string) => {
    setFormData(prev => ({
      ...prev,
      goals: prev.goals.includes(goal)
        ? prev.goals.filter(g => g !== goal)
        : [...prev.goals, goal]
    }));
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Yeni Kampanya Oluştur</h1>
        <p className="text-slate-600">Adım {step} / 5</p>
      </div>

      <div className="flex gap-2 mb-8">
        {[1, 2, 3, 4, 5].map((s) => (
          <div
            key={s}
            className={`h-2 flex-1 rounded ${
              s <= step ? 'bg-pink-600' : 'bg-slate-200'
            }`}
          />
        ))}
      </div>

      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Kampanya Sektörü Seçiniz</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Select value={formData.sector} onValueChange={(v) => setFormData({...formData, sector: v})}>
              <SelectTrigger>
                <SelectValue placeholder="Sektör seçin" />
              </SelectTrigger>
              <SelectContent>
                {sectors.map(s => (
                  <SelectItem key={s} value={s}>{s}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={handleNext} disabled={!formData.sector}>Devam Et</Button>
          </CardContent>
        </Card>
      )}

      {step === 2 && (
        <Card>
          <CardHeader>
            <CardTitle>Kampanya Hedefleri</CardTitle>
            <CardDescription>Bilinirlik Artırma veya Satış Odaklı</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {campaignGoals.map(goal => (
                <button
                  key={goal.value}
                  onClick={() => setFormData({...formData, campaign_type: goal.value})}
                  className={`p-6 border-2 rounded-lg text-left transition ${
                    formData.campaign_type === goal.value
                      ? 'border-pink-600 bg-pink-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="font-semibold mb-2">{goal.label}</div>
                  <p className="text-sm text-slate-600">
                    {goal.value === 'awareness' ? 'Markanızı daha fazla kişiye ulaştırın' : 'Satışlarınızı artırın'}
                  </p>
                </button>
              ))}
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleBack}>Geri</Button>
              <Button onClick={handleNext} disabled={!formData.campaign_type}>Devam Et</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {step === 3 && (
        <Card>
          <CardHeader>
            <CardTitle>
              {formData.campaign_type === 'awareness' ? 'Bilinirlik Hedefleri' : 'Satış Hedefi'}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {formData.campaign_type === 'awareness' ? (
              <div className="grid grid-cols-2 gap-2">
                {awarenessMetrics.map(metric => (
                  <button
                    key={metric}
                    onClick={() => toggleGoal(metric)}
                    className={`p-3 border rounded-lg text-sm ${
                      formData.goals.includes(metric)
                        ? 'border-pink-600 bg-pink-50'
                        : 'border-slate-200'
                    }`}
                  >
                    {metric}
                  </button>
                ))}
              </div>
            ) : (
              <Select value={formData.sales_goal} onValueChange={(v) => setFormData({...formData, sales_goal: v})}>
                <SelectTrigger>
                  <SelectValue placeholder="Satış Hedefi" />
                </SelectTrigger>
                <SelectContent>
                  {salesGoals.map(s => (
                    <SelectItem key={s} value={s}>{s}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleBack}>Geri</Button>
              <Button onClick={handleNext}>Devam Et</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {step === 4 && (
        <Card>
          <CardHeader>
            <CardTitle>Kampanya Detayı</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Kampanya Adı</label>
              <Input
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                placeholder="Örn: Kış Sezonu Kampanyası"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Müşteri ID</label>
              <Input
                value={formData.client_id}
                onChange={(e) => setFormData({...formData, client_id: e.target.value})}
                placeholder="Müşteri ID"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Başlangıç</label>
                <Input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                />
              </div>
              <div>
                <label className="text-sm font-medium">Bitiş</label>
                <Input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium">Bütçe ($)</label>
              <Input
                type="number"
                value={formData.budget}
                onChange={(e) => setFormData({...formData, budget: e.target.value})}
                placeholder="5000"
              />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleBack}>Geri</Button>
              <Button onClick={handleNext}>Devam Et</Button>
            </div>
          </CardContent>
        </Card>
      )}

      {step === 5 && (
        <Card>
          <CardHeader>
            <CardTitle>Kampanya Önizleme</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <p><strong>Kampanya Adı:</strong> {formData.name}</p>
              <p><strong>Sektör:</strong> {formData.sector}</p>
              <p><strong>Hedef:</strong> <Badge>{formData.campaign_type === 'awareness' ? 'Bilinirlik' : 'Satış'}</Badge></p>
              <p><strong>Bütçe:</strong> ${formData.budget}</p>
              <p><strong>Tarih:</strong> {formData.start_date} - {formData.end_date}</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={handleBack}>Geri</Button>
              <Button onClick={handleSubmit} className="bg-pink-600">Kampanya Oluştur</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
