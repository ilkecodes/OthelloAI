'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { getCampaigns } from '@/lib/api';
import { Plus } from 'lucide-react';

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);

  useEffect(() => {
    getCampaigns().then(res => setCampaigns(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Kampanyalar</h1>
        <Link href="/dashboard/campaigns/new">
          <Button className="bg-pink-600">
            <Plus className="mr-2 h-4 w-4" />
            Yeni Kampanya
          </Button>
        </Link>
      </div>
      <div className="grid gap-6">
        {campaigns.map((c) => (
          <Card key={c.id}>
            <CardHeader>
              <CardTitle>{c.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <div>
                  <p className="text-sm">Bütçe</p>
                  <p className="font-bold">${c.budget}</p>
                </div>
                <Badge>{c.status}</Badge>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
