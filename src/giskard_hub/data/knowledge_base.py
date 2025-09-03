from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ._entity import Entity, EntityWithTaskProgress
from .task import TaskProgress

if TYPE_CHECKING:
    from uuid import UUID


@dataclass
class Document(Entity):
    content: str
    topic_id: "UUID" | None = None
    embedding: list[float] = field(default_factory=list)


@dataclass
class Topic(Entity):
    name: str
    description: str | None = None


@dataclass
class KnowledgeBase(EntityWithTaskProgress):
    name: str
    project_id: str
    description: str | None = None
    n_documents: int = 0
    filename: str | None = None
    topics: list[Topic] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, **kwargs) -> "KnowledgeBase":
        """Create a KnowledgeBase instance from a dictionary."""
        data = dict(data)
        if "status" in data and data["status"]:
            # Map status to progress for EntityWithTaskProgress compatibility
            data["progress"] = TaskProgress.from_dict(data["status"])
        return super().from_dict(data, **kwargs)

    @property
    def resource(self) -> str:
        return "knowledge_bases"
