import os
from typing import List, Dict, Any, Optional
from apify_client import ApifyClient

class InfluencerDiscovery:
    """Discover and analyze influencers (Instagram) via Apify."""

    def __init__(self):
        # Tokens & actor ids from env (bilerek default vermiyoruz; doğru aktörleri env'den geçir)
        self.apify_token = os.getenv("APIFY_API_TOKEN")
        self.actor_hashtag = os.getenv("APIFY_IG_HASHTAG_ACTOR")  # ör: apify/instagram-hashtag-scraper
        self.actor_profile = os.getenv("APIFY_IG_PROFILE_ACTOR")  # ör: apify/instagram-profile-scraper
        self.actor_search  = os.getenv("APIFY_IG_SEARCH_ACTOR")   # ör: epctex~instagram-search-scraper (bio/isim arama)
        self.actor_place   = os.getenv("APIFY_IG_PLACE_ACTOR")    # ör: (konum/yer araması yapan actor id)

        if self.apify_token:
            self.client = ApifyClient(self.apify_token)
        else:
            self.client = None

    # -------------------------
    # 1) Hashtag bazlı keşif
    # -------------------------
    async def find_niche_influencers(
        self,
        hashtags: List[str],
        min_followers: int = 10_000,
        max_followers: int = 500_000,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find micro/mid-tier influencers via hashtag search."""
        if not self.client or not self.actor_hashtag:
            print("Apify token veya hashtag actor tanımlı değil.")
            return []

        try:
            influencers: List[Dict[str, Any]] = []

            for hashtag in hashtags[:5]:  # rate limit için sınır
                print(f"[Hashtag] #{hashtag} aranıyor...")
                run_input = {"hashtags": [hashtag], "resultsLimit": 50}

                run = self.client.actor(self.actor_hashtag).call(run_input=run_input)

                for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                    owner = item.get("ownerUsername") or item.get("username")
                    followers = (
                        item.get("ownerFollowers")
                        or item.get("followers")
                        or item.get("followersCount")
                        or 0
                    )
                    if not owner:
                        continue

                    if min_followers <= int(followers) <= max_followers:
                        influencers.append({
                            "platform": "instagram",
                            "username": owner,
                            "full_name": item.get("ownerFullName") or item.get("fullName"),
                            "profile_url": f"https://instagram.com/{owner}",
                            "avatar_url": item.get("ownerProfilePicUrl") or item.get("profilePicUrl"),
                            "followers": int(followers),
                            "engagement": item.get("likesCount") or item.get("engagement") or 0,
                            "hashtag": hashtag,
                        })

            return self._dedup_and_sort(influencers, limit=limit)

        except Exception as e:
            print(f"Error in find_niche_influencers: {e}")
            return []

    # -------------------------
    # 2) Bio/isim anahtar kelime araması
    # -------------------------
    async def find_influencers_by_bio(
        self,
        query: str,
        min_followers: int = 5_000,
        max_followers: int = 1_000_000,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Kullanıcı adı / ad-soyad / bio metninde anahtar kelime araması.
        Örn: 'ivf doktor izmir', 'bio: fizyoterapi'
        """
        if not self.client or not self.actor_search:
            print("Apify token veya search actor tanımlı değil.")
            return []

        try:
            print(f"[Search] Bio/isim araması: {query}")
            # Popüler arama actor'leri 'search' ya da 'queries' parametreleri kullanır; ikisini de deneriz.
            possible_inputs = [
                {"search": query, "resultsLimit": 100},
                {"queries": [query], "resultsLimit": 100},
                {"query": query, "resultsLimit": 100},
            ]

            influencers: List[Dict[str, Any]] = []
            run = None
            for run_input in possible_inputs:
                try:
                    run = self.client.actor(self.actor_search).call(run_input=run_input)
                    break
                except Exception as _:
                    continue

            if not run:
                print("Search actor uygun input ile çalıştırılamadı.")
                return []

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                username = item.get("username") or item.get("ownerUsername")
                if not username:
                    continue

                followers = (
                    item.get("followers") or item.get("followersCount") or item.get("ownerFollowers") or 0
                )
                bio_text = item.get("biography") or item.get("bio") or ""

                if min_followers <= int(followers) <= max_followers:
                    influencers.append({
                        "platform": "instagram",
                        "username": username,
                        "full_name": item.get("fullName") or item.get("ownerFullName"),
                        "profile_url": f"https://instagram.com/{username}",
                        "avatar_url": item.get("profilePicUrl") or item.get("ownerProfilePicUrl"),
                        "followers": int(followers),
                        "bio": bio_text,
                        "engagement": item.get("avgEngagement") or item.get("likesCount") or 0,
                        "match_reason": "bio/name search",
                        "query": query,
                    })

            return self._dedup_and_sort(influencers, limit=limit)

        except Exception as e:
            print(f"Error in find_influencers_by_bio: {e}")
            return []

    # -------------------------
    # 3) Konuma göre arama
    # -------------------------
    async def find_influencers_by_location(
        self,
        location_query: str,
        min_followers: int = 2_000,
        max_followers: int = 1_000_000,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Konuma göre içerik ve sahiplerini toplayıp kullanıcıya geri bağlama.
        Konum actor'leri farklı output şemalarına sahip olabildiğinden esnek parse ediyoruz.
        """
        if not self.client or not self.actor_place:
            print("Apify token veya place actor tanımlı değil.")
            return []

        try:
            print(f"[Place] Konum araması: {location_query}")

            possible_inputs = [
                {"search": location_query, "resultsLimit": 100},
                {"placeNames": [location_query], "resultsLimit": 100},
                {"query": location_query, "resultsLimit": 100},
            ]

            influencers: List[Dict[str, Any]] = []
            run = None
            for run_input in possible_inputs:
                try:
                    run = self.client.actor(self.actor_place).call(run_input=run_input)
                    break
                except Exception as _:
                    continue

            if not run:
                print("Place actor uygun input ile çalıştırılamadı.")
                return []

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # Bazı place actor'leri 'posts' altında dönebilir; bazılarında düz item olabilir.
                # Mümkün alanları kontrol ediyoruz:
                owner = (
                    item.get("ownerUsername") or
                    item.get("username") or
                    (item.get("post") or {}).get("ownerUsername")
                )
                if not owner:
                    continue

                followers = (
                    item.get("ownerFollowers") or
                    item.get("followers") or
                    (item.get("post") or {}).get("ownerFollowers") or 0
                )

                if min_followers <= int(followers) <= max_followers:
                    influencers.append({
                        "platform": "instagram",
                        "username": owner,
                        "full_name": item.get("ownerFullName") or item.get("fullName"),
                        "profile_url": f"https://instagram.com/{owner}",
                        "avatar_url": item.get("ownerProfilePicUrl") or item.get("profilePicUrl"),
                        "followers": int(followers),
                        "engagement": item.get("likesCount") or (item.get("post") or {}).get("likesCount") or 0,
                        "location_match": item.get("locationName") or location_query,
                    })

            return self._dedup_and_sort(influencers, limit=limit)

        except Exception as e:
            print(f"Error in find_influencers_by_location: {e}")
            return []

    # -------------------------
    # 4) İçerik stratejisi analizi (opsiyonel 2. katman)
    # -------------------------
    async def analyze_influencer_content(self, username: str) -> Dict[str, Any]:
        """Analyze an influencer's content strategy using profile latest posts."""
        if not self.client or not self.actor_profile:
            return {}

        try:
            run_input = {"username": [username], "resultsLimit": 15}
            run = self.client.actor(self.actor_profile).call(run_input=run_input)

            posts: List[Dict[str, Any]] = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                if item.get("latestPosts"):
                    posts = item["latestPosts"][:15]
                    break

            # İçerik analizi (senin mevcut analyzer'ını kullanıyoruz)
            try:
                from .content_analyzer import ContentAnalyzer
                analyzer = ContentAnalyzer()
                patterns = await analyzer.find_winning_patterns(posts)
            except Exception:
                patterns = {}

            return {
                "username": username,
                "post_count": len(posts),
                "winning_formula": patterns,
            }

        except Exception as e:
            print(f"Error analyzing influencer: {e}")
            return {}

    # -------------------------
    # util
    # -------------------------
    def _dedup_and_sort(self, influencers: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
        seen = set()
        unique: List[Dict[str, Any]] = []
        for inf in influencers:
            u = inf.get("username")
            if not u or u in seen:
                continue
            seen.add(u)
            unique.append(inf)

        # engagement -> followers öncelik sırası
        unique.sort(key=lambda x: (int(x.get("engagement") or 0), int(x.get("followers") or 0)), reverse=True)
        return unique[:limit]
