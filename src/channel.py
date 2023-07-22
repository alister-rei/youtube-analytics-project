import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше
         все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__youtube = self.get_service()

        channel = self.__youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()['items'][0]

        self.__title = channel['snippet']['title']
        self.__channel_description = channel['snippet']['description']
        self.__url = "https://www.youtube.com/" + channel['snippet']['customUrl']
        self.__quantity_sub = int(channel['statistics']['subscriberCount'])
        self.__video_count = channel['statistics']['videoCount']
        self.__quantity_all_views = channel['statistics']['viewCount']

    def __str__(self):
        """ возвращает строку для пользователя """
        return f"{self.__title} ({self.__url})"

    def __add__(self, other):
        """ возвращает сумму количества подписчиков """
        return self.__quantity_sub + other.__quantity_sub

    def __sub__(self, other):
        """ метод для операции вычитания количества подписчиков """
        return self.__quantity_sub - other.__quantity_sub

    def __lt__(self, other):
        """ Метод для операции сравнения «меньше» количества подписчиков """
        return self.__quantity_sub < other.__quantity_sub

    def __le__(self, other):
        """ Метод для операции сравнения «меньше или равно» количества подписчиков """
        return self.__quantity_sub <= other.__quantity_sub

    def __gt__(self, other):
        """ Метод для операции сравнения «больше» количества подписчиков """
        return self.__quantity_sub > other.__quantity_sub

    def __ge__(self, other):
        """  Метод для операции сравнения «больше или равно» количества подписчиков """
        return self.__quantity_sub >= other.__quantity_sub

    @property
    def channel_id(self) -> str:
        """ Геттер метод для получения channel_id """
        return self.__channel_id

    @property
    def title(self) -> str:
        """ Геттер метод для получения title """
        return self.__title

    @property
    def channel_description(self) -> str:
        """ Геттер метод для получения channel_description """
        return self.__channel_description

    @property
    def url(self) -> str:
        """ Геттер метод для получения url """
        return self.__url

    @property
    def quantity_sub(self) -> int:
        """ Геттер метод для получения quantity_sub """
        return self.__quantity_sub

    @property
    def video_count(self) -> int:
        """ Геттер метод для получения video_count """
        return self.__video_count

    @property
    def quantity_all_views(self) -> int:
        """ Геттер метод для получения quantity_all_views """
        return self.__quantity_all_views

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """  возвращает объект для работы с YouTube API """
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name) -> None:
        """ сохраняет в файл значения атрибутов экземпляра `Channel` """
        with open(file_name, 'wt', encoding='utf-8') as file:
            data = {'channel_id': self.__channel_id,
                    'title': self.__title,
                    'channel_description': self.__channel_description,
                    'url': self.__url,
                    'quantity_sub': self.__quantity_sub,
                    'video_count': self.__video_count,
                    'quantity_all_views': self.__quantity_all_views
                    }
            file.write(json.dumps(data, ensure_ascii=False, indent=2))
