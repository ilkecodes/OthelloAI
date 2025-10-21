"""
Brand Voice Service - İzole, sadece brand voice işlemleri
"""
import re
import hashlib
from typing import List, Dict

EMBED_DIM = 384

class BrandVoiceService:
    
    def summarize_brand_voice(self, texts: List[str]) -> Dict:
        """Extract brand voice from corpus"""
        
        if not texts:
            return self._empty_profile()
        
        all_txt = "\n".join(texts)
        sentences = [s.strip() for s in re.split(r"[.!?]\s+", all_txt) if s.strip()]
        words = re.findall(r"\w+", all_txt.lower())
        emojis = re.findall(r"[\U0001F300-\U0001FAFF]", all_txt)
        excls = all_txt.count("!")
        qmarks = all_txt.count("?")
        
        avg_sentence_len = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        emoji_rate = len(emojis) / max(1, len(words))
        ex_ratio = excls / max(1, len(sentences))
        q_ratio = qmarks / max(1, len(sentences))
        
        tone = {
            "sicaklik": min(1.0, 0.3 + emoji_rate * 5),
            "mizah": min(1.0, q_ratio * 2 + emoji_rate),
            "enerji": min(1.0, ex_ratio * 3 + 0.2),
            "resmiyet": max(0.0, 1.0 - (emoji_rate * 4 + ex_ratio))
        }
        
        style = {
            "cumle_uzunlugu": "kısa" if avg_sentence_len < 10 else "orta" if avg_sentence_len < 18 else "uzun",
            "emoji_kullanimi": "yüksek" if emoji_rate > 0.01 else "orta" if emoji_rate > 0.002 else "düşük",
            "soru_orani": round(q_ratio, 2),
            "unlem_orani": round(ex_ratio, 2)
        }
        
        lexicon = self._extract_lexicon(words)
        few_shots = self._extract_few_shots(sentences)
        cta_patterns = self._extract_cta_patterns(sentences)
        
        return {
            "tone": tone,
            "style": style,
            "lexicon": lexicon,
            "dos": ["samimi hitap", "kısa cümleler", "net CTA"],
            "donts": ["agresif satış", "abartılı iddia", "çok teknik dil"],
            "cta_patterns": cta_patterns,
            "few_shots": few_shots
        }
    
    def _extract_lexicon(self, words: List[str]) -> List[str]:
        stopwords = set([
            "ve","de","da","ile","için","bir","çok","biz","siz","bu","şu","o",
            "ama","fakat","the","a","to","of","in","on","is","and","or","but"
        ])
        
        freq = {}
        for w in words:
            if w in stopwords or len(w) < 3:
                continue
            freq[w] = freq.get(w, 0) + 1
        
        return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:12]]
    
    def _extract_few_shots(self, sentences: List[str]) -> List[Dict]:
        captions = sorted([s for s in sentences if len(s) > 20], key=lambda s: -len(s))[:3]
        return [{"caption": c, "notes": "yüksek engagement"} for c in captions]
    
    def _extract_cta_patterns(self, sentences: List[str]) -> List[str]:
        cta_keywords = ["hemen", "şimdi", "keşfet", "dene", "yaz", "gönder", "tıkla", "bak"]
        patterns = []
        
        for s in sentences:
            s_lower = s.lower()
            if any(kw in s_lower for kw in cta_keywords):
                patterns.append(s[:50])
        
        return list(set(patterns))[:5]
    
    def _empty_profile(self) -> Dict:
        return {
            "tone": {"sicaklik": 0.5, "mizah": 0.3, "enerji": 0.5, "resmiyet": 0.5},
            "style": {"cumle_uzunlugu": "orta", "emoji_kullanimi": "orta"},
            "lexicon": [],
            "dos": [],
            "donts": [],
            "cta_patterns": [],
            "few_shots": []
        }
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate pseudo-embeddings (replace with OpenAI later)"""
        embeddings = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            vec = [(h[i % len(h)] / 255.0) for i in range(EMBED_DIM)]
            embeddings.append(vec)
        return embeddings

# Singleton
brand_voice_service = BrandVoiceService()
