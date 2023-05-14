import json

from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

from src.utils.cs2 import CS2DataUtils
from src.utils.csgo import CSGODataUtils
from src.cs2.update_crawler import CounterStrike2Updates


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


def update_charts(data: dict) -> None:

    base_path = Path(__file__).parent / 'data' / 'csgo'
    data_filepath = base_path / "updates_combined_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        csgo_data = json.load(f)

    # Since the update page has changed due to the CS2 announcement
    # we combine the updates form the old update blog page with the latest ones.
    cs_updates_per_year = CSGODataUtils.updates_per_year(csgo_data)

    for year, udpates in CS2DataUtils.updates_per_year(data).items():
        cs_updates_per_year[year] += udpates

    create_bar_chart(cs_updates_per_year,
                     title="Counter-Strike (CS2 & CS:GO) updates over the past years",
                     filename="cs_updates_per_year.png",
                     xlabel="years",
                     ylabel="# updates")

    cs_updates_per_month = CSGODataUtils.updates_per_month_of_year(csgo_data, 2023)

    for month, udpates in CS2DataUtils.updates_per_month_of_year(data, 2023).items():
        cs_updates_per_month[month] += udpates

    create_bar_chart(cs_updates_per_month,
                     title="Counter-Strike (CS2 & CS:GO) updates per month in 2023",
                     filename="cs_updates_per_month.png",
                     xlabel="months",
                     ylabel="# updates",
                     offset=0.05)

def main() -> int:
    cs_latest_update = CounterStrike2Updates().crawl().latest

    base_path = Path(__file__).parent / 'data' / 'cs2'
    data_filepath = base_path / "updates_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        data = json.load(f)

    latest_saved_entry = data[0]

    if latest_saved_entry['posttime'] == cs_latest_update['posttime']:
        print("No new Counter-Strike update post!")
        print(f"Date is the same {datetime.fromtimestamp(cs_latest_update['posttime'])}")
        return 0

    print("New Counter-Strike update found ...")
    print(f"Update data with new entry: {datetime.fromtimestamp(cs_latest_update['posttime'])}")
    data = [cs_latest_update] + data

    update_charts(data)

    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())