import json
import requests
import hashlib

from bs4 import BeautifulSoup
from datetime import datetime


NEW_NEWS_URL = "https://blog.counter-strike.net/index.php/category/updates/page/1/"


def main() -> int:

    print("Start.")

    posts = []
    url = NEW_NEWS_URL

    while True:
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, features='html.parser')

        more = soup.find("span", {"id": "older_posts"})

        if more is None:
            print("Break no more items.")
            break

        entries = soup.find_all("div", {"class": "inner_post"})

        for entry in entries:
            date_str = entry.find("p", {"class": "post_date"}).text
            date_str = date_str[:10]
            #date = datetime.strptime(date_str, "%d %b, %Y")
            #2014.01.23
            date = datetime.strptime(date_str, "%Y.%m.%d")
            date_str = date.strftime("%d %b, %Y")

            post_title = entry.find("h2")
            post_link = post_title.find("a")['href']

            post_id = hashlib.sha256(date_str.encode())

            posts.append({"id": post_id.hexdigest(),
                          "timestamp": date_str,
                          "link": post_link,
                          "entry": entry.text})

        more = more.find_all("a")
        more = more[1] if len(more) > 1 else more[0]

        try:
            if "Older posts" in more.text:
                url = more['href']
            else:
                break
        except Exception:
            print("Break Exception.")
            break

    with open("updates_new.json", "w", encoding='utf-8') as f:
        json.dump(posts, f)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())