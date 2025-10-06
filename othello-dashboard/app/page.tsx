'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, Users, TrendingUp, Sparkles, Target } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <nav className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold text-slate-900">OthelloAI</div>
          <Link href="/dashboard">
            <Button>Dashboard <ArrowRight className="ml-2 h-4 w-4" /></Button>
          </Link>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-slate-900 mb-4">
            AI-Powered Marketing Platform
          </h1>
          <p className="text-xl text-slate-600 mb-8">
            Otomatik trend taraması, içerik üretimi ve influencer keşfi
          </p>
          <Link href="/dashboard">
            <Button size="lg" className="text-lg px-8">
              Başlayın <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader>
              <Users className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle>Müşteri Yönetimi</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                8 aktif müşteri ile sosyal medya stratejilerinizi yönetin
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <TrendingUp className="h-8 w-8 text-green-600 mb-2" />
              <CardTitle>Trend Tarama</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Instagram hashtag analizi ile güncel trendleri takip edin
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Sparkles className="h-8 w-8 text-purple-600 mb-2" />
              <CardTitle>İçerik Üretimi</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                GPT-4 ile otomatik içerik üretimi ve planlama
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Target className="h-8 w-8 text-orange-600 mb-2" />
              <CardTitle>Influencer Keşfi</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Apify ile otomatik influencer bulma ve skorlama
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
