import os
import json
from typing import List, Dict, Any
from openai import OpenAI

class BrandVoiceService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.openai = OpenAI(api_key=api_key) if api_key else None
        print(f"✅ BrandVoiceService initialized (OpenAI: {bool(self.openai)})")
    
    def embed_texts(self, texts: List[str]) -> List[str]:
        """Generate embeddings and return as JSON strings"""
        if not self.openai:
            return ['[0.0]' * 384 for _ in texts]
        
        try:
            response = self.openai.embeddings.create(
                model="text-embedding-3-small",
                input=[t[:8000] for t in texts]
            )
            # Return as JSON strings for TEXT column
            return [json.dumps(data.embedding) for data in response.data]
        except Exception as e:
            print(f"❌ Embedding error: {e}")
            return ['[0.0]' * 384 for _ in texts]
    
    def summarize_brand_voice(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze texts and create brand voice profile"""
        if not texts:
            return {"error": "No texts provided"}
        
        if not self.openai:
            return {
                "tone": "professional",
                "language_style": "formal",
                "emoji_usage": "moderate",
                "few_shots": texts[:3]
            }
        
        sample = "\n---\n".join(texts[:10])
        
        prompt = f"""Analyze this brand's content:

{sample}

Return ONLY valid JSON:
{{
  "tone": "samimi/profesyonel/eğlenceli",
  "language_style": "günlük/formal/teknik",
  "emoji_usage": "sık/orta/nadir",
  "themes": ["tema1", "tema2"],
  "personality": ["özellik1", "özellik2"],
  "hashtag_strategy": "açıklama",
  "few_shots": ["örnek1", "örnek2"]
}}"""

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a brand analyst. Return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            profile = json.loads(response.choices[0].message.content)
            profile["few_shots"] = texts[:5]
            return profile
            
        except Exception as e:
            print(f"❌ Brand voice analysis error: {e}")
            return {
                "tone": "professional",
                "language_style": "formal",
                "emoji_usage": "moderate",
                "few_shots": texts[:3],
                "error": str(e)
            }

# Create singleton
brand_voice_service = BrandVoiceService()
