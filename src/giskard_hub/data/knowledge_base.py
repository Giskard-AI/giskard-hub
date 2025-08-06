from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
from uuid import UUID

from ._entity import Entity


@dataclass
class Topic(Entity):
    """A topic within a knowledge base."""

    name: str
    knowledge_base_id: UUID


@dataclass
class Document(Entity):
    """A document within a knowledge base."""

    knowledge_base_id: UUID
    content: str
    topic_id: UUID | None = None
    embedding: List[float] | None = None


@dataclass
class KnowledgeBase(Entity):
    """A knowledge base entity."""

    status: dict
    project_id: UUID
    name: str
    description: str | None = None
    n_documents: int = 0
    filename: str | None = None
    topics: List[Topic] = field(default_factory=list)
