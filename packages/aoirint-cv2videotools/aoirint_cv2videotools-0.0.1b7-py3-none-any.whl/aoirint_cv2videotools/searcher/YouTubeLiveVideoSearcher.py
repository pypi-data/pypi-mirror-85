import os
from googleapiclient.discovery import build, Resource # type: ignore

from datetime import datetime
from dateutil.parser import parse

from typing import Tuple, List, Dict
from dataclasses import dataclass, field

from .YouTubeVideoEntry import YouTubeVideoEntry


class YouTubeLiveVideoSearcher:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)


    def search(self, channel_id) -> List[YouTubeVideoEntry]:
        request = self.youtube.search().list(
            part='snippet',
            eventType='live',
            type='video',
            channelId=channel_id,
            maxResults=1,
        )

        response = request.execute()
        items = response.get('items', [])

        videos = []
        for item in items:
            snippet = item.get('snippet', {})
            thumbnails = item.get('thumbnails', {})

            videos.append(YouTubeVideoEntry(
                video_id=item.get('id', {}).get('videoId'),
                title=snippet.get('title'),
                description=snippet.get('description'),
                thumbnail=thumbnails.get('high', thumbnails.get('default')),
                channel_id=snippet.get('channelId'),
                channel_title=snippet.get('channelTitle'),
                publish_time=parse(snippet.get('publishTime')),
            ))

        return videos


    @staticmethod
    def search_live_videos(
        api_key: str,
        channel_id: str
    ) -> List[YouTubeVideoEntry]:

        searcher = YouTubeLiveVideoSearcher(api_key=api_key)
        live_videos = searcher.search(channel_id=channel_id)

        return live_videos
