from __future__ import annotations

import json
import logging
from pathlib import Path

import requests


class CounterStrike2Updates:

    RELEASE_NOTES_EVENT: int = 12

    def __init__(self) -> None:

        # Time when cs2 test phase was officially announced
        self.__initial_epoch_time = 1679503828

        self.__url = "https://store.steampowered.com/" \
            "events/ajaxgetpartnereventspageable/" \
            "?clan_accountid=0" \
            "&appid=730" \
            "&offset=0" \
            "&count=100" \
            "&l=english" \
            "&origin=https://www.counter-strike.net"

        self.__data = []

    @property
    def url(self) -> str:
        return self.__url

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def latest(self) -> dict:
        return self.__data[0]

    def crawl(self, only_cs2: bool = True) -> CounterStrike2Updates:
        logging.info("Start")

        response = requests.get(self.url)

        if not response.ok:
            raise Exception(
                f'Could not fetch data received response code={response.status_code}')

        data = json.loads(response.text)

        for event in data['events']:
            if event['event_type'] != self.RELEASE_NOTES_EVENT:
                continue

            self.__data.append(event['announcement_body'])

        if only_cs2:
            self.__data = list(
                filter(lambda x: x['posttime'] >= self.__initial_epoch_time,
                       self.__data))

        logging.info("Done.")
        return self

    def save(self, filename: str = 'updates_raw.json') -> None:
        target_dir = Path(__file__).parent.parent.parent / \
            'data' / 'cs2' / filename
        target_dir = target_dir.with_suffix('.json')

        with open(target_dir, 'w', encoding='utf-8') as fp:
            json.dump(self.data, fp, indent=4)


def main() -> int:
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=logging.INFO)
    CounterStrike2Updates().crawl().save()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
