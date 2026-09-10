import re
from typing import Dict, Any, Optional
from .base import ContentExtractor

class YouTubeExtractor(ContentExtractor):
    """Extractor for YouTube videos"""

    def can_handle(self, url: str) -> bool:
        """Check if URL is a YouTube URL"""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+'
        ]

        for pattern in youtube_patterns:
            if re.match(pattern, url, re.IGNORECASE):
                return True
        return False

    def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from a YouTube video with real metadata extraction"""
        video_id = self._extract_video_id(url)
        if not video_id:
            return self._empty_result(url)

        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        title = f"YouTube Video ({video_id})"
        description = "YouTube video content"
        creator = "YouTube Creator"

        # Try extracting real metadata via yt-dlp
        try:
            import yt_dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'skip_download': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    title = info.get('title') or title
                    description = info.get('description') or description
                    creator = info.get('uploader') or info.get('channel') or creator
                    if info.get('thumbnail'):
                        thumbnail_url = info.get('thumbnail')
        except Exception:
            # Fallback to no-network/offline basic metadata
            pass

        return {
            'title': title,
            'caption': description[:250] if description else "",
            'text': f"{title}\n\n{description}",
            'transcript': "",
            'images': [{
                'url': thumbnail_url,
                'alt': f"Thumbnail for {title}",
                'type': 'thumbnail'
            }],
            'video': url,
            'creator': creator,
            'published_at': None,
            'source_url': url
        }

    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:v\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
            r'(?:shorts\/)([0-9A-Za-z_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _empty_result(self, url: str) -> Dict[str, Any]:
        """Return empty result when video ID can't be extracted"""
        return {
            'title': '',
            'caption': '',
            'text': 'Unable to extract YouTube video ID',
            'transcript': '',
            'images': [],
            'video': '',
            'creator': '',
            'published_at': None,
            'source_url': url
        }