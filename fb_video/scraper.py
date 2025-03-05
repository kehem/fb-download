import requests
import re
import json
from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class FacebookResponse:
    """Data class for Facebook video response"""
    url: str
    duration_ms: int
    sd: str
    hd: str
    title: str
    thumbnail: str

    def to_dict(self) -> Dict[str, any]:
        return self.__dict__

class FacebookVideoScraper:
    """Class to handle Facebook video scraping"""
    DEFAULT_HEADERS = {
        "sec-fetch-user": "?1",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-site": "none",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "cache-control": "max-age=0",
        "authority": "www.facebook.com",
        "upgrade-insecure-requests": "1",
        "accept-language": "en-GB,en;q=0.9",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }

    VALID_DOMAINS = {"facebook.com", "fb.watch"}

    @staticmethod
    def _parse_string(string: str) -> str:
        """Parse and clean string input"""
        return string.encode().decode('unicode_escape') if string else ""

    @classmethod
    def get_video_info(cls, video_url: str, cookie: Optional[str] = None, 
                      useragent: Optional[str] = None) -> FacebookResponse:
        """Fetch and parse Facebook video information"""
        if not video_url or not video_url.strip():
            raise ValueError("Please specify the Facebook URL")
        if not any(domain in video_url for domain in cls.VALID_DOMAINS):
            raise ValueError("Please enter a valid Facebook URL")

        headers = cls.DEFAULT_HEADERS.copy()
        if useragent:
            headers["user-agent"] = useragent
        if cookie:
            headers["cookie"] = cookie

        try:
            response = requests.get(video_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.text

            # Define regex patterns once
            PATTERNS = {
                'sd': [
                    r'"browser_native_sd_url":"(.*?)"',
                    r'"playable_url":"(.*?)"',
                    r'sd_src\s*:\s*"([^"]*)"',
                    r'(?<="src":")[^"]*(https:\/\/[^"]*)'
                ],
                'hd': [
                    r'"browser_native_hd_url":"(.*?)"',
                    r'"playable_url_quality_hd":"(.*?)"',
                    r'hd_src\s*:\s*"([^"]*)"'
                ],
                'title': r'<meta\sname="description"\scontent="(.*?)"',
                'title_fallback': r'<title>(.*?)</title>',
                'thumbnail': r'"preferred_thumbnail":{"image":{"uri":"(.*?)"',
                'duration': r'"playable_duration_in_ms":([0-9]+)'
            }

            # Efficient pattern matching
            def get_match(patterns):
                return next((m.group(1) for p in patterns for m in [re.search(p, data)] if m), None)

            sd_url = get_match(PATTERNS['sd'])
            if not sd_url:
                raise ValueError("Unable to fetch video information at this time")

            title = get_match([PATTERNS['title']]) or get_match([PATTERNS['title_fallback']]) or ""

            return FacebookResponse(
                url=video_url,
                duration_ms=int(get_match([PATTERNS['duration']]) or 0),
                sd=cls._parse_string(sd_url),
                hd=cls._parse_string(get_match(PATTERNS['hd']) or ""),
                title=cls._parse_string(title),
                thumbnail=cls._parse_string(get_match([PATTERNS['thumbnail']]) or "")
            )

        except requests.RequestException as err:
            raise ValueError(f"Unable to fetch video information: {err}")

def main():
    """Example usage"""
    try:
        url = "https://www.facebook.com/watch/?v=971981951549911"
        scraper = FacebookVideoScraper()
        video_info = scraper.get_video_info(url)
        print(json.dumps(video_info.to_dict(), indent=2, ensure_ascii=False))
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()