from dataclasses import dataclass, field
from typing import List, Optional

from giskard_hub.data import Conversation

from ._entity import Entity, maybe_entity_to_id
from .project import Project
from .._default_client import _load_client


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


    def push_to_hub(self, project: Project | str | None = None):
        """Push the dataset to the hub.

        Parameters
        ----------
        project : Project | str | None
            The project to push the dataset to.
        """
        client = self._client or _load_client()

        project = maybe_entity_to_id(project, Project) or self.project_id
        if project is None:
            raise TypeError("You need to provide a project to push the dataset to.")

        if self.id is None:
            data = client.datasets.create(
                name=self.name,
                description=self.description,
                project_id=project,
            )
        else:
            data = client.datasets.update(
                dataset_id=self.id,
                name=self.name,
                description=self.description,
                project_id=project,
            )

        self._hydrate(data)
