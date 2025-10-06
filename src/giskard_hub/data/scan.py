from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from giskard_hub.data._entity import EntityWithTaskProgress
from giskard_hub.data.knowledge_base import KnowledgeBase
from giskard_hub.data.model import Model
from giskard_hub.data.task import TaskProgress

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
    model: Model
    project_id: str
    knowledge_base: Optional[KnowledgeBase] = field(default=None)
    start_datetime: Optional[datetime] = field(default=None)
    grade: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, str], **kwargs) -> "ScanResult":
        data = dict(data)

        data["model"] = Model.from_dict(data["model"], **kwargs)
        data["knowledge_base"] = (
            KnowledgeBase.from_dict(data["knowledge_base"], **kwargs)
            if data.get("knowledge_base")
            else None
        )
        # Convert status to progress for EntityWithTaskProgress compatibility
        data["progress"] = (
            TaskProgress.from_dict(data.get("status")) if data.get("status") else None
        )

        return super().from_dict(data, **kwargs)

    @property
    def resource(self) -> str:
        return "scan_results"
