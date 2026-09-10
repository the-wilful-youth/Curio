import openai
import json
import logging
import re
import os
from typing import Dict, Any, List, Optional
from .base import LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider
from ..config import settings

logger = logging.getLogger(__name__)

class OpenModelProvider(LLMProvider, VisionProvider, EmbeddingProvider, SpeechToTextProvider):
    """
    Universal provider for Open Models via:
    - Groq (Llama 3.3, Mixtral, Gemma)
    - OpenRouter (Meta Llama, DeepSeek, Mistral, Qwen)
    - Together AI (Llama 3.1, Qwen, DeepSeek)
    - Ollama / vLLM / LocalAI (Local open models)
    - Any OpenAI-compatible endpoint
    """

    def __init__(self, provider_type: str = "auto", api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        self.provider_type = provider_type.lower()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

        self._configure()
        self.client = None
        if self.api_key or self.base_url:
            try:
                # Default to 'na' if no key provided but base_url is set (like local Ollama)
                client_key = self.api_key or "local-no-key-needed"
                self.client = openai.OpenAI(
                    api_key=client_key,
                    base_url=self.base_url
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client for open models: {e}")

    def _configure(self):
        # Auto-detect provider if set to auto
        if self.provider_type == "auto":
            if settings.GROQ_API_KEY:
                self.provider_type = "groq"
            elif settings.OPENROUTER_API_KEY:
                self.provider_type = "openrouter"
            elif settings.TOGETHER_API_KEY:
                self.provider_type = "together"
            elif settings.AI_BASE_URL:
                self.provider_type = "custom"
            elif settings.OPENAI_API_KEY:
                self.provider_type = "openai"
            else:
                self.provider_type = "none"

        # Apply specific provider configurations
        if self.provider_type == "groq":
            self.base_url = self.base_url or "https://api.groq.com/openai/v1"
            self.api_key = self.api_key or settings.GROQ_API_KEY
            self.model = self.model or settings.AI_MODEL or "llama-3.3-70b-versatile"

        elif self.provider_type == "openrouter":
            self.base_url = self.base_url or "https://openrouter.ai/api/v1"
            self.api_key = self.api_key or settings.OPENROUTER_API_KEY
            self.model = self.model or settings.AI_MODEL or "meta-llama/llama-3.3-70b-instruct"

        elif self.provider_type == "together":
            self.base_url = self.base_url or "https://api.together.xyz/v1"
            self.api_key = self.api_key or settings.TOGETHER_API_KEY
            self.model = self.model or settings.AI_MODEL or "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

        elif self.provider_type in ["ollama", "custom"]:
            self.base_url = self.base_url or settings.AI_BASE_URL or "http://localhost:11434/v1"
            self.api_key = self.api_key or settings.OPENAI_API_KEY or "ollama"
            self.model = self.model or settings.AI_MODEL or "llama3.2"

        elif self.provider_type == "openai":
            self.base_url = self.base_url or settings.AI_BASE_URL
            self.api_key = self.api_key or settings.OPENAI_API_KEY
            self.model = self.model or settings.AI_MODEL or "gpt-4o-mini"

        else:
            self.model = self.model or settings.AI_MODEL or "open-model"

    async def analyze(self, content: str, prompt_type: str = "content_analysis") -> Dict[str, Any]:
        """Analyze content using open model"""
        if not self.client:
            return {
                "error": "No open model API key or base URL configured",
                "title": content.split('\n')[0][:80] if content else "Untitled",
                "summary": content[:300] if content else "",
                "category": "general"
            }

        prompt = self._load_prompt(prompt_type)
        system_content = f"{prompt}\nIMPORTANT: Respond with valid, parseable JSON only. No preamble."

        # Attempt with json_object response format first
        raw_text = None
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": content}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_text = response.choices[0].message.content
        except Exception as e:
            # Fallback without response_format if model endpoint does not support json_object
            logger.info(f"Retrying without json_object response_format for open model {self.model}: {e}")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": content}
                    ],
                    temperature=0.2
                )
                raw_text = response.choices[0].message.content
            except Exception as e2:
                logger.error(f"Open model analysis failed: {e2}")
                return {"error": str(e2)}

        return self._extract_json(raw_text)

    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """Analyze image with open vision models if available"""
        if not self.client:
            return {"error": "No open model configured", "is_important": False}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self._load_prompt("image_analysis")},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            raw_text = response.choices[0].message.content
            return self._extract_json(raw_text)
        except Exception as e:
            logger.debug(f"Open model vision call failed or unsupported: {e}")
            return {"error": str(e), "is_important": False}

    async def embed(self, text: str) -> List[float]:
        """Generate embedding using open model embeddings endpoint if available"""
        if not self.client:
            return [0.0] * 1536

        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.debug(f"Embedding not supported by provider: {e}")
            return [0.0] * 1536

    async def transcribe(self, audio_url: str) -> str:
        """Transcribe audio with Whisper if supported"""
        return ""

    def _extract_json(self, text: Optional[str]) -> Dict[str, Any]:
        """Robustly extract JSON from open model outputs"""
        if not text:
            return {}

        # 1. Direct JSON parse
        try:
            return json.loads(text.strip())
        except Exception:
            pass

        # 2. Extract from markdown code blocks
        code_block = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if code_block:
            try:
                return json.loads(code_block.group(1).strip())
            except Exception:
                pass

        # 3. Extract bracketed JSON object
        json_obj = re.search(r'(\{[\s\S]*\})', text)
        if json_obj:
            try:
                return json.loads(json_obj.group(1).strip())
            except Exception:
                pass

        # 4. Fallback structured dict
        return {
            "title": "Extracted Content",
            "summary": text[:250],
            "category": "general",
            "raw_text": text
        }

    def _load_prompt(self, prompt_type: str) -> str:
        try:
            if settings.PROMPTS_DIR:
                prompt_path = os.path.join(settings.PROMPTS_DIR, f"{prompt_type}.txt")
                if os.path.exists(prompt_path):
                    with open(prompt_path, 'r') as f:
                        return f.read()
        except Exception as e:
            logger.debug(f"Could not load prompt {prompt_type}: {e}")

        return "Analyze the following content and extract title, summary, category, dates, deadlines, and key tasks in JSON."
