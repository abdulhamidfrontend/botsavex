import requests
import os

class VideoDownloader:
    def is_valid_url(self, url):
        return "instagram.com" in url

    def get_video_url(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                import re
                match = re.search(r'"video_url":"([^"]+)"', r.text)
                if match:
                    return match.group(1).replace('\\u0026', '&')
        except Exception:
            pass
        return None

    def download_video(self, video_url, filename):
        try:
            r = requests.get(video_url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return filename
        except Exception:
            pass
        return None