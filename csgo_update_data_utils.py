from csgo_update_data import Entry


class Utils:

    @staticmethod
    def updates_per_year(data: dict) -> dict:
        res = {
            "2012": 0, "2013": 0, "2014": 0, "2015": 0,
            "2016": 0, "2017": 0, "2018": 0, "2019": 0,
            "2020": 0, "2021": 0, "2022": 0, "2023": 0
        }

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
