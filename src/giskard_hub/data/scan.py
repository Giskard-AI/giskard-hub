from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List

from giskard_hub.data._entity import EntityWithTaskProgress
from giskard_hub.data.knowledge_base import KnowledgeBase
from giskard_hub.data.model import Model

from ..data._base import BaseData


class Severity(int, Enum):
    SAFE = 0
    MINOR = 10
    MAJOR = 20
    CRITICAL = 30


class ScanMetric(BaseData):
    severity: Severity
    count: int


@dataclass
class ProbeResult(EntityWithTaskProgress):
    scan_result_id: str
    probe_lidar_id: str
    probe_name: str
    probe_description: str
    probe_tags: List[str]
    probe_category: str

    metrics: List[ScanMetric] | None

    @classmethod
    def from_dict(cls, data: Dict[str, str], **kwargs) -> "ProbeResult":
        data = dict(data)

        # Convert status to progress for EntityWithTaskProgress compatibility
        data["progress"] = data.get("status", None)

        return super().from_dict(data, **kwargs)


@dataclass
class ScanResult(EntityWithTaskProgress):
    project_id: str | None
    model: Model
    knowledge_base: KnowledgeBase | None = None
    start_datetime: datetime | None = None
    grade: str | None

    @classmethod
    def from_dict(cls, data: Dict[str, str], **kwargs) -> "ScanResult":
        data = dict(data)

        # Convert status to progress for EntityWithTaskProgress compatibility
        data["progress"] = data.get("status", None)

        return super().from_dict(data, **kwargs)
