import os
from typing import Dict, Any, List
from openai import OpenAI

class ContentAnalyzer:
    """Deep content analysis beyond captions."""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_post_deeply(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze post structure, hooks, CTAs, engagement patterns."""
        
        caption = post.get('caption', '')
        likes = post.get('likesCount', 0)
        comments = post.get('commentsCount', 0)
        engagement_rate = (likes + comments * 2) / max(likes, 1)
        
        prompt = f"""Bu Instagram post'unu detaylı analiz et:

CAPTION:
{caption}

ENGAGEMENT:
- Likes: {likes}
- Comments: {comments}
- Engagement Rate: {engagement_rate:.2f}

ANALİZ ET:
1. HOOK (İlk Cümle): Nasıl dikkat çekiyor?
2. STRUCTURE (Yapı): Hikaye mi, liste mi, soru-cevap mı?
3. EMOTIONAL TRIGGER (Duygusal Tetikleyici): Hangi duyguya hitap ediyor?
4. CTA (Call-to-Action): Ne tür eylem istiyor?
5. HASHTAG PLACEMENT: Hashtag'ler nerede ve kaç tane?
6. LENGTH: Kısa mı uzun mu?
7. VALUE PROPOSITION: Ne değer sunuyor?
8. WHY IT WORKS: Neden yüksek engagement almış?

JSON formatında çıktı ver:
{{
  "hook_type": "",
  "structure_type": "",
  "emotional_trigger": "",
  "cta_type": "",
  "hashtag_strategy": "",
  "length_category": "",
  "value_type": "",
  "success_factors": []
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen bir sosyal medya analisti ve content stratejistisin."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return {}
    
    async def find_winning_patterns(self, posts: List[Dict]) -> Dict[str, Any]:
        """Find common patterns in high-performing posts."""
        
        if not posts:
            return {}
        
        high_performers = sorted(posts, key=lambda x: x.get('likesCount', 0), reverse=True)[:5]
        
        # Simple analysis without deep AI for each post
        captions = [p.get('caption', '')[:200] for p in high_performers]
        
        prompt = f"""Analyze these {len(captions)} high-performing Instagram captions:

{chr(10).join([f"{i+1}. {c}" for i, c in enumerate(captions)])}

Find COMMON PATTERNS and respond ONLY with valid JSON:

{{
  "best_hook_type": "question|statement|emoji|story",
  "best_structure": "short|medium|long",
  "emotional_triggers": ["curiosity", "urgency", "joy"],
  "cta_strategy": "dm|link|comment|tag",
  "hashtag_count": 3,
  "optimal_length": "short|medium|long",
  "content_themes": ["education", "promotion", "engagement"]
}}

IMPORTANT: Return ONLY the JSON object, no extra text."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a data analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            
            import json
            patterns = json.loads(content)
            print(f"✅ Patterns found: {patterns}")
            return patterns
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Response was: {content[:200]}")
            return {
                "best_hook_type": "statement",
                "best_structure": "medium",
                "emotional_triggers": ["interest"],
                "cta_strategy": "dm",
                "hashtag_count": 3,
                "optimal_length": "medium",
                "content_themes": ["general"]
            }
        except Exception as e:
            print(f"❌ Error finding patterns: {e}")
            return {}
