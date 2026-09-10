from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class LLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def analyze(self, content: str, prompt_type: str = "content_analysis") -> Dict[str, Any]:
        """Analyze content and return structured data"""
        pass

class VisionProvider(ABC):
    """Base class for vision providers"""

    @abstractmethod
    async def analyze_image(self, image_url: str) -> Dict[str, Any]:
        """Analyze an image and return description, OCR text, etc."""
        pass

class EmbeddingProvider(ABC):
    """Base class for embedding providers"""

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        pass

class SpeechToTextProvider(ABC):
    """Base class for speech-to-text providers"""

    @abstractmethod
    async def transcribe(self, audio_url: str) -> str:
        """Transcribe audio to text"""
        pass