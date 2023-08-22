import os

import requests
from googleapiclient.discovery import build
from requests import Response

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> Response:
        """Выводит в консоль информацию о канале."""
        request = youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        response = request.execute()
        print(response)
