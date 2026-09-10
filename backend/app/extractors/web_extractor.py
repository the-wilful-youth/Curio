import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from urllib.parse import urljoin, urlparse
import re
from .base import ContentExtractor

class WebExtractor(ContentExtractor):
    """Extractor for general websites"""

    def can_handle(self, url: str) -> bool:
        """Check if URL is a regular website (not YouTube, Instagram, etc.)"""
        parsed = urlparse(url.lower())
        domain = parsed.netloc

        excluded_platforms = [
            'youtube.com', 'youtu.be',
            'instagram.com',
            'linkedin.com',
            'twitter.com', 'x.com',
            'facebook.com', 'fb.com'
        ]

        for platform in excluded_platforms:
            if platform in domain:
                return False

        return parsed.scheme in ['http', 'https']

    def extract(self, url: str) -> Dict[str, Any]:
        """Extract content from a website using trafilatura & BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            response = requests.get(url, headers=headers, timeout=12)
            response.raise_for_status()

            # Attempt clean article extraction with trafilatura
            main_text = ""
            trafilatura_title = ""
            try:
                import trafilatura
                downloaded = response.text
                extracted = trafilatura.extract(downloaded, include_links=True, include_images=True)
                if extracted:
                    main_text = extracted
                metadata = trafilatura.extract_metadata(downloaded)
                if metadata and metadata.title:
                    trafilatura_title = metadata.title
            except Exception:
                pass

            soup = BeautifulSoup(response.content, 'html.parser')

            # Clean scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()

            # Title
            title = trafilatura_title
            if not title:
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else ""

            # Meta description
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                       soup.find('meta', attrs={'property': 'og:description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc.get('content').strip()

            # Fallback text if trafilatura didn't extract
            if not main_text:
                content_container = soup.find('article') or soup.find('main') or soup.body
                if content_container:
                    raw = content_container.get_text()
                else:
                    raw = soup.get_text()
                lines = (line.strip() for line in raw.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                main_text = '\n'.join(chunk for chunk in chunks if chunk)

            # Images
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif not src.startswith(('http://', 'https://')):
                        src = urljoin(url, src)

                    images.append({
                        'url': src,
                        'alt': img.get('alt', ''),
                        'type': 'unknown'
                    })

            return {
                'title': title or "Web Article",
                'caption': description,
                'text': main_text,
                'transcript': '',
                'images': images[:10],
                'video': '',
                'creator': '',
                'published_at': None,
                'source_url': url
            }

        except Exception as e:
            return {
                'title': url,
                'caption': '',
                'text': f"Error extracting content: {str(e)}",
                'transcript': '',
                'images': [],
                'video': '',
                'creator': '',
                'published_at': None,
                'source_url': url
            }