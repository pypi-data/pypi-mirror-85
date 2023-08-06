from typing import NamedTuple
from datetime import datetime

class YouTubeVideoEntry(NamedTuple):
    video_id: str
    title: str
    description: str
    thumbnail: str
    channel_id: str
    channel_title: str
    publish_time: datetime
