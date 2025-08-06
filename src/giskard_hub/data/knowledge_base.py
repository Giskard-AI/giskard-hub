from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ._entity import Entity

if TYPE_CHECKING:
    from uuid import UUID


@dataclass
class Document(Entity):
    id: str
    content: str
    topic_id: "UUID" | None = None
    embedding: list[float] | None = None


@dataclass
class Topic(Entity):
    id: str
    name: str
    description: str | None = None


@dataclass
class KnowledgeBase(Entity):
    id: str
    name: str
    project_id: str
    description: str | None = None
    n_documents: int = 0
    filename: str | None = None
    topics: list[Topic] = field(default_factory=list)
