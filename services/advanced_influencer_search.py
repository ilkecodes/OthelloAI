"""Advanced Influencer Search - Full System"""
from typing import Dict, Optional
import sys
sys.path.append('..')
from services.ai_content_analyzer import (
    generate_smart_hashtags,
    analyze_bio_match,
    analyze_content_consistency
)
from services.multi_search import parallel_hashtag_search, get_detailed_profiles
from services.quality_scorer import calculate_quality_score
from services.authenticity_checker import check_authenticity

async def advanced_influencer_search(
    search_query: str,
    location: Optional[str] = None,
    min_quality_score: int = 40
) -> Dict:
    """
    TAM SİSTEM - Advanced Influencer Search
    
    Steps:
    1. AI generates smart hashtags
    2. Parallel multi-hashtag search
    3. Get detailed profiles
    4. AI analyzes bio & content
    5. Quality scoring
    6. Authenticity check
    7. Filter & sort
    """
    
    print(f"\n{'='*60}")
    print(f"🎯 ADVANCED INFLUENCER SEARCH")
    print(f"Query: {search_query}")
    if location:
        print(f"Location: {location}")
    print(f"{'='*60}\n")
    
    try:
        # STEP 1: Generate Smart Hashtags
        print("STEP 1: 🤖 Generating smart hashtags...")
        hashtags = generate_smart_hashtags(search_query, location)
        print(f"Generated: {hashtags}\n")
        
        # STEP 2: Parallel Multi-Hashtag Search
        print("STEP 2: 🔍 Parallel hashtag search...")
        usernames = parallel_hashtag_search(hashtags, max_posts_per_hashtag=30)
        
        if not usernames:
            return {
                "success": True,
                "query": search_query,
                "location": location,
                "profiles": [],
                "message": "No profiles found"
            }
        
        print(f"\nFound {len(usernames)} unique profiles")
        
        # STEP 3: Get Detailed Profiles
        print("\nSTEP 3: 📊 Getting detailed profiles...")
        profiles = get_detailed_profiles(list(usernames)[:30])
        
        if not profiles:
            return {
                "success": True,
                "query": search_query,
                "location": location,
                "profiles": [],
                "message": "Could not fetch profile details"
            }
        
        print(f"Got {len(profiles)} profiles with data\n")
        
        # STEP 4 & 5 & 6: AI Analysis + Scoring + Authenticity
        print("STEP 4-6: 🧠 AI Analysis, Scoring & Authenticity Check...")
        
        analyzed_profiles = []
        
        for idx, profile in enumerate(profiles, 1):
            print(f"  [{idx}/{len(profiles)}] Analyzing @{profile['username']}...")
            
            # AI Bio Analysis
            bio_analysis = analyze_bio_match(
                profile.get("biography", ""),
                search_query,
                location
            )
            
            # AI Content Consistency
            content_analysis = analyze_content_consistency(
                profile.get("latest_posts", []),
                search_query
            )
            
            # Quality Scoring
            quality_result = calculate_quality_score(
                profile,
                bio_analysis,
                content_analysis
            )
            
            # Authenticity Check
            authenticity_result = check_authenticity(profile)
            
            # Add all analysis to profile
            profile["bio_analysis"] = bio_analysis
            profile["content_analysis"] = content_analysis
            profile["quality_score"] = quality_result["total_score"]
            profile["score_breakdown"] = quality_result["breakdown"]
            profile["tier"] = quality_result["tier"]
            profile["reasons"] = quality_result["reasons"]
            profile["badge"] = quality_result["badge"]
            profile["authenticity"] = authenticity_result
            
            analyzed_profiles.append(profile)
        
        print("\n✅ Analysis complete!\n")
        
        # STEP 7: Filter by quality score
        qualified_profiles = [
            p for p in analyzed_profiles 
            if p["quality_score"] >= min_quality_score 
            and p["authenticity"]["is_authentic"]
        ]
        
        # Sort by quality score
        qualified_profiles.sort(key=lambda x: x["quality_score"], reverse=True)
        
        print(f"📊 RESULTS:")
        print(f"  Total analyzed: {len(analyzed_profiles)}")
        print(f"  Qualified (score ≥ {min_quality_score}): {len(qualified_profiles)}")
        print(f"  Top score: {qualified_profiles[0]['quality_score']:.1f}" if qualified_profiles else "  No qualified profiles")
        print(f"\n{'='*60}\n")
        
        return {
            "success": True,
            "query": search_query,
            "location": location,
            "hashtags_used": hashtags,
            "total_found": len(usernames),
            "analyzed": len(analyzed_profiles),
            "qualified": len(qualified_profiles),
            "profiles": qualified_profiles[:20]  # Top 20
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e),
            "profiles": []
        }
