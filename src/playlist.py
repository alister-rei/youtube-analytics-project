import isodate
from googleapiclient.discovery import build
import os
import datetime


class PlayList:
    """ Класс для плейлиста с видео из ютуба """

    def __init__(self, playlist_id: str) -> None:
        """ Инициализатор класса
         playlist_id: id плейлиста
         Получает параметры:
         __title: заголовок плейлиста
         __url: ссылка на плейлист
         """
        self.__playlist_id = playlist_id

        playlist = self.get_service().playlists().list(id=self.__playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50).execute()

        self.__title = playlist['items'][0]['snippet']['title']
        self.__url = "https://www.youtube.com/playlist?list=" + self.__playlist_id

    def __str__(self) -> str:
        """ возвращает строку для пользователя """
        return f"{self.__title} ({self.__url})"

    @classmethod
    def get_service(cls):
        """  возвращает объект для работы с YouTube API """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def playlist_id(self) -> str:
        """ Геттер метод для получения channel_id """
        return self.__playlist_id

    @property
    def title(self) -> str:
        """ Геттер метод для получения title """
        return self.__title

    @property
    def url(self) -> str:
        """ Геттер метод для получения url """
        return self.__url

    @property
    def playlist_videos_list(self) -> list[str]:
        """ Метод возвращает список с videoId видео из плейлиста """
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def video_response(self):
        """ Метод для получения ответа для всех видео в списке по videoId """
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.playlist_videos_list)
                                                          ).execute()
        return video_response

    @property
    def total_duration(self):
        """ Метод возвращающий общую продолжительность видео в плейлисте """
        durations = datetime.timedelta()

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations += duration
        return durations

    def show_best_video(self) -> str:
        """ Метод возвращает самое популярное видео в плейлисте(по кол-ву лайков) """
        most_liked_video = None
        max_likes = 0

        for video in self.video_response['items']:
            video_id = video["id"]
            likes = int(video["statistics"]["likeCount"])

            if likes > max_likes:
                max_likes = likes
                most_liked_video = video_id
        return f"https://youtu.be/{most_liked_video}"
