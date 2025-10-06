'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, TrendingUp, FileText, Target } from 'lucide-react';
import { getClients, getCampaigns } from '@/lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    clients: 0,
    campaigns: 0,
    trends: 0,
    content: 0
  });

  useEffect(() => {
    async function loadStats() {
      try {
        const [clientsRes, campaignsRes] = await Promise.all([
          getClients(),
          getCampaigns()
        ]);
        setStats({
          clients: clientsRes.data.length,
          campaigns: campaignsRes.data.length,
          trends: 0,
          content: 0
        });
      } catch (error) {
        console.error('Stats yüklenemedi:', error);
      }
    }
    loadStats();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Genel Bakış</h1>
        <p className="text-slate-600">OthelloAI Marketing Platform istatistikleri</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Müşteriler</CardTitle>
            <Users className="h-4 w-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.clients}</div>
            <p className="text-xs text-slate-600">Aktif müşteri sayısı</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Kampanyalar</CardTitle>
            <Target className="h-4 w-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.campaigns}</div>
            <p className="text-xs text-slate-600">Aktif kampanya</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Trendler</CardTitle>
            <TrendingUp className="h-4 w-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.trends}</div>
            <p className="text-xs text-slate-600">Taranan trend</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">İçerikler</CardTitle>
            <FileText className="h-4 w-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.content}</div>
            <p className="text-xs text-slate-600">Üretilen içerik</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Hoş Geldiniz</CardTitle>
          <CardDescription>
            OthelloAI Marketing Platform ile sosyal medya stratejilerinizi otomatikleştirin
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <p className="text-sm">Platform özellikleri:</p>
            <ul className="list-disc list-inside text-sm text-slate-600 space-y-1">
              <li>Otomatik trend taraması (Instagram hashtag analizi)</li>
              <li>GPT-4 ile içerik üretimi</li>
              <li>Influencer keşif ve skorlama</li>
              <li>Kampanya yönetimi</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
