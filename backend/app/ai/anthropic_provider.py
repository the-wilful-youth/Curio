import anthropic
import json
import logging
import os
from typing import Dict, Any, List, Optional
from .base import LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider
from ..config import settings

logger = logging.getLogger(__name__)

class AnthropicProvider(LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider):
    """Anthropic implementation of AI providers"""

    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.model = "claude-3-5-sonnet-20241022"

    async def analyze(self, content: str, prompt_type: str = "content_analysis") -> Dict[str, Any]:
        """Analyze content using Anthropic"""
        if not self.client:
            return {
                "error": "Anthropic API key not configured",
                "title": content.split('\n')[0][:80] if content else "Untitled",
                "summary": content[:300] if content else "",
                "category": "general"
            }

        try:
            prompt = self._load_prompt(prompt_type)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                system=prompt,
                messages=[
                    {"role": "user", "content": content}
                ]
            )

            text_response = response.content[0].text
            try:
                return json.loads(text_response)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except json.JSONDecodeError:
                        pass

                return {
                    "title": "Content Analysis",
                    "summary": text_response[:200] + "..." if len(text_response) > 200 else text_response,
                    "category": "unknown",
                    "raw_response": text_response
                }

        except Exception as e:
            logger.error(f"Anthropic analysis failed: {e}")
            return {"error": str(e)}

    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """Analyze image using Anthropic"""
        return {"error": "Anthropic vision not implemented", "is_important": False}

    async def embed(self, text: str) -> List[float]:
        """Anthropic fallback embedding"""
        return [0.0] * 1536

    async def transcribe(self, audio_url: str) -> str:
        """Anthropic speech-to-text fallback"""
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

        return "Analyze the following content and extract title, summary, category, dates, and key action items in JSON."