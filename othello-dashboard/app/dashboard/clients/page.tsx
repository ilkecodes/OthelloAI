'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Users, Plus, Building, Instagram } from 'lucide-react';

interface Client {
  id: string;
  name: string;
  industry: string;
  instagram: string;
  sector: string;
}

const CLIENTS: Client[] = [
  {
    id: '1',
    name: 'Op. Dr. Murat Önal',
    industry: 'Sağlık - IVF',
    instagram: '@drmuratonal',
    sector: 'medical_ivf'
  },
  {
    id: '2',
    name: 'Kemerli Ev Restaurant',
    industry: 'Gastronomi - Fine Dining',
    instagram: '@kemerlievrestaurant',
    sector: 'fine_dining'
  },
  {
    id: '3',
    name: 'Basda Cyprus',
    industry: 'Cafe & Restaurant',
    instagram: '@basda.cyprus',
    sector: 'restaurant_cafe'
  },
  {
    id: '4',
    name: 'Baklava Atölyesi',
    industry: 'Gıda - Geleneksel',
    instagram: '@baklava_atolyesi',
    sector: 'traditional_food'
  },
  {
    id: '5',
    name: 'DJ Soydan Korkmaz',
    industry: 'Eğlence - Müzik',
    instagram: '@djsoydankorkmazcy',
    sector: 'entertainment'
  },
  {
    id: '6',
    name: 'Othello Digital',
    industry: 'Dijital Pazarlama',
    instagram: '@othellodigitalcom',
    sector: 'digital_marketing'
  },
  {
    id: '7',
    name: 'Nesdersan Kıbrıs',
    industry: 'İnşaat Malzemeleri',
    instagram: '@nesdersan.com_kibris',
    sector: 'construction_materials'
  },
  {
    id: '8',
    name: 'Casa De Mellizo',
    industry: 'Gastronomi - Akdeniz',
    instagram: '@casademellizo',
    sector: 'restaurant'
  }
];

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    setTimeout(() => {
      setClients(CLIENTS);
      setLoading(false);
    }, 500);
  }, []);

  const filteredClients = clients.filter(client =>
    client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    client.industry.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sectorColors: Record<string, string> = {
    medical_ivf: 'bg-blue-100 text-blue-700',
    fine_dining: 'bg-purple-100 text-purple-700',
    restaurant_cafe: 'bg-orange-100 text-orange-700',
    traditional_food: 'bg-green-100 text-green-700',
    entertainment: 'bg-pink-100 text-pink-700',
    digital_marketing: 'bg-indigo-100 text-indigo-700',
    construction_materials: 'bg-red-100 text-red-700',
    restaurant: 'bg-yellow-100 text-yellow-700'
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Müşteriler</h1>
          <p className="text-gray-600">{clients.length} aktif müşteri</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Yeni Müşteri
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Müşteri Portföyü</CardTitle>
            <div className="w-64">
              <Input
                placeholder="Müşteri ara..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Yükleniyor...</p>
            </div>
          ) : filteredClients.length === 0 ? (
            <div className="text-center py-12">
              <Users className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-600">Müşteri bulunamadı</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filteredClients.map((client) => (
                <Card key={client.id} className="hover:shadow-lg transition cursor-pointer">
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-sm leading-tight mb-2">
                          {client.name}
                        </CardTitle>
                        <span className={`inline-block text-xs px-2 py-1 rounded-full ${sectorColors[client.sector] || 'bg-gray-100 text-gray-700'}`}>
                          {client.industry}
                        </span>
                      </div>
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center flex-shrink-0">
                        <Building className="h-5 w-5 text-blue-600" />
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Instagram className="h-4 w-4" />
                      <span className="text-sm truncate">{client.instagram}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="grid md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-blue-600">{clients.length}</p>
              <p className="text-sm text-gray-600">Toplam Müşteri</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-green-600">5</p>
              <p className="text-sm text-gray-600">Farklı Sektör</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-purple-600">24</p>
              <p className="text-sm text-gray-600">Bu Ay İçerik</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
