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


class ScanType(str, Enum):
    DEFAULT = "default"
    QUICK = "quick"
    IN_DEPTH = "in_depth"


@dataclass
class ProbeErrorSummary(BaseData):
    probe_lidar_id: str
    original_error: str
    trace: str


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
    end_datetime: Optional[datetime] = field(default=None)
    grade: Optional[str] = field(default=None)
    lidar_version: str = field(default="unknown")
    tags: List[str] = field(default_factory=list)
    scan_type: ScanType = field(default=ScanType.DEFAULT)
    errors: List[ProbeErrorSummary] = field(default_factory=list)
    generator_metadata: Dict[str, any] = field(default_factory=dict)
    target_info: Dict[str, any] = field(default_factory=dict)
    scan_metadata: Dict[str, any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, str], **kwargs) -> "ScanResult":
        data = dict(data)

        # Convert nested objects
        data["model"] = Model.from_dict(data["model"], **kwargs)
        if data.get("knowledge_base"):
            data["knowledge_base"] = KnowledgeBase.from_dict(
                data["knowledge_base"], **kwargs
            )
        if data.get("start_datetime"):
            data["start_datetime"] = datetime.fromisoformat(data["start_datetime"])
        if data.get("end_datetime"):
            data["end_datetime"] = datetime.fromisoformat(data["end_datetime"])
        if data.get("scan_type"):
            data["scan_type"] = ScanType(data.get("scan_type"))
        if data.get("errors"):
            data["errors"] = [
                ProbeErrorSummary.from_dict(err) for err in data.get("errors")
            ]
        # Convert status to progress for EntityWithTaskProgress compatibility
        if data.get("status"):
            data["progress"] = TaskProgress.from_dict(data.get("status"))

        return super().from_dict(data, **kwargs)

    @property
    def resource(self) -> str:
        return "scan_results"
