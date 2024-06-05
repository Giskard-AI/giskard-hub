from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Dict, Literal


class NotGiven:
    """Sentinel object to represent a value that was not given."""

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()


def filter_not_given(data: Dict[str, any]) -> Dict[str, any]:
    return {k: v for k, v in data.items() if v is not NOT_GIVEN}


@dataclass
class BaseData:
    """Base dataclass containing utility function."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseData":
        """Class method factory.

        Parameters
        ----------
        data : Dict[str, Any]
            The data to use to initialize the dataclass.

        Returns
        -------
        BaseDataclass
            The dataclass instance.
        """
        init_set = [f.name for f in fields(cls) if f.init]
        instance = cls(**{k: data.get(k) for k in init_set})

        post_set = [f.name for f in fields(cls) if not f.init]
        for key in post_set:
            value = data.get(key, NOT_GIVEN)
            if value is not NOT_GIVEN:
                setattr(instance, key, value)

        return instance

    def to_dict(self) -> Dict[str, Any]:
        """Return the dataclass as a dictionary.

        Returns
        -------
        Dict[str, Any]
            The dictionary representation of the dataclass.
        """
        return {
            f.name: maybe_to_dict(getattr(self, f.name))
            for f in fields(self)
            if not f.name.startswith("_")
        }


def maybe_to_dict(data):
    if isinstance(data, BaseData):
        return data.to_dict()

    return data
