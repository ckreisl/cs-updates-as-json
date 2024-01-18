from __future__ import annotations

import unittest
from datetime import datetime

from fixture import get_dummy_entry_data

from src.cs2.update_entry import Entry


class TestUpdateEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.entry_data = get_dummy_entry_data()

    def test_create_entry_object(self):
        entry = Entry(**self.entry_data)

        self.assertEqual(entry.gid, self.entry_data['gid'])
        self.assertEqual(entry.clanid, self.entry_data['clanid'])
        self.assertEqual(entry.posterid, self.entry_data['posterid'])
        self.assertEqual(entry.headline, self.entry_data['headline'])
        self.assertEqual(entry.posttime, self.entry_data['posttime'])
        self.assertEqual(entry.updatetime, self.entry_data['updatetime'])
        self.assertEqual(entry.body, self.entry_data['body'])
        self.assertEqual(entry.commentcount, self.entry_data['commentcount'])
        self.assertEqual(entry.tags, self.entry_data['tags'])
        self.assertEqual(entry.language, self.entry_data['language'])
        self.assertEqual(entry.hidden, self.entry_data['hidden'])
        self.assertEqual(entry.forum_topic_id,
                         self.entry_data['forum_topic_id'])
        self.assertEqual(entry.event_gid, self.entry_data['event_gid'])
        self.assertEqual(entry.voteupcount, self.entry_data['voteupcount'])
        self.assertEqual(entry.votedowncount, self.entry_data['votedowncount'])
        self.assertEqual(entry.ban_check_result,
                         self.entry_data['ban_check_result'])
        self.assertEqual(entry.banned, self.entry_data['banned'])

    def test_get_item(self):
        entry = Entry(**self.entry_data)

        self.assertEqual(entry['gid'], self.entry_data['gid'])
        self.assertEqual(entry['clanid'], self.entry_data['clanid'])
        self.assertEqual(entry['posterid'], self.entry_data['posterid'])
        self.assertEqual(entry['headline'], self.entry_data['headline'])
        self.assertEqual(entry['posttime'], self.entry_data['posttime'])
        self.assertEqual(entry['updatetime'], self.entry_data['updatetime'])
        self.assertEqual(entry['body'], self.entry_data['body'])
        self.assertEqual(entry['commentcount'],
                         self.entry_data['commentcount'])
        self.assertEqual(entry['tags'], self.entry_data['tags'])
        self.assertEqual(entry['language'], self.entry_data['language'])
        self.assertEqual(entry['hidden'], self.entry_data['hidden'])
        self.assertEqual(entry['forum_topic_id'],
                         self.entry_data['forum_topic_id'])
        self.assertEqual(entry['event_gid'], self.entry_data['event_gid'])
        self.assertEqual(entry['voteupcount'], self.entry_data['voteupcount'])
        self.assertEqual(entry['votedowncount'],
                         self.entry_data['votedowncount'])
        self.assertEqual(entry['ban_check_result'],
                         self.entry_data['ban_check_result'])
        self.assertEqual(entry['banned'], self.entry_data['banned'])

    def test_to_dict(self):
        entry = Entry(**self.entry_data)
        self.assertEqual(entry.to_dict(), self.entry_data)

    def test_posttime_as_datetime(self):
        entry = Entry(**self.entry_data)
        self.assertTrue(isinstance(entry.posttime_as_datetime, datetime))
        self.assertEqual(entry.posttime_as_datetime,
                         datetime.fromtimestamp(entry.posttime))
