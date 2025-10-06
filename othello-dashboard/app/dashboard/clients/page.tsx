'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { getClients } from '@/lib/api';
import { Copy } from 'lucide-react';

export default function ClientsPage() {
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    async function loadClients() {
      try {
        const res = await getClients();
        setClients(res.data);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }
    loadClients();
  }, []);

  const copyId = (id: string) => {
    navigator.clipboard.writeText(id);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (loading) return <div className="p-8">Yükleniyor...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Müşteriler</h1>
        <p className="text-slate-600">{clients.length} aktif müşteri</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {clients.map((client) => (
          <Card key={client.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="mb-1">{client.name}</CardTitle>
                  <CardDescription>{client.brand_guidelines?.industry}</CardDescription>
                </div>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <code className="text-xs bg-slate-100 px-2 py-1 rounded flex-1 truncate">
                  {client.id}
                </code>
                <button
                  onClick={() => copyId(client.id)}
                  className="p-1 hover:bg-slate-100 rounded"
                  title="ID'yi kopyala"
                >
                  <Copy className={`h-4 w-4 ${copiedId === client.id ? 'text-green-600' : 'text-slate-600'}`} />
                </button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <p className="text-sm text-slate-600">
                  {client.brand_guidelines?.description}
                </p>
                <div>
                  <p className="text-xs font-semibold mb-2">Keywords:</p>
                  <div className="flex flex-wrap gap-1">
                    {client.keywords?.keywords?.slice(0, 3).map((kw: string, i: number) => (
                      <Badge key={i} variant="secondary">{kw}</Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-xs font-semibold mb-2">Platforms:</p>
                  <div className="flex flex-wrap gap-1">
                    {client.platforms?.platforms?.map((p: string, i: number) => (
                      <Badge key={i}>{p}</Badge>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
