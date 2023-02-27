import json

from pathlib import Path
from csgo_update_data_utils import Utils


def main() -> int:
    filepath = Path(__file__).parent / "csgo_update_data.json"

    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    # dummy example
    print(Utils.updates_per_year(data))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())