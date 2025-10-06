from openai import OpenAI
from config import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_content(
        self,
        prompt: str,
        platform: str = "instagram",
        tone: str = "professional",
        max_tokens: int = 500
    ) -> Optional[str]:
        """Generate social media content using GPT-4"""
        
        if not self.client:
            return "OpenAI not configured. Please add OPENAI_API_KEY to .env"
        
        system_prompt = f"""You are a professional social media content creator.
Platform: {platform}
Tone: {tone}
Create engaging, authentic content that resonates with the audience.
Include relevant hashtags at the end."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info(f"Generated content for {platform}")
            return content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error generating content: {str(e)}"
    
    def generate_hashtags(
        self,
        topic: str,
        count: int = 10
    ) -> List[str]:
        """Generate relevant hashtags for a topic"""
        
        if not self.client:
            return ["#AI", "#Marketing"]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate relevant hashtags without the # symbol."},
                    {"role": "user", "content": f"Generate {count} hashtags for: {topic}"}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            hashtags_text = response.choices[0].message.content
            hashtags = [f"#{tag.strip()}" for tag in hashtags_text.split() if tag.strip()]
            return hashtags[:count]
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return []

openai_service = OpenAIService()
