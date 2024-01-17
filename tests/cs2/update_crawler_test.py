from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from src.cs2.update_crawler import CounterStrike2UpdateCrawler
from src.cs2.update_crawler import CounterStrike2Updates


def response_text() -> str:
    return r'''{
        "events": [
            {
                "event_type": 12,
                "announcement_body": {
                    "gid": "3860212413466910114",
                    "clanid": "3381077",
                    "posterid": "76561199571358539",
                    "headline": "Release Notes for 1/4/2024",
                    "posttime": 1704407496,
                    "updatetime": 1704407760,
                    "body": "[ UI ]\n[list]\n[*]Fixed cases where there was a visible delay loading map images in the Play menu\n[*]Fixed a bug where items that can't be equipped were visible in the Loadout menu\n[*]Fixed a bug where loadout items couldn't be unequipped\n[*]Fixed a bug where loadout changes weren't saved if the game was quit shortly after making changes\n[*]Fixed a bug where loadout changes on the main menu character were delayed\n[/list]\n[ MISC ]\n[list]\n[*]Fixed some visual issues with demo playback\n[*]Fixed an issue where animations would not play back correctly in a CSTV broadcast\n[*]Adjusted wear values of some community stickers to better match CS:GO\n[/list]\n[ MAPS ]\n[i]Ancient:[/i][list]\n[*]Added simplified grenade collisions to corner trims and central pillar on B site\n[/list]\n[i]Anubis:[/i][list]\n[*]Adjusted clipping at A site steps between Walkway and Heaven\n[/list]",
                    "commentcount": 540,
                    "tags": [
                        "patchnotes",
                        "mod_reviewed",
                        "ModAct_1415588329_1704407907_0"
                    ],
                    "language": 0,
                    "hidden": 0,
                    "forum_topic_id": "4031350479982590077",
                    "event_gid": "3860212413466910113",
                    "voteupcount": 2361,
                    "votedowncount": 719,
                    "ban_check_result": 0,
                    "banned": 0
                }
            },
            {
                "event_type": 12,
                "announcement_body": {
                    "gid": "3860212413416497619",
                    "clanid": "3381077",
                    "posterid": "76561199569812632",
                    "headline": "Release Notes for 12/21/2023",
                    "posttime": 1703201270,
                    "updatetime": 1703201270,
                    "body": "[ MISC ]\n[list]\n[*]Fixed a case where players could refund a grenade for a brief period after it was thrown\n[/list]",
                    "commentcount": 189,
                    "tags": [
                        "patchnotes",
                        "mod_reviewed",
                        "ModAct_1415588329_1703202413_0"
                    ],
                    "language": 0,
                    "hidden": 0,
                    "forum_topic_id": "4031349199258800158",
                    "event_gid": "3860212413416497618",
                    "voteupcount": 695,
                    "votedowncount": 142,
                    "ban_check_result": 0,
                    "banned": 0
                }
            },
            {
                "event_type": 11,
                "announcement_body": {}
            }
        ]
    }'''


class TestCounterStrike2UpdateCrawler(unittest.TestCase):

    def create_mocked_response(self) -> MagicMock:
        response = MagicMock()
        response.ok = True
        response.text = response_text()
        return response

    def setUp(self) -> None:
        self.crawler = CounterStrike2UpdateCrawler()

    @patch('requests.get')
    def test_crawl_success_with_limit_one(self, mocked_get) -> None:
        mocked_get.return_value = self.create_mocked_response()

        updates = self.crawler.crawl(from_epoch_time=1703201270, limit=1)

        self.assertEqual(len(updates), 1)
        self.assertEqual(updates.latest.posterid, "76561199571358539")
        self.assertEqual(updates.oldest.posterid, "76561199571358539")
        self.assertTrue(isinstance(updates, CounterStrike2Updates))

        mocked_get.assert_called_once_with(self.crawler.url)

    @patch('requests.get')
    def test_crawl_success_without_limit(self, mocked_get) -> None:
        mocked_get.return_value = self.create_mocked_response()

        updates = self.crawler.crawl()

        self.assertEqual(len(updates), 2)
        self.assertEqual(updates.latest.posterid, "76561199571358539")
        self.assertEqual(updates.oldest.posterid, "76561199569812632")
        self.assertTrue(isinstance(updates, CounterStrike2Updates))

        mocked_get.assert_called_once_with(self.crawler.url)

    @patch('requests.get')
    def test_crawl_with_failed_response(self, mocked_get) -> None:
        mocked_get.return_value = MagicMock(ok=False)

        with self.assertRaises(Exception):
            self.crawler.crawl()

    @patch('requests.get')
    def test_crawl_with_epoch_time(self, mocked_get) -> None:
        mocked_get.return_value = self.create_mocked_response()

        updates = self.crawler.crawl(from_epoch_time=1703201271)

        self.assertEqual(len(updates), 1)
        self.assertEqual(updates.latest.posttime, 1704407496)
        self.assertEqual(updates.oldest.posttime, 1704407496)
