import googleapiclient
from googleapiclient.discovery import build
import os


class Video:
    ''' Класс для ютуб-видео '''

    def __init__(self, video_id: str) -> None:
        ''' Экземпляр инициализируется id видео. Дальше
         все данные будут подтягиваться по API. '''
        self.__video_id = video_id
        self.__title = None
        self.__url = None
        self.__view_count = None
        self.__like_count = None
        self.__comment_count = None
        self.__youtube = self.get_service()

        try:
            video_response = self.__youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=self.__video_id).execute()

            self.__title = video_response['items'][0]['snippet']['title']
            self.__url = "https://www.youtube.com/watch?v=" + self.__video_id
            self.__view_count = video_response['items'][0]['statistics']['viewCount']
            self.__like_count = video_response['items'][0]['statistics']['likeCount']
            self.__comment_count = video_response['items'][0]['statistics']['commentCount']

        except IndexError:
            pass

    def __str__(self) -> str:
        ''' возвращает строку для пользователя '''
        return f"{self.__title}"

    @property
    def video_id(self) -> str:
        ''' Геттер метод для получения video_id '''
        return self.__video_id

    @property
    def title(self) -> str:
        ''' Геттер метод для получения title '''
        return self.__title

    @property
    def url(self) -> str:
        ''' Геттер метод для получения url '''
        return self.__url

    @property
    def view_count(self) -> int:
        ''' Геттер метод для получения quantity_sub '''
        return self.__view_count

    @property
    def like_count(self) -> int:
        ''' Геттер метод для получения video_count '''
        return self.__like_count

    @property
    def comment_count(self) -> int:
        ''' Геттер метод для получения video_count '''
        return self.__comment_count

    @classmethod
    def get_service(cls) -> googleapiclient.discovery.Resource:
        '''  возвращает объект для работы с YouTube API '''
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):
    ''' Класс для ютуб-видео в плейлисте '''

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """ Инициализация по id видео """
        super().__init__(video_id)
        self.__playlist_id = playlist_id
