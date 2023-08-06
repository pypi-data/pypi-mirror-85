from urllib.parse import urlparse, urlunparse, urlencode
import subprocess
import cv2

from .VideoLoader import VideoLoader

class YouTubeLoader(VideoLoader):
    def __init__(self,
        video_url=None,
        video_id=None,
        video_format='bestvideo/best',
        # video_format='worstvideo/worst',
    ):
        assert video_url or video_id

        if video_id is not None:
            params = {
                'v': video_id,
            }
            qs = urlencode(params, doseq=True)
            urlp = urlparse('https://www.youtube.com/watch')
            video_url = urlunparse(urlp._replace(query=qs))

        ytdl_process = subprocess.Popen([
            'youtube-dl',
            '-f', video_format,
            '-o', '-',
            video_url,
        ], stdout=subprocess.PIPE)

        cap = cv2.VideoCapture(f'pipe:{ytdl_process.stdout.fileno()}')
        self.cap = cap
