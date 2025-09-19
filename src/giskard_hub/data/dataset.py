from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ._entity import EntityWithTaskProgress
from .chat_test_case import ChatTestCase
from .task import TaskProgress


@dataclass
class Dataset(EntityWithTaskProgress):
    """Dataset object, containing the metadata about the dataset."""

    name: str
    description: str = field(default="")
    project_id: Optional[str] = field(default=None)
    tags: List[str] = field(default_factory=list)

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

    @classmethod
    def from_dict(cls, data: dict, **kwargs) -> "Dataset":
        """Create a Dataset instance from a dictionary."""
        data = dict(data)
        if "status" in data and data["status"]:
            # Map status to progress for EntityWithTaskProgress compatibility
            data["progress"] = TaskProgress.from_dict(data["status"])
        return super().from_dict(data, **kwargs)

    @property
    def resource(self) -> str:
        return "datasets"
