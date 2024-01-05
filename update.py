from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from src.cs2.update_crawler import CounterStrike2Updates
from src.utils.cs2 import CS2DataUtils
from src.utils.csgo import CSGODataUtils


def create_bar_chart(data: dict, title: str,
                     xlabel: str, ylabel: str,
                     filename: str,
                     offset: float = 0.5,
                     archive: bool = False) -> None:

    x_value = list(data.values())
    y_value = list(data.keys())

    fig, ax = plt.subplots()

    ax.bar(y_value, x_value)

    for i in range(len(y_value)):
        plt.text(i, x_value[i] + offset, x_value[i], ha='center')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    filepath = Path(__file__).parent / 'images'
    if archive:
        filepath = filepath / "archive"

    fig.savefig(filepath / filename, dpi=400)


def update_charts(data: dict, year: int) -> None:

    base_path = Path(__file__).parent / 'data' / 'csgo'
    data_filepath = base_path / "updates_combined_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        csgo_data = json.load(f)

    # Since the update page has changed due to the CS2 announcement
    # we combine the updates form the old update blog page with the latest ones.
    cs_updates_per_year = CSGODataUtils.updates_per_year(csgo_data)

    for _year, updates in CS2DataUtils.updates_per_year(data).items():
        cs_updates_per_year[_year] += updates

    create_bar_chart(cs_updates_per_year,
                     title="Counter-Strike (CS2 & CS:GO) updates over the past years",
                     filename="cs_updates_per_year.png",
                     xlabel="years",
                     ylabel="# updates")

    cs_updates_per_month = {}
    if year < 2024:
        cs_updates_per_month = CSGODataUtils.updates_per_month_of_year(
            data=csgo_data, year=year)

    for month, updates in CS2DataUtils.updates_per_month_of_year(data=data, year=year).items():
        try:
            cs_updates_per_month[month] += updates
        except KeyError:
            cs_updates_per_month[month] = updates

    if year > 2023:
        title = f"Counter Strike 2 (CS2) updates per month in {year}"
    elif 2023 <= year < 2024:
        title = f"Counter-Strike (CS2 & CS:GO) updates per month in {year}"
    else:
        title = f"Counter-Strike: Global Offensive (CS:GO) updates per month in {year}"

    create_bar_chart(cs_updates_per_month,
                     title=title,
                     filename="cs_updates_per_month.png",
                     xlabel="months",
                     ylabel="# updates",
                     offset=0.05)


def archive_monthly_updates_chart(data: dict, year: int) -> None:
    filename = f"cs_updates_per_month_{year}.png"
    filepath = Path(__file__).parent / "images" / "archive" / filename

    if filepath.exists():
        return

    cs_updates_per_month = {}
    if year < 2024:
        base_path = Path(__file__).parent / 'data' / 'csgo'
        data_filepath = base_path / "updates_combined_raw.json"
        with open(data_filepath, encoding='utf-8') as f:
            csgo_data = json.load(f)

        cs_updates_per_month = CSGODataUtils.updates_per_month_of_year(
            data=csgo_data, year=year)

    for month, updates in CS2DataUtils.updates_per_month_of_year(data=data, year=year).items():
        try:
            cs_updates_per_month[month] += updates
        except KeyError:
            cs_updates_per_month[month] = updates

    if year > 2023:
        title = f"Counter Strike 2 (CS2) updates per month in {year}"
    elif 2023 <= year < 2024:
        title = f"Counter-Strike (CS2 & CS:GO) updates per month in {year}"
    else:
        title = f"Counter-Strike: Global Offensive (CS:GO) updates per month in {year}"

    create_bar_chart(data=cs_updates_per_month,
                     title=title,
                     filename=filename,
                     xlabel="months",
                     ylabel="# updates",
                     offset=0.05,
                     archive=True)


def main(args) -> int:

    base_path = Path(__file__).parent / 'data' / 'cs2'
    data_filepath = base_path / "updates_raw.json"
    with open(data_filepath, encoding='utf-8') as f:
        data = json.load(f)

    latest_saved_entry = data[0]

    if args.yearly:
        print(f"Archiving update chart from {args.yearly}")
        archive_monthly_updates_chart(data=data, year=args.yearly)
        return 0

    if not args.daily:
        print("Nothing todo ... provide args '--daily' or '--yearly'")
        return 0

    cs_latest_update = CounterStrike2Updates().crawl().latest
    if latest_saved_entry['posttime'] == cs_latest_update['posttime']:
        print("No new Counter-Strike update post!")
        print(
            f"Date is the same {datetime.fromtimestamp(cs_latest_update['posttime'])}")
        return 0

    print("New Counter-Strike update found ...")
    print(
        f"Update data with new entry: {datetime.fromtimestamp(cs_latest_update['posttime'])}")
    data = [cs_latest_update] + data

    update_charts(data=data, year=datetime.now().year)

    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Just for CI/CD Github Workflow to auto generate charts and check for updates.")
    parser.add_argument("--daily",
                        help="Run daily execution",
                        action='store_true')
    parser.add_argument("--yearly",
                        help="Run archiving of year chart (default: today.year)",
                        type=int,
                        nargs="?",
                        const=datetime.now().year,
                        default=None)
    raise SystemExit(main(parser.parse_args()))
