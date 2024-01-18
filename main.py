from __future__ import annotations

import json
from pathlib import Path

from src.cs2.update_crawler import CounterStrike2Updates
from src.utils.cs2 import CS2DataUtils
from src.utils.csgo import CSGODataUtils


def main() -> int:
    filepath = Path(__file__).parent / "data" / "csgo" / \
        "updates_combined_custom.json"

    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    """
        Some dummy examples on how to use the utils.
    """

    # Deprecated CS:GO
    print("CSGO updates per year:")
    print(CSGODataUtils.updates_per_year(data))

    print("CSGO updates per month of year:")
    print(CSGODataUtils.updates_per_month_of_year(data, 2020))

    # CS2 update examples
    print("CS2 Updates per year:")
    cs2_updates = CounterStrike2Updates.load_from_json()
    print(CS2DataUtils.updates_per_year(cs2_updates.updates_raw))

    print("CS2 Updates per month of year 2023:")
    print(CS2DataUtils.updates_per_month_of_year(cs2_updates.updates_raw, 2023))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
