from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any


class Entry:
    gid: str
    clanid: str
    posterid: str
    headline: str
    posttime: int
    updatetime: int
    body: str
    commentcount: int
    tags: list[str]
    language: int
    hidden: int
    forum_topic_id: str
    event_gid: str
    voteupcount: int
    votedowncount: int
    ban_check_result: int
    banned: int

    @property
    def posttime_as_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.posttime)

    def to_dict(self) -> dict:
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]
