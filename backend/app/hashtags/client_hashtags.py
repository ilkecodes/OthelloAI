"""
Client-specific niche hashtags - ASCII only for Instagram compatibility.
"""

CLIENT_HASHTAGS = {
    "Dr. Murat Önal": {
        "primary": [
            "TupBebek",
            "IVFTurkey", 
            "DogurganlikTedavisi",
            "YumurtaDonasyonu"
        ],
        "secondary": [
            "IVFGermany",
            "IVFUK",
            "Infertilite",
            "EmbriyoDondurma"
        ],
        "longtail": [
            "TupBebekMerkeziAnkara",
            "IVFUzmani",
            "DogurganlikDoktoru",
            "IVFBasariHikayeleri"
        ]
    },
    
    "Kemerli Ev Restaurant": {
        "primary": [
            "KuzeyKibrisYemek",
            "GazimagusaRestaurant",
            "LefkosaRestoran",
            "KKTCGastronomi"
        ],
        "secondary": [
            "CyprusFood",
            "NorthCyprusDining",
            "MediterraneanCuisine",
            "GirneYemek"
        ],
        "longtail": [
            "KemerliEvRestaurant",
            "KibrisAksam Yemegi",
            "CyprusFineDining",
            "GastronomyLovers"
        ]
    },
    
    "Basda Cyprus": {
        "primary": [
            "BasdaCyprus",
            "KKTCUrun",
            "CyprusHandmade",
            "KibrisElIsi"
        ],
        "secondary": [
            "CyprusGifts",
            "LocalCyprus",
            "MadeInCyprus",
            "CyprusSouvenirs"
        ],
        "longtail": [
            "BasdaCyprusHediyelik",
            "KKTCYerelUretim",
            "CyprusArtisan",
            "KibrisOzgunUrun"
        ]
    },
    
    "Baklava Atölyesi": {
        "primary": [
            "BaklavaAtolyesi",
            "CyprusDessert",
            "CyprusBaklava",
            "KKTCTatli"
        ],
        "secondary": [
            "BaklavaLove",
            "SweetMoments",
            "TurkishDesserts",
            "GazimagusaDessert"
        ],
        "longtail": [
            "BaklavaAtolyesiKibris",
            "KuzeyKibrisBaklava",
            "TazeBaklava",
            "GelenekselBaklava"
        ]
    },
    
    "DJ Soydan Korkmaz": {
        "primary": [
            "CyprusDJ",
            "CyprusEvents",
            "KKTCEglence",
            "GirneGecesi"
        ],
        "secondary": [
            "NorthCyprusNightlife",
            "CyprusParty",
            "DJLife",
            "LiveMusicCyprus"
        ],
        "longtail": [
            "DJSoydanKorkmaz",
            "KibrisGeceHayati",
            "CyprusClubbing",
            "KKTCEtkinlik"
        ]
    },
    
    "Othello Digital": {
        "primary": [
            "DigitalMarketingCyprus",
            "KKTCDijitalPazarlama",
            "CyprusBranding",
            "SosyalMedyaYonetimi"
        ],
        "secondary": [
            "OthelloDigital",
            "CyprusBusiness",
            "ContentMarketing",
            "InfluencerMarketingCyprus"
        ],
        "longtail": [
            "KuzeyKibrisMarketing",
            "CyprusSocialMedia",
            "KKTCIsGelistirme",
            "DigitalAgencyCyprus"
        ]
    },
    
    "Nesder San": {
        "primary": [
            "NesderSan",
            "KKTCOnlineAlistiris",
            "CyprusShopping",
            "KibrisUrun"
        ],
        "secondary": [
            "OnlineShoppingCyprus",
            "CyprusRetail",
            "KKTCMagaza",
            "NorthCyprusShopping"
        ],
        "longtail": [
            "NesderSanKibris",
            "KKTCHizliTeslimat",
            "CyprusOnlineStore",
            "KuzeyKibrisAlistiris"
        ]
    },
    
    "Casa de Mellizo": {
        "primary": [
            "CasaDeMellizo",
            "KKTCIcMimari",
            "CyprusInteriorDesign",
            "ModernMimariKKTC"
        ],
        "secondary": [
            "CyprusHomes",
            "LuxuryLivingCyprus",
            "InteriorDesignCyprus",
            "KKTCLuxury"
        ],
        "longtail": [
            "CasaDeMellizoCyprus",
            "KKTCEvDekorasyonu",
            "CyprusArchitecture",
            "ModernEvlerKibris"
        ]
    }
}

def get_client_hashtags(client_name: str) -> dict:
    """Get hashtags for a specific client."""
    return CLIENT_HASHTAGS.get(client_name, {
        "primary": [],
        "secondary": [],
        "longtail": []
    })

def get_all_hashtags_for_client(client_name: str, include_longtail: bool = True) -> list:
    """Get all hashtags for a client as a flat list."""
    hashtags = CLIENT_HASHTAGS.get(client_name, {})
    all_tags = hashtags.get("primary", []) + hashtags.get("secondary", [])
    
    if include_longtail:
        all_tags += hashtags.get("longtail", [])
    
    return all_tags

def format_hashtags_for_post(client_name: str, max_count: int = 10) -> str:
    """Format hashtags for a social media post."""
    all_tags = get_all_hashtags_for_client(client_name, include_longtail=False)
    selected_tags = all_tags[:max_count]
    return " ".join([f"#{tag}" for tag in selected_tags])
