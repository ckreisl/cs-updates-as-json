from datetime import datetime


class Entry:

    def __init__(self, obj: dict) -> None:
        self.__obj = obj

        self.__post_id = obj['id']
        self.__timestamp = obj['timestamp']
        self.__link = obj['link']
        self.__entry = obj['entry']
        self.__tags = obj['tags']
        self.__chars = obj['chars']

    @property
    def data(self) -> dict:
        return self.__obj

    @property
    def post_id(self) -> str:
        return self.__post_id

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def link(self) -> str:
        return self.__link

    @property
    def entry(self) -> str:
        return self.__entry

    @property
    def tags(self) -> str:
        return self.__tags

    @property
    def tags_list(self) -> list:
        return self.tags.split(',')

    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self.timestamp, "%d %b, %Y")
    
    @property
    def chars(self) -> int:
        return self.__chars
