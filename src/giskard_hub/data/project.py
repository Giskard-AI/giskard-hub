from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ._base import BaseData
from ._entity import Entity


@dataclass
class FailureCategory(BaseData):
    """Failure Category

    Attributes
    ----------
    identifier : str
        The identifier of the failure category.
    title : str
        The title of the failure category.
    description : str
        The description of the failure category.
    """

    identifier: str
    title: str
    description: str


@dataclass
class Project(Entity):
    """Project

    Attributes
    ----------
    name : str
        The name of the project.
    description : str, optional
        The description of the project.
    failure_categories : List[FailureCategory]
    """

    name: str
    description: str = ""
    failure_categories: List[FailureCategory] = field(default_factory=list)
