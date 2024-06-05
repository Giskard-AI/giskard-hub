from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from dateutil import parser

if TYPE_CHECKING:
    from ..client import HubClient

from ._base import BaseData


def maybe_entity_to_id(entity, EntityClass=None):
    if entity is None:
        return None

    return entity_to_id(entity, EntityClass)


def entity_to_id(entity, EntityClass=None):
    if isinstance(entity, str):
        return entity

    if EntityClass is None:
        return entity.id

    if isinstance(entity, EntityClass):
        return entity.id

    raise ValueError(
        f"Invalid {EntityClass.__name__} provided, got object of type {type(entity)}"
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
        entity._client = _client
        return entity

    def _hydrate(self, data: "Entity"):
        """Hydrate with the data from the API."""
        # @TODO: make this more robust
        for key, value in data.__dict__.items():
            setattr(self, key, value)


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
