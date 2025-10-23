import os
from typing import List, Dict, Any
from openai import OpenAI
import json

class BrandVoiceService:
    """Marka sesi analizi ve içerik üretimi"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
    
    def analyze_brand_voice(self, corpus_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Marka içeriklerini analiz et"""
        
        if not self.openai_client:
            return self._default_voice_profile()
        
        if not corpus_items:
            return self._default_voice_profile()
        
        sample_texts = [item.get('text_content', '')[:300] for item in corpus_items[:20]]
        combined_text = "\n---\n".join(sample_texts)
        
        prompt = f"""Analyze these brand contents and create a BRAND VOICE PROFILE.

CONTENTS:
{combined_text}

Return ONLY valid JSON with these fields:
{{
  "tone": "professional/casual/friendly/authoritative",
  "language_style": "formal/conversational/technical",
  "emoji_usage": "frequent/moderate/minimal/none",
  "content_themes": ["education", "entertainment", "sales"],
  "brand_personality": ["innovative", "trustworthy", "fun"],
  "hashtag_strategy": "3-5 relevant hashtags",
  "voice_summary": "2-3 sentence brand description",
  "confidence_score": 85
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a brand analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            
            voice_profile = json.loads(content)
            voice_profile['sample_size'] = len(corpus_items)
            
            return voice_profile
            
        except Exception as e:
            print(f"❌ Brand voice analysis error: {e}")
            return self._default_voice_profile()
    
    def generate_branded_content(
        self,
        voice_profile: Dict[str, Any],
        prompt: str,
        platform: str = "instagram"
    ) -> str:
        """Generate brand-aligned content"""
        
        if not self.openai_client:
            return "OpenAI API key not configured."
        
        voice_summary = voice_profile.get('voice_summary', '')
        tone = voice_profile.get('tone', 'professional')
        
        system_prompt = f"""You are a brand content creator. Follow this brand voice EXACTLY:

BRAND VOICE:
{voice_summary}

Tone: {tone}
Platform: {platform}

Create content that matches this brand's style perfectly."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            return "Failed to generate content."
    
    def _default_voice_profile(self) -> Dict[str, Any]:
        return {
            "tone": "professional",
            "language_style": "conversational",
            "emoji_usage": "moderate",
            "content_themes": ["general"],
            "brand_personality": ["authentic"],
            "hashtag_strategy": "3-5 relevant hashtags",
            "voice_summary": "Professional brand communication.",
            "confidence_score": 50,
            "sample_size": 0
        }

brand_voice_service = BrandVoiceService()
