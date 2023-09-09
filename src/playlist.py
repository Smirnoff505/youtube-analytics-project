import datetime
import os


import isodate
from googleapiclient.discovery import build



class PlayList():
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        reduction = self.get_service().playlists().list(id=self.playlist_id,
                                                        part='snippet',
                                                        ).execute()
        self.title = reduction['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def list_video_id(self):
        # Собираем в список все video_id из playlist
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        total = datetime.timedelta()
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.list_video_id())
                                                          ).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""

        # Определяем переменные в которые будем записывать наибольшее количество лайков и video_id
        best_like_count = 0
        best_video = ''

        # Проверяем количество лайков перебирая видео
        for video_id in self.list_video_id():
            video_response = self.get_service().videos().list(part='statistics',
                                                              id=video_id
                                                              ).execute()
            like_count = video_response['items'][0]['statistics']['likeCount']
            if best_like_count < int(like_count):
                best_like_count = int(like_count)
                best_video = video_id

        return f"https://youtu.be/{best_video}"

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

