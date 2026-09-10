from typing import Optional
from .base import ContentExtractor
from .web_extractor import WebExtractor
from .youtube_extractor import YouTubeExtractor

class ExtractorFactory:
    """Factory for getting the appropriate extractor for a URL"""

    def __init__(self):
        self.extractors = [
            YouTubeExtractor(),  # Check YouTube first (more specific)
            WebExtractor(),      # Then general web
            # InstagramExtractor(),  # To be implemented
            # PDFExtractor(),        # To be implemented
        ]

    def get_extractor(self, url: str) -> Optional[ContentExtractor]:
        """Get the appropriate extractor for the given URL"""
        for extractor in self.extractors:
            if extractor.can_handle(url):
                return extractor
        return None

    def extract(self, url: str) -> dict:
        """Extract content using the appropriate extractor"""
        extractor = self.get_extractor(url)
        if extractor:
            return extractor.extract(url)
        else:
            # Fallback to basic web extractor
            return WebExtractor().extract(url)