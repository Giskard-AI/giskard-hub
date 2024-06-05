from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ._base import BaseData


class TaskStatus(str, Enum):
    SKIPPED = "skipped"
    FINISHED = "finished"
    ERROR = "error"
    RUNNING = "running"


@dataclass
class TaskProgress(BaseData):
    status: TaskStatus
    current: int
    total: int
    error: str | None = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            status=TaskStatus(data["state"]),
            current=data["current"],
            total=data["total"],
            error=data.get("error"),
        )
