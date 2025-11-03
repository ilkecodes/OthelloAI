'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Sparkles, TrendingUp, Users, FileText } from 'lucide-react';
import Link from 'next/link';

const quickActions = [
  {
    title: 'İçerik Üret',
    description: 'AI ile sosyal medya içeriği oluştur',
    icon: Sparkles,
    href: '/dashboard/content',
    color: 'blue'
  },
  {
    title: 'Trendleri İncele',
    description: 'Güncel trendleri keşfet',
    icon: TrendingUp,
    href: '/dashboard/trends',
    color: 'green'
  },
  {
    title: 'Müşteriler',
    description: 'Müşteri portföyünü yönet',
    icon: Users,
    href: '/dashboard/clients',
    color: 'purple'
  }
];

export default function DashboardPage() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Hoş Geldiniz</h1>
        <p className="text-gray-600">Othello AI Marketing Platform</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link key={action.href} href={action.href}>
              <Card className="hover:shadow-lg transition cursor-pointer">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-lg bg-${action.color}-100 flex items-center justify-center mb-3`}>
                    <Icon className={`h-6 w-6 text-${action.color}-600`} />
                  </div>
                  <CardTitle className="text-lg">{action.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Sistem Özellikleri</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="font-semibold">Şeffaf Akış Formatı</p>
                <p className="text-gray-600">9 adımlı detaylı içerik üretimi</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="font-semibold">Marka Kimliği Koruması</p>
                <p className="text-gray-600">Her marka için özel renk ve font kullanımı</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="font-semibold">Tasarımcı Brief&apos;i</p>
                <p className="text-gray-600">Detaylı görsel tasarım notları</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="font-semibold">Çoklu Format</p>
                <p className="text-gray-600">Carousel, Reel, Post, Thread desteği</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
