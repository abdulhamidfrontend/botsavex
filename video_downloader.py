import requests
import re
import json
import os
from urllib.parse import urlparse, parse_qs
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_instagram_video(self, url: str) -> Optional[str]:
        """Extract video URL from Instagram post/reel"""
        try:
            # Clean the URL
            if '?' in url:
                url = url.split('?')[0]
            
            # Try different methods to extract video - using popular working methods
            methods = [
                self._extract_instagram_direct_api,     # Direct Instagram API (most reliable)
                self._extract_instagram_web_scraping,   # Web scraping method
                self._extract_instagram_savefrom,       # SaveFrom.net method
                self._extract_instagram_sssinstagram,   # SSSInstagram method
                self._extract_instagram_instadownload,  # InstaDownload method
                self._extract_instagram_igram,          # iGram method
                self._extract_instagram_instadownloader, # InstaDownloader method
                self._extract_instagram_instagramdownloader, # InstagramDownloader method
                self._extract_instagram_method1,        # Original method as fallback
            ]
            
            for i, method in enumerate(methods, 1):
                try:
                    result = method(url)
                    if result:
                        logger.info(f"Instagram method {i} succeeded")
                        return result
                except Exception as e:
                    logger.error(f"Instagram method {i} failed: {e}")
                    continue
            
            logger.warning("All Instagram extraction methods failed")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting Instagram video: {e}")
            return None
    
    def _extract_instagram_method1(self, url: str) -> Optional[str]:
        """Method 1: Using Instagram embed with updated approach"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # Use Instagram embed page
                embed_url = f"https://www.instagram.com/p/{shortcode}/embed/"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                response = self.session.get(embed_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    # Look for video URL in embed page
                    video_patterns = [
                        r'"video_url":"([^"]+)"',
                        r'<meta property="og:video" content="([^"]+)"',
                        r'<video[^>]+src="([^"]+)"',
                        r'"contentUrl":"([^"]+)"',
                        r'"playbackUrl":"([^"]+)"'
                    ]
                    
                    for pattern in video_patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            video_url = match.group(1).replace('\\u0026', '&')
                            if video_url.startswith('http'):
                                return video_url
        except Exception as e:
            logger.error(f"Instagram method 1 failed: {e}")
        return None
    
    def _extract_instagram_method2(self, url: str) -> Optional[str]:
        """Method 2: Using Instagram web scraping with updated headers"""
        try:
            # Update headers to mimic mobile browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # Look for video URL in page source
                video_patterns = [
                    r'"video_url":"([^"]+)"',
                    r'<meta property="og:video" content="([^"]+)"',
                    r'<video[^>]+src="([^"]+)"',
                    r'"contentUrl":"([^"]+)"'
                ]
                
                for pattern in video_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        video_url = match.group(1).replace('\\u0026', '&')
                        if video_url.startswith('http'):
                            return video_url
        except Exception as e:
            logger.error(f"Instagram method 2 failed: {e}")
        return None
    
    def _extract_instagram_method3(self, url: str) -> Optional[str]:
        """Method 3: Using Instagram API with session cookies"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # First get the page to get cookies
                page_response = self.session.get(url, timeout=10)
                if page_response.status_code == 200:
                    # Try to get video info from page data
                    data_pattern = r'<script type="text/javascript">window\._sharedData = (.+?);</script>'
                    match = re.search(data_pattern, page_response.text)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                            if 'entry_data' in data and 'PostPage' in data['entry_data']:
                                media = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
                                if media.get('is_video'):
                                    return media.get('video_url')
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            logger.error(f"Instagram method 3 failed: {e}")
        return None
    
    def _extract_instagram_method4(self, url: str) -> Optional[str]:
        """Method 4: Using Instagram web scraping"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # Look for video URL in page source
                video_patterns = [
                    r'"video_url":"([^"]+)"',
                    r'<meta property="og:video" content="([^"]+)"',
                    r'<video[^>]+src="([^"]+)"'
                ]
                
                for pattern in video_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        video_url = match.group(1).replace('\\u0026', '&')
                        if video_url.startswith('http'):
                            return video_url
        except Exception as e:
            logger.error(f"Instagram method 4 failed: {e}")
        return None
    
    def _extract_instagram_method5(self, url: str) -> Optional[str]:
        """Method 5: Using Instagram GraphQL API"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # Use Instagram's GraphQL API
                graphql_url = "https://www.instagram.com/graphql/query/"
                
                variables = {
                    "shortcode": shortcode
                }
                
                params = {
                    "query_hash": "9f8827793ef34641b2fb195d4d41151c",
                    "variables": json.dumps(variables)
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Referer': 'https://www.instagram.com/',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                
                response = self.session.get(graphql_url, params=params, headers=headers, timeout=10)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'data' in data and 'shortcode_media' in data['data']:
                            media = data['data']['shortcode_media']
                            if media.get('is_video'):
                                return media.get('video_url')
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.error(f"Instagram method 5 failed: {e}")
        return None
    
    def _extract_instagram_method6(self, url: str) -> Optional[str]:
        """Method 6: Using Instagram mobile API with session"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # First get the main page to establish session
                main_url = f"https://www.instagram.com/p/{shortcode}/"
                response = self.session.get(main_url, timeout=10)
                
                if response.status_code == 200:
                    # Look for video URL in the page source
                    video_patterns = [
                        r'"video_url":"([^"]+)"',
                        r'"contentUrl":"([^"]+)"',
                        r'<meta property="og:video" content="([^"]+)"',
                        r'<video[^>]+src="([^"]+)"',
                        r'"playbackUrl":"([^"]+)"'
                    ]
                    
                    for pattern in video_patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            video_url = match.group(1).replace('\\u0026', '&')
                            if video_url.startswith('http'):
                                return video_url
        except Exception as e:
            logger.error(f"Instagram method 6 failed: {e}")
        return None
    
    def _extract_instagram_method7(self, url: str) -> Optional[str]:
        """Method 7: Using Instagram API with different endpoint"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # Try different API endpoint
                api_url = f"https://www.instagram.com/api/v1/media/{shortcode}/info/"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                
                response = self.session.get(api_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'items' in data and len(data['items']) > 0:
                            item = data['items'][0]
                            if item.get('media_type') == 2:  # Video
                                video_versions = item.get('video_versions', [])
                                if video_versions:
                                    # Get the highest quality video
                                    best_video = max(video_versions, key=lambda x: x.get('width', 0) * x.get('height', 0))
                                    return best_video.get('url')
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            logger.error(f"Instagram method 7 failed: {e}")
        return None
    
    def _extract_instagram_method8(self, url: str) -> Optional[str]:
        """Method 8: Using Instagram with session cookies and different approach"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # First visit Instagram homepage to get cookies
                self.session.get("https://www.instagram.com/", timeout=10)
                
                # Then try to get the post page
                post_url = f"https://www.instagram.com/p/{shortcode}/"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                response = self.session.get(post_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    # Look for video URL in the page source with more patterns
                    video_patterns = [
                        r'"video_url":"([^"]+)"',
                        r'"contentUrl":"([^"]+)"',
                        r'<meta property="og:video" content="([^"]+)"',
                        r'<video[^>]+src="([^"]+)"',
                        r'"playbackUrl":"([^"]+)"',
                        r'"video_versions":\[[^\]]*"url":"([^"]+)"',
                        r'"display_url":"([^"]+)"'
                    ]
                    
                    for pattern in video_patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            video_url = match.group(1).replace('\\u0026', '&')
                            if video_url.startswith('http'):
                                return video_url
        except Exception as e:
            logger.error(f"Instagram method 8 failed: {e}")
        return None
    
    def _extract_instagram_method9(self, url: str) -> Optional[str]:
        """Method 9: Using working Instagram downloader"""
        try:
            # Use a working Instagram downloader service
            api_url = "https://api.instagram-downloader.com/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 9 failed: {e}")
        return None
    
    def _extract_instagram_method10(self, url: str) -> Optional[str]:
        """Method 10: Using working Instagram downloader API"""
        try:
            # Use a working Instagram downloader API
            api_url = "https://api.instagram-downloader.net/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.net/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 10 failed: {e}")
        return None
    
    def _extract_instagram_method11(self, url: str) -> Optional[str]:
        """Method 11: Using Instagram downloader API (most popular)"""
        try:
            # Use the most popular Instagram downloader API
            api_url = "https://instagram-downloader-download-instagram-photos-and-videos.p.rapidapi.com/api/instagram"
            
            headers = {
                'X-RapidAPI-Key': 'your-api-key-here',  # This would need a real API key
                'X-RapidAPI-Host': 'instagram-downloader-download-instagram-photos-and-videos.p.rapidapi.com',
                'Content-Type': 'application/json'
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 11 failed: {e}")
        return None
    
    def _extract_instagram_method12(self, url: str) -> Optional[str]:
        """Method 12: Using free Instagram downloader service"""
        try:
            # Use a free Instagram downloader service
            api_url = "https://api.instagram-downloader.org/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.org/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 12 failed: {e}")
        return None
    
    def _extract_instagram_method13(self, url: str) -> Optional[str]:
        """Method 13: Using a different Instagram downloader service"""
        try:
            # Use a different Instagram downloader service
            api_url = "https://api.instagram-downloader.com/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'data' in data and 'video_url' in data['data']:
                        return data['data']['video_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 13 failed: {e}")
        return None
    
    def _extract_instagram_method14(self, url: str) -> Optional[str]:
        """Method 14: Using a more reliable Instagram downloader service"""
        try:
            # Use a more reliable Instagram downloader service
            api_url = "https://api.instagram-downloader.com/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'data' in data and 'video_url' in data['data']:
                        return data['data']['video_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 14 failed: {e}")
        return None
    
    def _extract_instagram_method15(self, url: str) -> Optional[str]:
        """Method 15: Using a different Instagram downloader service"""
        try:
            # Use a different Instagram downloader service
            api_url = "https://api.instagram-downloader.net/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.net/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 15 failed: {e}")
        return None
    
    def _extract_instagram_method16(self, url: str) -> Optional[str]:
        """Method 16: Using a working Instagram downloader service"""
        try:
            # Use a working Instagram downloader service
            api_url = "https://api.instagram-downloader.org/api/instagram"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagram-downloader.org/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                    elif 'data' in data and 'video_url' in data['data']:
                        return data['data']['video_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Instagram method 16 failed: {e}")
        return None
    
    def _extract_instagram_method17(self, url: str) -> Optional[str]:
        """Method 17: Using Instagram web scraping with better headers"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if shortcode_match:
                shortcode = shortcode_match.group(1)
                
                # Use Instagram embed page with better headers
                embed_url = f"https://www.instagram.com/p/{shortcode}/embed/"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                }
                
                response = self.session.get(embed_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    # Look for video URL in embed page with more patterns
                    video_patterns = [
                        r'"video_url":"([^"]+)"',
                        r'<meta property="og:video" content="([^"]+)"',
                        r'<video[^>]+src="([^"]+)"',
                        r'"contentUrl":"([^"]+)"',
                        r'"playbackUrl":"([^"]+)"',
                        r'"media_url":"([^"]+)"',
                        r'"display_url":"([^"]+)"',
                        r'"video_versions":\[[^\]]*"url":"([^"]+)"',
                    ]
                    
                    for pattern in video_patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            video_url = match.group(1).replace('\\u0026', '&')
                            if video_url.startswith('http'):
                                return video_url
        except Exception as e:
            logger.error(f"Instagram method 17 failed: {e}")
        return None
    
    def _extract_instagram_direct_api(self, url: str) -> Optional[str]:
        """Method: Direct Instagram API call"""
        try:
            # Extract shortcode from URL
            shortcode_match = re.search(r'/p/([^/]+)/', url) or re.search(r'/reel/([^/]+)/', url)
            if not shortcode_match:
                return None
            
            shortcode = shortcode_match.group(1)
            
            # Use Instagram's public API
            api_url = f"https://www.instagram.com/p/{shortcode}/?__a=1&__d=1"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(api_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Try to extract video URL from response
            content = response.text
            
            # Look for video URL patterns
            video_patterns = [
                r'"video_url":"([^"]+)"',
                r'"video_url":"([^"]+)"',
                r'"display_url":"([^"]+\.mp4[^"]*)"',
                r'"video_versions":\[[^\]]*"url":"([^"]+)"',
            ]
            
            for pattern in video_patterns:
                match = re.search(pattern, content)
                if match:
                    video_url = match.group(1)
                    # Clean the URL
                    video_url = video_url.replace('\\/', '/').replace('\\u0026', '&').replace('\\u00253D', '=')
                    return video_url
            
            return None
            
        except Exception as e:
            logger.error(f"Direct API method failed: {e}")
            return None

    def _extract_instagram_web_scraping(self, url: str) -> Optional[str]:
        """Method: Web scraping Instagram page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            content = response.text
            
            # Look for video URL patterns in the page source
            video_patterns = [
                r'"video_url":"([^"]+)"',
                r'"display_url":"([^"]+\.mp4[^"]*)"',
                r'"video_versions":\[[^\]]*"url":"([^"]+)"',
                r'<meta property="og:video" content="([^"]+)"',
                r'<meta property="og:video:url" content="([^"]+)"',
            ]
            
            for pattern in video_patterns:
                match = re.search(pattern, content)
                if match:
                    video_url = match.group(1).replace('\\u0026', '&')
                    return video_url
            
            return None
            
        except Exception as e:
            logger.error(f"Web scraping method failed: {e}")
            return None

    def _extract_instagram_savefrom(self, url: str) -> Optional[str]:
        """Method: Using SaveFrom.net API"""
        try:
            api_url = "https://savefrom.net/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://savefrom.net/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"SaveFrom method failed: {e}")
            return None

    def _extract_instagram_sssinstagram(self, url: str) -> Optional[str]:
        """Method: Using SSSInstagram API"""
        try:
            api_url = "https://sssinstagram.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://sssinstagram.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"SSSInstagram method failed: {e}")
            return None

    def _extract_instagram_instadownload(self, url: str) -> Optional[str]:
        """Method: Using InstaDownload API"""
        try:
            api_url = "https://instadownload.co/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instadownload.co/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"InstaDownload method failed: {e}")
            return None

    def _extract_instagram_igram(self, url: str) -> Optional[str]:
        """Method: Using iGram API"""
        try:
            api_url = "https://igram.world/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://igram.world/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"iGram method failed: {e}")
            return None

    def _extract_instagram_instadownloader(self, url: str) -> Optional[str]:
        """Method: Using InstaDownloader API"""
        try:
            api_url = "https://instadownloader.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instadownloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"InstaDownloader method failed: {e}")
            return None

    def _extract_instagram_instagramdownloader(self, url: str) -> Optional[str]:
        """Method: Using InstagramDownloader API"""
        try:
            api_url = "https://instagramdownloader.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://instagramdownloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, headers=headers, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if 'url' in result and result['url']:
                return result['url']
            
            return None
            
        except Exception as e:
            logger.error(f"InstagramDownloader method failed: {e}")
            return None
    
    def extract_tiktok_video(self, url: str) -> Optional[str]:
        """Extract video URL from TikTok video"""
        try:
            # Try different methods to extract TikTok video
            methods = [
                self._extract_tiktok_direct_api,    # Direct TikTok API (most reliable)
                self._extract_tiktok_web_scraping,  # Web scraping method
                self._extract_tiktok_snaptik,       # Snaptik method
                self._extract_tiktok_ssstiktok,     # SSS TikTok method
                self._extract_tiktok_tikmate,       # TikMate method
                self._extract_tiktok_savetiktok,    # SaveTikTok method
                self._extract_tiktok_tikdownloader, # TikTok Downloader method
                self._extract_tiktok_method1,       # Original method as fallback
                self._extract_tiktok_method2,       # Web scraping method
                self._extract_tiktok_method3        # Mobile API method
            ]
            
            for method in methods:
                try:
                    video_url = method(url)
                    if video_url:
                        logger.info(f"TikTok video extracted successfully: {video_url}")
                        return video_url
                except Exception as e:
                    logger.error(f"TikTok method failed: {e}")
                    continue
            
            logger.warning("All TikTok extraction methods failed")
            return None
        except Exception as e:
            logger.error(f"Error extracting TikTok video: {e}")
            return None
    
    def _extract_tiktok_direct_api(self, url: str) -> Optional[str]:
        """Method: Direct TikTok API call"""
        try:
            # Extract video ID from URL
            video_id = self.extract_tiktok_video_id(url)
            if not video_id:
                return None
            
            # Use TikTok's public API
            api_url = f"https://www.tiktok.com/api/item/detail/?itemId={video_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://www.tiktok.com/',
            }
            
            response = self.session.get(api_url, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'itemInfo' in data and 'itemStruct' in data['itemInfo']:
                        item = data['itemInfo']['itemStruct']
                        if 'video' in item and 'playAddr' in item['video']:
                            video_url = item['video']['playAddr'][0]
                            if video_url.startswith('//'):
                                video_url = 'https:' + video_url
                            return video_url
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"TikTok direct API method failed: {e}")
        return None
    
    def _extract_tiktok_web_scraping(self, url: str) -> Optional[str]:
        """Method: TikTok web scraping"""
        try:
            # Get the TikTok page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                content = response.text
                
                # Look for video URL patterns
                patterns = [
                    r'"playAddr":"([^"]+)"',
                    r'"downloadAddr":"([^"]+)"',
                    r'"playAddrNoWatermark":"([^"]+)"',
                    r'"video":{"playAddr":"([^"]+)"',
                    r'"video":{"downloadAddr":"([^"]+)"',
                    r'"playAddr":\["([^"]+)"',
                    r'"downloadAddr":\["([^"]+)"',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        video_url = match.replace('\\u002F', '/').replace('\\u0026', '&')
                        if video_url.startswith('//'):
                            video_url = 'https:' + video_url
                        if 'http' in video_url and '.mp4' in video_url:
                            return video_url
        except Exception as e:
            logger.error(f"TikTok web scraping method failed: {e}")
        return None
    
    def _extract_tiktok_snaptik(self, url: str) -> Optional[str]:
        """Method: Using Snaptik API"""
        try:
            api_url = "https://snaptik.app/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://snaptik.app/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"Snaptik method failed: {e}")
        return None
    
    def _extract_tiktok_ssstiktok(self, url: str) -> Optional[str]:
        """Method: Using SSS TikTok API"""
        try:
            api_url = "https://ssstiktok.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://ssstiktok.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"SSS TikTok method failed: {e}")
        return None
    
    def _extract_tiktok_tikmate(self, url: str) -> Optional[str]:
        """Method: Using TikMate API"""
        try:
            api_url = "https://tikmate.app/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://tikmate.app/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"TikMate method failed: {e}")
        return None
    
    def _extract_tiktok_savetiktok(self, url: str) -> Optional[str]:
        """Method: Using SaveTikTok API"""
        try:
            api_url = "https://savetiktok.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://savetiktok.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"SaveTikTok method failed: {e}")
        return None
    
    def _extract_tiktok_tikdownloader(self, url: str) -> Optional[str]:
        """Method: Using TikTok Downloader API"""
        try:
            api_url = "https://tiktok-downloader.com/api/convert"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://tiktok-downloader.com/',
            }
            
            data = {
                'url': url
            }
            
            response = self.session.post(api_url, data=data, headers=headers, timeout=15)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'video_url' in data:
                        return data['video_url']
                    elif 'url' in data:
                        return data['url']
                    elif 'download_url' in data:
                        return data['download_url']
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.error(f"TikTok Downloader method failed: {e}")
        return None
    
    def _extract_tiktok_method1(self, url: str) -> Optional[str]:
        """Method 1: Using TikTok API"""
        try:
            video_id = self.extract_tiktok_video_id(url)
            if video_id:
                api_url = f"https://www.tiktok.com/api/item/detail/?itemId={video_id}"
                response = self.session.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'itemInfo' in data:
                        video_url = data['itemInfo']['itemStruct']['video']['playAddr']
                        return video_url
        except Exception as e:
            logger.error(f"TikTok method 1 failed: {e}")
        return None
    
    def _extract_tiktok_method2(self, url: str) -> Optional[str]:
        """Method 2: Using TikTok web scraping"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # Look for video URL in page source
                video_patterns = [
                    r'"downloadAddr":"([^"]+)"',
                    r'"playAddr":"([^"]+)"',
                    r'<video[^>]+src="([^"]+)"'
                ]
                
                for pattern in video_patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        video_url = match.group(1).replace('\\u0026', '&')
                        if video_url.startswith('http'):
                            return video_url
        except Exception as e:
            logger.error(f"TikTok method 2 failed: {e}")
        return None
    
    def _extract_tiktok_method3(self, url: str) -> Optional[str]:
        """Method 3: Using TikTok mobile API"""
        try:
            video_id = self.extract_tiktok_video_id(url)
            if video_id:
                api_url = f"https://api.tiktok.com/api/item/detail/?itemId={video_id}"
                response = self.session.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'itemInfo' in data:
                        video_url = data['itemInfo']['itemStruct']['video']['playAddr']
                        return video_url
        except Exception as e:
            logger.error(f"TikTok method 3 failed: {e}")
        return None
    
    def extract_tiktok_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from TikTok URL"""
        try:
            # First, if it's a vt.tiktok.com URL, we need to follow the redirect
            if 'vt.tiktok.com' in url:
                try:
                    response = self.session.get(url, allow_redirects=True, timeout=10)
                    url = response.url
                except Exception as e:
                    logger.error(f"Error following TikTok redirect: {e}")
                    return None
            
            # Extract video ID from URL
            patterns = [
                r'/video/(\d+)',
                r'/v/(\d+)',
                r'@[\w.-]+/video/(\d+)',
                r'itemId=(\d+)',
                r'/video/(\d+)\?',
                r'video/(\d+)',
                r'/(\d+)\?',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    video_id = match.group(1)
                    # Validate that it's a numeric ID
                    if video_id.isdigit():
                        return video_id
            
            return None
        except Exception as e:
            logger.error(f"Error extracting TikTok video ID: {e}")
            return None
    
    def download_video(self, video_url: str, filename: str) -> Optional[str]:
        """Download video from URL to local file"""
        try:
            # Clean the URL - fix escaped characters
            video_url = video_url.replace('\\/', '/').replace('\\u0026', '&').replace('\\u00253D', '=')
            
            response = self.session.get(video_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Check content type to ensure it's a video
            content_type = response.headers.get('content-type', '').lower()
            if not any(video_type in content_type for video_type in ['video/', 'mp4', 'mov', 'avi', 'mkv']):
                # If content type doesn't indicate video, check the first few bytes
                first_chunk = next(response.iter_content(chunk_size=1024), b'')
                if not first_chunk.startswith(b'\x00\x00\x00') and not first_chunk.startswith(b'ftyp'):
                    logger.warning(f"Downloaded file doesn't appear to be a video: {content_type}")
                    return None
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Video downloaded successfully: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None
    
    def get_video_url(self, url: str) -> Optional[str]:
        """Get video URL from Instagram or TikTok link"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            if 'instagram.com' in domain:
                return self.extract_instagram_video(url)
            elif 'tiktok.com' in domain:
                return self.extract_tiktok_video(url)
            else:
                logger.warning(f"Unsupported domain: {domain}")
                return None
        except Exception as e:
            logger.error(f"Error getting video URL: {e}")
            return None
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is a valid Instagram or TikTok video URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Instagram patterns
            if 'instagram.com' in domain:
                return '/p/' in url or '/reel/' in url
            
            # TikTok patterns
            if 'tiktok.com' in domain or 'vt.tiktok.com' in domain:
                # Check for various TikTok URL patterns
                tiktok_patterns = [
                    '/@' in url and '/video/' in url,
                    '/video/' in url,
                    '/v/' in url,
                    'vt.tiktok.com' in url
                ]
                return any(tiktok_patterns)
            
            return False
        except Exception as e:
            logger.error(f"Error validating URL: {e}")
            return False

# Example usage
if __name__ == "__main__":
    downloader = VideoDownloader()
    
    # Test URLs
    test_urls = [
        "https://www.instagram.com/p/ABC123/",
        "https://www.tiktok.com/@user/video/1234567890"
    ]
    
    for url in test_urls:
        if downloader.is_valid_url(url):
            video_url = downloader.get_video_url(url)
            if video_url:
                print(f"Found video URL: {video_url}")
            else:
                print(f"Could not extract video URL from: {url}")
        else:
            print(f"Invalid URL: {url}") 