from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class CSGOUpdateCrawler:

    def __init__(self) -> None:
        self.__url_old_updates = "https://store.steampowered.com/news/posts/" \
            "?feed=steam_updates" \
            "&appids=730" \
            "&enddate=1420066800"

        self.__url_new_updates = "https://blog.counter-strike.net/index.php/category/updates/page/1/"

        self.__updates_old = []
        self.__updates_new = []

    def crawl_old_update_news(self) -> None:
        logging.info("Start")
        url = self.__url_old_updates

        if len(self.__updates_old) > 0:
            self.__updates_old.clear()

        while True:
            logging.info(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='html.parser')

            more = soup.find("a", {"id": "more_posts_url"})
            if more is None:
                logging.info("Break no more items.")
                break

            posts = soup.find_all("div", {"id": re.compile(r"post_[0-9]*")})
            for post in posts:
                post_id = post['id'].replace("post_", "")

                post_date = post.find("div", {"class": "date"}).text
                post_date = post_date.strip()

                post_title = post.find("div", {"class": "posttitle"})
                post_link = post_title.find("a")['href']

                post_content = post.find("div", {"class": "body"}).text

                self.__updates_old.append({
                    "id": post_id,
                    "timestamp": post_date,
                    "link": post_link,
                    "entry": post_content})

            try:
                url = more['href']
            except Exception:
                logging.info("Break Exception.")
                break

        self.__updates_old.reverse()
        logging.info("Done.")

    def crawl_new_update_news(self) -> None:
        logging.info("Start")
        url = self.__url_new_updates

        if len(self.__updates_new) > 0:
            self.__updates_new.clear()

        while True:
            logging.info(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='html.parser')

            posts = soup.find_all("div", {"class": "inner_post"})

            for post in posts:
                post_date = post.find("p", {"class": "post_date"}).text
                post_date = post_date[:10]

                date = datetime.strptime(post_date, "%Y.%m.%d")
                post_date_str = date.strftime("%d %b, %Y")

                post_title = post.find("h2")
                post_link = post_title.find("a")['href']

                post_id = hashlib.sha256(post_date_str.encode())

                self.__updates_new.append({
                    "id": post_id.hexdigest(),
                    "timestamp": post_date_str,
                    "link": post_link,
                    "entry": post.text})

            more = soup.find("span", {"id": "older_posts"}).find_all("a")
            more = more[1] if len(more) > 1 else more[0]

            try:
                if "Older posts" in more.text:
                    url = more['href']
                else:
                    logging.info("Break. No more updates available.")
                    break
            except Exception as e:
                logging.error(f"Break. Exception: {e}")
                break

        self.__updates_new.reverse()
        logging.info("Done.")

    def crawl_all(self) -> None:
        self.crawl_old_update_news()
        self.crawl_new_update_news()

    def crawl_latest(self) -> dict:
        logging.info("Start")

        response = requests.get(self.__url_new_updates)
        soup = BeautifulSoup(response.text, features='html.parser')

        latest_post = soup.find("div", {"class": "inner_post"})

        post_date = latest_post.find("p", {"class": "post_date"}).text
        post_date = post_date[:10]
        post_date_str = datetime.strptime(
            post_date, "%Y.%m.%d").strftime("%d %b, %Y")
        post_title = latest_post.find("h2")
        post_link = post_title.find("a")['href']
        post_id = hashlib.sha256(post_date_str.encode())

        res = {
            "id": post_id.hexdigest(),
            "timestamp": post_date_str,
            "link": post_link,
            "entry": latest_post.text}

        logging.info(f"{post_id.hexdigest()=}")
        logging.info(f"{post_date_str=}")
        logging.info(f"{post_link=}")
        logging.info(f"{latest_post.text=}")

        logging.info("Done.")

        return res

    def save(self, filename: str = "updates_combined_raw.json") -> None:
        targetdir = Path(__file__).parent.parent.parent / \
            'data' / 'csgo' / filename
        targetdir = targetdir.with_suffix('.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([
                *self.__updates_old,
                *self.__updates_new
            ], f, indent=4)


def main() -> int:
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=logging.INFO)

    c = CSGOUpdateCrawler()
    c.crawl_all()
    c.save()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
