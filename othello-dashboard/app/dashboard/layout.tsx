'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, FileText, TrendingUp, Users, Sparkles, Search, BarChart } from 'lucide-react';

const navigation = [
  { name: 'Ana Sayfa', href: '/dashboard', icon: Home },
  { name: 'İçerik Üretimi', href: '/dashboard/content', icon: Sparkles },
  { name: 'Influencer Keşfi', href: '/dashboard/influencers', icon: Search },
  { name: 'Influencer Stats', href: '/dashboard/influencer-stats', icon: BarChart },
  { name: 'Trendler', href: '/dashboard/trends', icon: TrendingUp },
  { name: 'Müşteriler', href: '/dashboard/clients', icon: Users },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-blue-600">Othello</h1>
            <p className="text-xs text-gray-500">Digital Marketing AI</p>
          </div>

          <nav className="px-3 space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition ${
                    isActive
                      ? 'bg-blue-50 text-blue-600 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span className="text-sm">{item.name}</span>
                </Link>
              );
            })}
          </nav>
        </aside>

        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}
