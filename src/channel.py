import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше
         все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        # YT_API_KEY из переменной окружения
        self.__api_key: str = os.getenv('YT_API_KEY')

        # специальный объект для работы с API
        self.__youtube = build('youtube', 'v3', developerKey=self.__api_key)

        channel = self.__youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()['items'][0]

        self.__title = channel['snippet']['title']
        self.__channel_description = channel['snippet']['description']
        self.__url = "https://www.youtube.com/" + channel['snippet']['customUrl']
        self.__quantity_sub = channel['statistics']['subscriberCount']
        self.__video_count = channel['statistics']['videoCount']
        self.__quantity_all_views = channel['statistics']['viewCount']

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def channel_description(self) -> str:
        return self.__channel_description

    @property
    def url(self) -> str:
        return self.__url

    @property
    def quantity_sub(self) -> int:
        return self.__quantity_sub

    @property
    def video_count(self) -> int:
        return self.__video_count

    @property
    def quantity_all_views(self) -> int:
        return self.__quantity_all_views

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.__youtube.channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        '''  возвращает объект для работы с YouTube API '''
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name) -> None:
        ''' сохраняет в файл значения атрибутов экземпляра `Channel` '''
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
