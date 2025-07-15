import requests
import re

class VideoDownloader:
    def is_valid_url(self, url):
        return "instagram.com" in url and ("/reel/" in url or "/p/" in url)

    def get_video_url(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                match = re.search(r'"video_url":"([^"]+)"', r.text)
                if match:
                    return match.group(1).replace('\\u0026', '&')
                match2 = re.search(r'<meta property="og:video" content="([^"]+)"', r.text)
                if match2:
                    return match2.group(1)
        except Exception as e:
            print("Error extracting video url:", e)
        return None

    def download_video(self, video_url, filename):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            r = requests.get(video_url, stream=True, headers=headers)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return filename
        except Exception as e:
            print("Error downloading video:", e)
        return None