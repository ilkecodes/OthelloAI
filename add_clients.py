import json
import urllib.request

backend_url = "https://othello-backend-production-7acc.up.railway.app"

clients = [
    {"name": "Op. Dr. Murat Önal", "industry": "Healthcare", "description": "Kadın Hastalıkları", "target_audience": "Kadınlar", "brand_voice": "Profesyonel", "keywords": ["sağlık", "ivf"], "social_platforms": ["instagram", "facebook"]},
    {"name": "Kemerli Ev Restaurant", "industry": "Restaurant", "description": "Kıbrıs meyhane kültürü", "target_audience": "Yemek severler", "brand_voice": "Sıcak", "keywords": ["meyhane"], "social_platforms": ["instagram", "facebook"]},
    {"name": "Basda Cyprus", "industry": "Food & Beverage", "description": "Sütlü tatlılar", "target_audience": "Tatlı severler", "brand_voice": "Tatlı", "keywords": ["tatlı", "kahve"], "social_platforms": ["instagram", "facebook"]},
    {"name": "Baklava Atölyesi", "industry": "Food", "description": "El yapımı baklava", "target_audience": "Baklava severler", "brand_voice": "Geleneksel", "keywords": ["baklava"], "social_platforms": ["instagram"]},
    {"name": "DJ Soydan Korkmaz", "industry": "Entertainment", "description": "DJ performansları", "target_audience": "Parti", "brand_voice": "Enerjik", "keywords": ["DJ", "müzik"], "social_platforms": ["instagram", "tiktok"]},
    {"name": "Othello Dijital", "industry": "Marketing", "description": "Dijital pazarlama", "target_audience": "İşletmeler", "brand_voice": "Profesyonel", "keywords": ["SEO"], "social_platforms": ["linkedin"]},
    {"name": "Nesdersan", "industry": "E-commerce", "description": "Online alışveriş", "target_audience": "Alışveriş", "brand_voice": "Güvenilir", "keywords": ["elektronik"], "social_platforms": ["instagram"]},
    {"name": "Casa de Mellizo", "industry": "Real Estate", "description": "Konut projeleri", "target_audience": "Ev alıcıları", "brand_voice": "Zarif", "keywords": ["villa"], "social_platforms": ["instagram"]},
]

print("Adding clients to production...")
for client in clients:
    try:
        data = json.dumps(client).encode('utf-8')
        req = urllib.request.Request(
            f"{backend_url}/api/clients/",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            print(f"✓ {client['name']}: Added (ID: {result.get('id')})")
    except Exception as e:
        print(f"✗ {client['name']}: {e}")

print("\n✅ Done!")
