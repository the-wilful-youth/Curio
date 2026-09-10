import openai
import json
import logging
import os
from typing import Dict, Any, List, Optional
from .base import LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider
from ..config import settings

logger = logging.getLogger(__name__)

class OpenAIProvider(LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider):
    """OpenAI implementation of AI providers"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o"

    async def analyze(self, content: str, prompt_type: str = "content_analysis") -> Dict[str, Any]:
        """Analyze content using OpenAI"""
        if not self.client:
            return {
                "error": "OpenAI API key not configured",
                "title": content.split('\n')[0][:80] if content else "Untitled",
                "summary": content[:300] if content else "",
                "category": "general"
            }

        try:
            prompt = self._load_prompt(prompt_type)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"OpenAI analysis failed: {e}")
            return {"error": str(e)}

    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """Analyze image using OpenAI Vision"""
        if not self.client:
            return {"error": "OpenAI API key not configured", "is_important": False}

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self._load_prompt("image_analysis")},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=1000
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"OpenAI vision analysis failed: {e}")
            return {"error": str(e)}

    async def embed(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        if not self.client:
            return [0.0] * 1536

        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"OpenAI embedding failed: {e}")
            return [0.0] * 1536

    async def transcribe(self, audio_url: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        logger.warning("Audio transcription not fully implemented")
        return ""

    def _load_prompt(self, prompt_type: str) -> str:
        """Load prompt from file with fallback"""
        try:
            if settings.PROMPTS_DIR:
                prompt_path = os.path.join(settings.PROMPTS_DIR, f"{prompt_type}.txt")
                if os.path.exists(prompt_path):
                    with open(prompt_path, 'r') as f:
                        return f.read()
        except Exception as e:
            logger.debug(f"Could not load prompt file for {prompt_type}: {e}")

        default_prompts = {
            "content_analysis": """You are analyzing content saved by a single user.
Extract title, summary, category, important facts, dates, deadlines, events, action items.
Return JSON with:
{
  "title": "string",
  "summary": "string",
  "category": "string",
  "facts": [],
  "events": [],
  "deadlines": [],
  "action_items": [],
  "important_images": []
}""",
            "image_analysis": """Analyze this image. Return JSON with description, is_informative, ocr_text, image_type, importance_score."""
        }
        return default_prompts.get(prompt_type, "Analyze the following content and extract structured information.")