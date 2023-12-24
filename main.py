from __future__ import annotations

import json
from pathlib import Path

from src.utils.csgo import CSGODataUtils


def main() -> int:
    filepath = Path(__file__).parent / "data" / "csgo" / \
        "updates_combined_custom.json"

    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    # dummy example
    print(CSGODataUtils.updates_per_year(data))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
