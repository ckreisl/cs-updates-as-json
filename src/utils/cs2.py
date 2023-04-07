from datetime import datetime
from datetime import date

from src.utils.utils import Utils


class CS2DataUtils(Utils):

    @staticmethod
    def updates_per_year(data: dict) -> dict:

        year = datetime.now().year
        res = {}

        for i in range(2023, year + 1):
            res[str(i)] = 0

        for entry in data:
            post_date = datetime.fromtimestamp(entry['posttime'])
            res[f"{post_date.year}"] += 1

        return res
    
    @staticmethod
    def updates_per_month_of_year(data: dict, year: int) -> dict:

        res = {}

        for i in range(1, 13):
            month_name = date(1900, i, 1).strftime('%b')
            res[month_name] = 0

        for entry in data:
            post_date = datetime.fromtimestamp(entry['posttime'])

            if year != post_date.year:
                continue

            month_name = post_date.strftime('%b')
            res[month_name] += 1

        return res