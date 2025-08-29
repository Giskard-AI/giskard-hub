from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from time import sleep
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar

from dateutil import parser

from ._base import BaseData
from .task import TaskProgress, TaskStatus

T = TypeVar("T", bound="EntityWithTaskProgress")

if TYPE_CHECKING:
    from ..client import HubClient


def maybe_entity_to_id(entity, entity_class=None):
    if entity is None:
        return None

    return entity_to_id(entity, entity_class)


def entity_to_id(entity, entity_class=None):
    if isinstance(entity, str):
        return entity

    if entity_class is None:
        return entity.id

    if isinstance(entity, entity_class):
        return entity.id

    raise ValueError(
        f"Invalid {entity_class.__name__} provided, got object of type {type(entity)}"
    )


@dataclass
class Entity(BaseData):
    """Base class containing audit fields and id."""

    id: str | None = field(init=False, default=None)
    created_at: datetime | None = field(init=False, default=None)
    updated_at: datetime | None = field(init=False, default=None)

    _client: Optional["HubClient"] = field(init=False, repr=False, default=None)

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], *, _client: Optional["HubClient"] = None
    ) -> "Entity":
        """Class method factory, allowing to filter from a dict.

        Parameters
        ----------
        data : Dict[str, Any]
            The data to use to initialize the dataclass.
        """
        data = dict(data)

        raw_created_at = data.get("created_at", None)
        raw_updated_at = data.get("updated_at", None)

        if raw_created_at:
            data["created_at"] = parser.parse(raw_created_at)

        if raw_updated_at:
            data["updated_at"] = parser.parse(raw_updated_at)

        entity = super().from_dict(data)
        setattr(entity, "_client", _client)
        return entity  # type: ignore

    def _hydrate(self, data: "Entity"):
        """Hydrate with the data from the API."""
        # @TODO: make this more robust
        for key, value in data.__dict__.items():
            setattr(self, key, value)


@dataclass
class EntityWithTaskProgress(Entity, ABC):
    progress: TaskProgress | None = field(init=False, default=None)

    @property
    @abstractmethod
    def resource(self) -> str:
        """Abstract property for the resource name used in API calls."""

    def is_running(self) -> bool:
        """Check if the evaluation is running."""
        status = getattr(self.progress, "status", None)
        return isinstance(status, TaskStatus) and status == TaskStatus.RUNNING

    def is_finished(self) -> bool:
        """Check if the evaluation is finished."""
        status = getattr(self.progress, "status", None)
        return isinstance(status, TaskStatus) and status == TaskStatus.FINISHED

    def is_errored(self) -> bool:
        """Check if the evaluation terminated with an error."""
        status = getattr(self.progress, "status", None)
        return isinstance(status, TaskStatus) and status == TaskStatus.ERROR

    def wait_for_completion(
        self: T, timeout: float = 600, poll_interval: float = 5
    ) -> T:
        """Wait for the evaluation to complete successfully.

        Parameters
        ----------
        timeout : int, optional
            The timeout in seconds, by default 600
        poll_interval : int, optional
            The polling interval in seconds, by default 5.

        Returns
        -------
        EntityWithTaskProgress
            The updated entity instance after completion.
        """
        end_time = time.perf_counter() + timeout
        if self.is_running():
            self.refresh()
        while time.perf_counter() < end_time:
            if not self.is_running():
                break
            sleep(poll_interval)
            self.refresh()

        if self.is_finished():
            return self

        if self.is_errored():
            raise RuntimeError(
                f"{self.resource.capitalize()} with id '{self.id}' failed"
            )

        if self.is_running():
            raise TimeoutError(
                f"{self.resource.capitalize()} with id '{self.id}' did not finish in time."
            )

        raise RuntimeError(
            f"{self.resource.capitalize()} with id '{self.id}' was aborted."
        )

    def refresh(self: T) -> T:
        """Refresh the entity data from the API."""
        if not self._client or not self.id:
            raise ValueError(
                f"This {self.resource} instance with id '{self.id}' is detached or unsaved and cannot be refreshed."
            )

        # Use the abstract resource property for the API call
        resource = self.resource
        data = getattr(self._client, resource).retrieve(self.id)
        self._hydrate(data)

        return self


@dataclass
class Model(Entity):
    """Model entity.

    Specifies the configuration of a model that can be used on the Hub.
    """

    project_id: str
    name: str
    url: str
    description: str
    supported_languages: List[str]
    headers: List[Dict[str, str]]
