from __future__ import annotations

from dataclasses import dataclass

from ._entity import Entity


@dataclass
class Project(Entity):
    """Project

    Attributes
    ----------
    name : str
        The name of the project.
    description : str, optional
        The description of the project.
    """

    name: str
    description: str = ""
