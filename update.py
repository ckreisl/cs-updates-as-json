import json

import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

from src.utils.cs2 import CS2DataUtils
from src.utils.csgo import CSGODataUtils

from src.cs2.update_crawler import CounterStrike2Updates
from src.csgo.update_crawler import CSGOUpdateCrawler


def create_bar_chart(data: dict, title: str,
                    xlabel: str, ylabel: str,
                    filename: str,
                    offset: float = 0.5) -> None:

    x_value = list(data.values())
    y_value = list(data.keys())

    fig, ax = plt.subplots()

    ax.bar(y_value, x_value)

    for i in range(len(y_value)):
        plt.text(i, x_value[i] + offset, x_value[i], ha = 'center')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    fig.savefig(Path(__file__).parent / 'images' / filename, dpi=400)


def update_csgo() -> None:
    csgo_latest_update = CSGOUpdateCrawler().crawl_latest()

    base_path = Path(__file__).parent / 'data' / 'csgo'
    data_filepath = base_path / "updates_combined_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        data = json.load(f)

    latest_saved_entry = data[-1]

    if latest_saved_entry['timestamp'] == csgo_latest_update['timestamp']:
        print(f"No new CS:GO update post. Date is the same {csgo_latest_update['timestamp']}")
        return

    print("New CS:GO update entry found ...")
    print(f"Update data with new entry: {datetime.fromtimestamp(csgo_latest_update['timestamp'])}")
    data.append(csgo_latest_update)

    create_bar_chart(CSGODataUtils.updates_per_year(data),
        title="CS:GO updates over the past years",
        filename="csgo_updates_per_year.png",
        xlabel="years",
        ylabel="# updates")
    
    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def update_cs2() -> None:
    cs2_latest_update = CounterStrike2Updates().crawl().latest

    base_path = Path(__file__).parent / 'data' / 'cs2'
    data_filepath = base_path / "updates_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        data = json.load(f)

    latest_saved_entry = data[0]

    if latest_saved_entry['posttime'] == cs2_latest_update['posttime']:
        print(f"No new CS2 update post. Date is the same {cs2_latest_update['posttime']}")
        return

    print("New Counter-Strike 2 update entry found ...")
    print(f"Update data with new entry: {cs2_latest_update['posttime']}")
    data = [cs2_latest_update] + data

    # Future stuff.
    """ 
    create_bar_chart(CS2DataUtils.updates_per_year(data),
        title="Counter-Strike 2 Updates",
        filename="cs2_updates_per_year.png",
        xlabel="years",
        ylabel="# updates",
        offset=0.05)
    """
    
    create_bar_chart(CS2DataUtils.updates_per_month_of_year(data, 2023),
        title="Counter-Strike 2 Updates per month in 2023",
        filename="cs2_updates_per_month.png",
        xlabel="months",
        ylabel="# updates",
        offset=0.05)
    
    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def main() -> int:
    update_csgo()
    update_cs2()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())