from datetime import datetime
from datetime import date

from src.utils.utils import Utils
from src.csgo.update_entry import Entry


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
    def updates_per_month_of_year(data: dict, year: int) -> dict:

        res = {}

        for i in range(1, 13):
            month_name = date(1900, i, 1).strftime('%b')
            res[month_name] = 0

        for entry in data:
            e = Entry(entry)

            if year != e.datetime.year:
                continue

            month_name = e.datetime.date().strftime('%b')
            res[month_name] += 1

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