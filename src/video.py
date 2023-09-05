import os
import json

import requests
from googleapiclient.discovery import build
from requests import Response


class Video(object):
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        reduction = self.get_service().videos().list(id=video_id, part='snippet,statistics').execute()
        self.title = reduction['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = reduction['items'][0]['statistics']['viewCount']
        self.like_count = reduction['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'

    def print_info(self) -> Response:
        """Выводит в консоль информацию о видео."""
        response = self.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id
