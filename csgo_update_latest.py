import requests
import hashlib
import json

from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


url = "https://blog.counter-strike.net/index.php/category/updates/"


def crawl_latest_update_entry() -> dict:
    print("Start")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')

    latest_post = soup.find("div", {"class": "inner_post"})

    post_date = latest_post.find("p", {"class": "post_date"}).text
    post_date = post_date[:10]
    post_date_str = datetime.strptime(post_date, "%Y.%m.%d").strftime("%d %b, %Y")
    post_title = latest_post.find("h2")
    post_link = post_title.find("a")['href']
    post_id = hashlib.sha256(post_date_str.encode())

    res = {
        "id": post_id.hexdigest(),
        "timestamp": post_date_str,
        "link": post_link,
        "entry": latest_post.text}

    print(f"{post_id.hexdigest()=}")
    print(f"{post_date_str=}")
    print(f"{post_link=}")
    print(f"{latest_post.text=}")

    print("Done.")

    return res


def main() -> int:
    latest_update_news_entry = crawl_latest_update_entry()

    data_filepath = Path(__file__).parent / 'data' / "updates_combined_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        data = json.load(f)

    latest_entry_in_data = data[-1]

    if latest_entry_in_data['timestamp'] == latest_update_news_entry['timestamp']:
        print(f"No new update post. Date is the same {latest_update_news_entry['timestamp']}")
        return 0

    print("New update found ...")
    print(f"Update data with new entry: {latest_update_news_entry['timestamp']}")
    data.append(latest_update_news_entry)

    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())