import requests
import re
import json
from typing import Optional, Dict
from dataclasses import dataclass
import argparse
import base64

@dataclass
class FacebookResponse:
    url: str
    duration_ms: int
    sd: str
    hd: str
    title: str
    thumbnail: str

    def to_dict(self) -> Dict[str, any]:
        return self.__dict__

class FacebookVideoScraper:
    ENCRYPTED_HEADERS = {
        "c2VjLWZldGNoLXVzZXI=": "XjE=",
        "c2VjLWNoLXVhLW1vYmlsZQ==": "XjA=",
        "c2VjLWZldGNoLXNpdGU=": "bm9uZQ==",
        "c2VjLWZldGNoLWRlc3Q=": "ZG9jdW1lbnQ=",
        "c2VjLWZldGNoLW1vZGU=": "bmF2aWdhdGU=",
        "Y2FjaGUtY29udHJvbA==": "bWF4LWFnZT0w",
        "YXV0aG9yaXR5": "d3d3LmZhY2Vib29rLmNvbQ==",
        "dXBncmFkZS1pbnNlY3VyZS1yZXF1ZXN0cw==": "MQ==",
        "YWNjZXB0LWxhbmd1YWdl": "ZW4tR0IsZW47cT0wLjI=",
        "c2VjLWNoLXVh": "Ikdvb2dsZSBDaHJvbWU7dj0iODkiLCBDaHJvbWl1bTt2PSI4OSIsICJOb3QgQSBCcmFuZDt2PSI5OSIn",
        "dXNlci1hZ2VudA==": "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNg==",
        "YWNjZXB0": "dGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44",
    }

    ENCRYPTED_PATTERNS = {
        'sd': [
            "ImJyb3dzZXJfbmF0aXZlX3NkX3VybCI6IiguKj8pIg==",
            "InBsYXlhYmxlX3VybCI6IiguKj8pIg==",
            "c2Rfc3JjXHMqOlxzKiIoW14iXSpcIg==",
            "KD88PSJzcmMiOilbXiJdKihodHRwczpcL1xbXiJdKik="
        ],
        'hd': [
            "ImJyb3dzZXJfbmF0aXZlX2hkX3VybCI6IiguKj8pIg==",
            "InBsYXlhYmxlX3VybF9xdWFsaXR5X2hkIjoiKC4qPyk=",
            "aGRfc3JjXHMqOlxzKiIoW14iXSpcIg=="
        ],
        'title': "PG1ldGFcc25hbWU9ImRlc2NyaXB0aW9uIlxzY29udGVudD0iKC4qPyk=",
        'title_fallback': "PHRpdGxlPigqPyk8L3RpdGxlPg==",
        'thumbnail': "InByZWZlcnJlZF90aHVtYm5haWwiOnsiaW1hZ2UiOnsidXJpIjoiKC4qPyk=",
        'duration': "InBsYXlhYmxlX2R1cmF0aW9uX2luX21zIjpbMC05XSs="
    }

    VALID_DOMAINS = {"facebook.com", "fb.watch"}
    XOR_KEY = 42

    @staticmethod
    def _decrypt_string(encoded: str) -> str:
        decoded = base64.b64decode(encoded).decode('utf-8')
        return ''.join(chr(ord(c) ^ FacebookVideoScraper.XOR_KEY) for c in decoded)

    @classmethod
    def _get_decrypted_headers(cls) -> Dict[str, str]:
        return {cls._decrypt_string(k): cls._decrypt_string(v) 
                for k, v in cls.ENCRYPTED_HEADERS.items()}

    @classmethod
    def _get_decrypted_patterns(cls) -> Dict[str, list]:
        return {
            key: [cls._decrypt_string(pattern) for pattern in patterns]
            if isinstance(patterns, list) else cls._decrypt_string(patterns)
            for key, patterns in cls.ENCRYPTED_PATTERNS.items()
        }

    @staticmethod
    def _parse_string(string: str) -> str:
        return string.encode().decode('unicode_escape') if string else ""

    @classmethod
    def get_video_info(cls, video_url: str, cookie: Optional[str] = None, 
                      useragent: Optional[str] = None) -> FacebookResponse:
        if not video_url or not video_url.strip():
            raise ValueError("Please specify the Facebook URL")
        if not any(domain in video_url for domain in cls.VALID_DOMAINS):
            raise ValueError("Please enter a valid Facebook URL")

        headers = cls._get_decrypted_headers()
        if useragent:
            headers[cls._decrypt_string("dXNlci1hZ2VudA==")] = useragent
        if cookie:
            headers["cookie"] = cookie

        try:
            response = requests.get(video_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.text

            PATTERNS = cls._get_decrypted_patterns()

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
    parser = argparse.ArgumentParser(description='Facebook Video Information Scraper')
    parser.add_argument('--url', type=str, required=True, 
                       help='Facebook video URL to scrape')
    parser.add_argument('--cookie', type=str, 
                       help='Optional Facebook cookie for authenticated requests')
    parser.add_argument('--useragent', type=str,
                       help='Optional custom User-Agent string')

    args = parser.parse_args()

    try:
        scraper = FacebookVideoScraper()
        video_info = scraper.get_video_info(
            video_url=args.url,
            cookie=args.cookie,
            useragent=args.useragent
        )
        print("Video Information:")
        print(json.dumps(video_info.to_dict(), indent=2, ensure_ascii=False))
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()