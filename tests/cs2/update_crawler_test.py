from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from fixture import RESPONSE_TEXT

from src.cs2.update_crawler import CounterStrike2UpdateCrawler
from src.cs2.update_crawler import CounterStrike2Updates


class TestCounterStrike2UpdateCrawler(unittest.TestCase):

    def create_mocked_response(self) -> MagicMock:
        response = MagicMock()
        response.ok = True
        response.text = RESPONSE_TEXT
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
