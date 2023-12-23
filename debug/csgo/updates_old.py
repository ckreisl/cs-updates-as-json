from __future__ import annotations

import json
import re

import requests
from bs4 import BeautifulSoup


OLD_NEWS_URL = "https://store.steampowered.com/news/posts/" \
    "?feed=steam_updates" \
    "&appids=730" \
    "&enddate=1420066800"


def main() -> int:

    print("Start.")

    url = OLD_NEWS_URL

    posts = []

    while True:
        print(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')

        more = soup.find("a", {"id": "more_posts_url"})

        if more is None:
            print("Break no more items.")
            break

        entries = soup.find_all("div", {"id": re.compile(r"post_[0-9]*")})

        for entry in entries:
            post_id = entry['id'].replace("post_", "")
            date_str = entry.find("div", {"class": "date"}).text
            date_str = date_str.strip()

            post_title = entry.find("div", {"class": "posttitle"})
            post_link = post_title.find("a")['href']

            post_entry = entry.find("div", {"class": "body"})
            post_entry_text = post_entry.text

            posts.append({"id": post_id,
                          "timestamp": date_str,
                          "link": post_link,
                          "entry": post_entry_text})

        try:
            url = more['href']
        except Exception:
            print("Break Exception.")
            break

    with open("updates_old.json", "w", encoding='utf-8') as f:
        json.dump(posts, f)

    print("Done.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
