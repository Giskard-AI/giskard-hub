from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import List, Optional

from ._entity import Entity
from .chat_test_case import ChatTestCase
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
        warnings.warn(
            "Conversation is deprecated and will be removed. Please use ChatTestCase operations instead.",
            category=DeprecationWarning,
        )
        if self._client and self.id:
            return self._client.conversations.list(dataset_id=self.id)
        return None

    def create_conversation(self, conversation: Conversation):
        """Add a conversation to the dataset."""
        warnings.warn(
            "Conversation is deprecated and will be removed. Please use ChatTestCase operations instead.",
            category=DeprecationWarning,
        )
        if not self._client or not self.id:
            raise ValueError(
                "This dataset instance is detached or unsaved, cannot add conversation."
            )

        return self._client.conversations.create(
            dataset_id=self.id, **conversation.to_dict()
        )

    @property
    def chat_test_cases(self):
        """Return the chat test cases of the dataset."""
        if self._client and self.id:
            return self._client.chat_test_cases.list(dataset_id=self.id)
        return None

    def create_chat_test_case(self, chat_test_case: ChatTestCase):
        """Add a chat test case to the dataset."""
        if not self._client or not self.id:
            raise ValueError(
                "This dataset instance is detached or unsaved, cannot add chat test case."
            )

        return self._client.chat_test_cases.create(
            dataset_id=self.id, **chat_test_case.to_dict()
        )
