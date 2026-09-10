from typing import Dict, Any, Optional
import json
import logging
from .base import LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .open_model_provider import OpenModelProvider
from ..config import settings

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered content analysis supporting Open Models and Commercial LLMs"""

    def __init__(self):
        # Select provider based on configuration
        if (
            settings.GROQ_API_KEY
            or settings.OPENROUTER_API_KEY
            or settings.TOGETHER_API_KEY
            or settings.AI_BASE_URL
            or settings.AI_PROVIDER.lower() in ["groq", "openrouter", "together", "ollama", "custom"]
        ):
            open_provider = OpenModelProvider(provider_type=settings.AI_PROVIDER)
            self.llm_provider = open_provider
            self.vision_provider = open_provider
            self.embedding_provider = open_provider
            self.speech_provider = open_provider
            self.fallback_llm = OpenAIProvider() if settings.OPENAI_API_KEY else AnthropicProvider()
        elif settings.OPENAI_API_KEY:
            self.llm_provider = OpenAIProvider()
            self.vision_provider = OpenAIProvider()
            self.embedding_provider = OpenAIProvider()
            self.speech_provider = OpenAIProvider()
            self.fallback_llm = AnthropicProvider()
        elif settings.ANTHROPIC_API_KEY:
            self.llm_provider = AnthropicProvider()
            self.vision_provider = OpenAIProvider()
            self.embedding_provider = OpenAIProvider()
            self.speech_provider = OpenAIProvider()
            self.fallback_llm = OpenModelProvider()
        else:
            default_prov = OpenModelProvider()
            self.llm_provider = default_prov
            self.vision_provider = default_prov
            self.embedding_provider = default_prov
            self.speech_provider = default_prov
            self.fallback_llm = AnthropicProvider()

    async def analyze_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content using AI to extract structured information
        This is the main AI processing step
        """
        try:
            # Prepare the content for analysis
            analysis_text = self._prepare_content_for_analysis(content_data)

            # Use LLM to extract structured information
            structured_data = await self.llm_provider.analyze(
                content=analysis_text,
                prompt_type="content_analysis"
            )

            # If primary provider fails, try fallback
            if not structured_data or "error" in structured_data:
                logger.warning("Primary LLM provider failed, trying fallback")
                structured_data = await self.fallback_llm.analyze(
                    content=analysis_text,
                    prompt_type="content_analysis"
                )

            # Process images if any
            if content_data.get('images'):
                image_analyses = []
                for image in content_data['images']:
                    if image.get('url'):  # Only analyze if we have a URL
                        try:
                            vision_result = await self.vision_provider.analyze_image(
                                image_url=image['url']
                            )
                            image_analyses.append(vision_result)
                        except Exception as e:
                            logger.error(f"Vision analysis failed for image: {e}")
                            image_analyses.append({
                                "error": str(e),
                                "is_important": False
                            })
                structured_data['image_analyses'] = image_analyses

            return structured_data

        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {
                "error": str(e),
                "title": content_data.get('title', 'Untitled'),
                "summary": "Failed to analyze content",
                "category": "unknown"
            }

    def _prepare_content_for_analysis(self, content_data: Dict[str, Any]) -> str:
        """Prepare content data for AI analysis"""
        parts = []

        if content_data.get('title'):
            parts.append(f"Title: {content_data['title']}")

        if content_data.get('caption'):
            parts.append(f"Caption: {content_data['caption']}")

        if content_data.get('text'):
            parts.append(f"Content: {content_data['text'][:2000]}")  # Limit length

        if content_data.get('transcript'):
            parts.append(f"Transcript: {content_data['transcript'][:2000]}")  # Limit length

        return "\n\n".join(parts)

    async def generate_embedding(self, text: str) -> list:
        """Generate embedding for text"""
        try:
            return await self.embedding_provider.embed(text)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            # Return zero vector as fallback
            return [0.0] * 1536  # OpenAI embedding size

    async def transcribe_audio(self, audio_url: str) -> str:
        """Transcribe audio to text"""
        try:
            return await self.speech_provider.transcribe(audio_url)
        except Exception as e:
            logger.error(f"Audio transcription failed: {e}")
            return ""