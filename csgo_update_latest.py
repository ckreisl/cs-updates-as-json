import requests
import hashlib
import json

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

from csgo_update_data_utils import Utils


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


def update_readme_image(data: dict) -> None:
    updates_per_year = Utils.updates_per_year(data)

    years = updates_per_year.keys()
    updates = updates_per_year.values()

    plt.bar(years, updates)

    offset = 0.5

    for i in range(len(years)):
        plt.text(i, updates[i] + offset, 
                 updates[i], ha = 'center')

    plt.title('CS:GO updates over the past years.')
    plt.xlabel('Year')
    plt.ylabel('# updates')

    plt.savefig(
        Path(__file__).parent / 'images' / 'csgo_updates_per_year.png', 
        dpi=400)


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

    update_readme_image(data)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())