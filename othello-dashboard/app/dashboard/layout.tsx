'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, TrendingUp, FileText, Target, UserSearch } from 'lucide-react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const links = [
    { href: '/dashboard', label: 'Genel Bakış', icon: LayoutDashboard },
    { href: '/dashboard/clients', label: 'Müşteriler', icon: Users },
    { href: '/dashboard/trends', label: 'Trendler', icon: TrendingUp },
    { href: '/dashboard/content', label: 'İçerikler', icon: FileText },
    { href: '/dashboard/campaigns', label: 'Kampanyalar', icon: Target },
    { href: '/dashboard/influencers', label: 'Influencer Keşfi', icon: UserSearch },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="text-2xl font-bold">OthelloAI Dashboard</div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-6 flex gap-6">
        <aside className="w-64 bg-white rounded-lg border p-4">
          <nav className="space-y-2">
            {links.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-slate-900 text-white'
                      : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </aside>

        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
