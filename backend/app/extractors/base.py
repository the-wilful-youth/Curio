from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import urllib.parse

class ContentExtractor(ABC):
    """Base class for all content extractors"""

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Check if this extractor can handle the given URL"""
        pass

    @abstractmethod
    def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from the URL"""
        pass

    def normalize_url(self, url: str) -> str:
        """Normalize URL for comparison"""
        parsed = urllib.parse.urlparse(url)
        # Remove fragments and normalize
        normalized = urllib.parse.urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip('/'),
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        return normalized