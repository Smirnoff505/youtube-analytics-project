import json
import os

import requests
from googleapiclient.discovery import build
from requests import Response


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        reduction = self.get_service().channels().list(part="snippet,statistics", id=self.__channel_id).execute()
        self.title = reduction['items'][0]['snippet']['title']
        self.channel_description = reduction['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = reduction['items'][0]['statistics']['subscriberCount']
        self.video_count = reduction['items'][0]['statistics']['videoCount']
        self.view_count = reduction['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> Response:
        """Выводит в консоль информацию о канале."""
        response = self.get_service().channels().list(
            part="snippet,statistics",
            id=self.__channel_id
        ).execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, name_file):
        channel_list = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.channel_description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(name_file, 'w') as file:
            json.dump(channel_list, file, indent=2, ensure_ascii=False)
