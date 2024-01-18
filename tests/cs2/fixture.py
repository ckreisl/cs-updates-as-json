from __future__ import annotations

import json


RESPONSE_TEXT = r'''{
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


def get_dummy_entry_data() -> dict:
    return json.loads(RESPONSE_TEXT)['events'][0]['announcement_body']
