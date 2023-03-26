from datetime import datetime
from csgo_update_data import Entry


class Utils:
    pass


class CS2DataUtils(Utils):

    @staticmethod
    def updates_per_year(data: dict) -> dict:

        year = datetime.now().year
        res = {}

        for i in range(2023, year + 1):
            res[str(i)] = 0

        for entry in data:
            date = datetime.utcfromtimestamp(entry['posttime'])
            res[f"{date.year}"] += 1

    @staticmethod
    def tags_histogram(data: dict) -> dict:
        # TODO
        pass


class CSGODataUtils(Utils):

    @staticmethod
    def updates_per_year(data: dict) -> dict:

        year = datetime.now().year
        res = {}

        for i in range(2012, year + 1):
            res[str(i)] = 0

        for post in data:
            e = Entry(post)
            res[f"{e.datetime.year}"] += 1

        return res
    
    @staticmethod
    def tags_histogram(data: dict) -> dict:
        res = {}

        for post in data:
            e = Entry(post)
            tags = e.tags_list
            for tag in tags:
                if res.get(tag, None) is None:
                    res[tag] = 1
                else:
                    res[tag] += 1

        return res
    
    # TODO more to come
