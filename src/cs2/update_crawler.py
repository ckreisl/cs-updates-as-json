from __future__ import annotations

import json
import logging
from pathlib import Path

import requests

try:
    from src.cs2.update_entry import Entry
except ImportError:
    from .update_entry import Entry


class CounterStrike2UpdateCrawler:

    # Time when cs2 test phase was officially announced
    INITIAL_EPOCH_TIME_CS2 = 1679503828
    RELEASE_NOTES_EVENT: int = 12

    def __init__(self) -> None:
        self.url = "https://store.steampowered.com/" \
            "events/ajaxgetpartnereventspageable/" \
            "?clan_accountid=0" \
            "&appid=730" \
            "&offset=0" \
            "&count=100" \
            "&l=english" \
            "&origin=https://www.counter-strike.net"

    def crawl(self,
              *,
              from_epoch_time: int = INITIAL_EPOCH_TIME_CS2,
              limit: int = -1) -> CounterStrike2Updates:
        logging.info("Start")

        response = requests.get(self.url)

        if not response.ok:
            raise Exception(
                f'Could not fetch data received response code={response.status_code}')

        data = json.loads(response.text)

        entries = []
        for event in data['events']:
            if event['event_type'] != self.RELEASE_NOTES_EVENT:
                continue

            if limit != -1 and len(entries) >= limit:
                break

            entries.append(Entry(**event['announcement_body']))

        entries = list(
            filter(lambda x: x.posttime >= from_epoch_time, entries))

        logging.info("Done.")

        return CounterStrike2Updates(entries)


class CounterStrike2Updates:

    def __init__(self, updates: list[Entry]) -> None:
        self.__updates = updates

    @property
    def updates(self) -> list[Entry]:
        return self.__updates

    @property
    def updates_raw(self) -> list[dict]:
        return list(map(lambda x: x.to_dict(), self.__updates))

    @property
    def latest(self) -> Entry:
        return self.__updates[0]

    @property
    def oldest(self) -> Entry:
        return self.__updates[-1]

    def __len__(self) -> int:
        return len(self.__updates)

    @classmethod
    def load_from_json(cls, filename: str = 'updates_raw.json') -> CounterStrike2Updates:
        with open(filename, encoding='utf-8') as fp:
            data = json.load(fp)

        updates = []
        for entry in data:
            updates.append(Entry(**entry))

        return CounterStrike2Updates(updates)

    def add(self, update: Entry) -> None:
        self.__updates = [update, *self.__updates]

    def save(self, filename: str = 'updates_raw.json') -> None:
        target_dir = Path(__file__).parent.parent.parent / \
            'data' / 'cs2' / filename
        target_dir = target_dir.with_suffix('.json')

        with open(target_dir, 'w', encoding='utf-8') as fp:
            json.dump(self.updates_raw, fp, indent=4)


def main() -> int:
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=logging.INFO)

    updates = CounterStrike2UpdateCrawler().crawl()
    cs2_updates = CounterStrike2Updates(updates)
    cs2_updates.save()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
