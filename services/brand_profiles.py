"""Müşteri Brand Profiles"""

BRAND_PROFILES = {
    "baklava_atolyesi": {
        "name": "Baklava Atölyesi",
        "aliases": ["baklava", "atölyesi", "baklava atolyesi"],
        "colors": {"cream": "#9fb9aa", "green": "#828f77", "brown": "#775629"},
        "fonts": {"primary": "New York", "secondary": "Quicksand"},
        "style": {
            "mood": "Geleneksel, organik, doğal",
            "visual_style": "Doğal ışık, toprak tonları"
        }
    },
    "dr_murat_onal": {
        "name": "Op. Dr. Murat Önal",
        "aliases": ["murat", "önal", "onal", "dr murat"],
        "colors": {"white": "#f6f7f8", "blue_gray": "#cbd4d7", "dark": "#45595e"},
        "fonts": {"primary": "Calibri", "secondary": "Poppins"},
        "style": {
            "mood": "Güvenilir, profesyonel, şefkatli",
            "visual_style": "Temiz beyaz, mavi-gri tonları"
        }
    },
    "seluna": {
        "name": "Seluna",
        "aliases": ["seluna"],
        "colors": {"cream": "#e7ddda", "gold": "#ead49c", "navy": "#0f2132"},
        "fonts": {"primary": "Times New Roman", "secondary": "Poppins"},
        "style": {
            "mood": "Lüks, mistik, dönüştürücü",
            "visual_style": "Gold tonları, mistik atmosfer"
        }
    },
    "kemerli_su": {
        "name": "Kemerli Su Restaurant",
        "aliases": ["kemerli", "su", "kemerli su"],
        "colors": {"turquoise": "#288f7e", "gold": "gradient"},
        "fonts": {"primary": "Monsal Gothic", "secondary": "Challystin"},
        "style": {
            "mood": "Modern, elegant, sofistike",
            "visual_style": "Turkuaz & gold, dramatik ışık"
        }
    }
}

def get_brand_profile(client_name: str):
    """Brand profile bul"""
    if not client_name:
        return None
    
    client_lower = client_name.lower().strip()
    
    for key, profile in BRAND_PROFILES.items():
        if profile["name"].lower() == client_lower:
            return profile
        for alias in profile.get("aliases", []):
            if alias.lower() in client_lower:
                return profile
    
    return None

def get_all_brand_profiles():
    """Tüm brand profile'ları döndür"""
    return BRAND_PROFILES
