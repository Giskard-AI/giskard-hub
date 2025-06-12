from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ._base import BaseData


# Backend DTO
@dataclass
class TestCaseCheckConfig(BaseData):
    identifier: str
    assertions: List[Dict[str, Any]]
    enabled: bool


# SDK DTO
@dataclass
class CheckConfig(BaseData):
    identifier: str
    params: Optional[Dict[str, Any]] = None
    enabled: bool = True
