from __future__ import annotations

import json

import pytest

from src.cs2.update_crawler import CounterStrike2Updates
from src.cs2.update_entry import Entry
from src.utils.cs2 import CS2DataUtils
from tests.cs2.fixture import RESPONSE_TEXT


@pytest.fixture
def data() -> CounterStrike2Updates:
    updates = []
    # TODO: Refactor so that CS2Updates class can handle it and utils can use it
    for event in json.loads(RESPONSE_TEXT.encode())['events']:
        if event['event_type'] != 12:
            continue
        updates.append(Entry(**event['announcement_body']))
    return CounterStrike2Updates(updates).updates_raw


def test_cs2_updates_per_year(data):
    cs2_histogram = CS2DataUtils.updates_per_year(data)
    assert cs2_histogram['2023'] == 1
    assert cs2_histogram['2024'] == 1

    with pytest.raises(KeyError):
        cs2_histogram['2022']


def test_cs2_updates_per_month_of_year(data):
    csgo_data = CS2DataUtils.updates_per_month_of_year(data, 2023)
    assert len(csgo_data) == 12
