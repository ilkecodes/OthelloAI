'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, FileText, TrendingUp, Users, Sparkles } from 'lucide-react';

const navigation = [
  { name: 'Ana Sayfa', href: '/dashboard', icon: Home },
  { name: 'İçerik Üretimi', href: '/dashboard/content', icon: Sparkles },
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
        {/* Sidebar */}
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
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          <div className="absolute bottom-6 left-6 right-6">
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
              <p className="text-xs font-semibold text-gray-700 mb-1">Othello AI</p>
              <p className="text-xs text-gray-600">v2.0.0</p>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1">
          {children}
        </main>
      </div>
    </div>
  );
}
