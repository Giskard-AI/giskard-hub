from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ._entity import Entity
from .conversation import Conversation


@dataclass
class Dataset(Entity):
    """Dataset object, containing the metadata about the dataset."""

    name: str
    description: str = field(default="")
    project_id: Optional[str] = field(default=None)
    tags: List[str] = field(default_factory=list)

    @property
    def conversations(self):
        """Return the conversations of the dataset."""
        if self._client and self.id:
            return self._client.conversations.list(dataset_id=self.id)
        return None

    def create_conversation(self, conversation: Conversation):
        """Add a conversation to the dataset."""
        if not self._client or not self.id:
            raise ValueError(
                "This dataset instance is detached or unsaved, cannot add conversation."
            )

        return self._client.conversations.create(
            dataset_id=self.id, **conversation.to_dict()
        )
