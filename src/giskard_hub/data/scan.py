from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from dateutil import parser

from giskard_hub.data._entity import EntityWithTaskProgress
from giskard_hub.data.chat import ChatMessageWithMetadata
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


class ReviewStatus(str, Enum):
    PENDING = "pending"
    IGNORED = "ignored"
    ACKNOWLEDGED = "acknowledged"
    CORRECTED = "corrected"


@dataclass
class AttemptError(BaseData):
    message: str


@dataclass
class ProbeAttempt(BaseData):
    id: str
    probe_result_id: str

    messages: list[ChatMessageWithMetadata]
    metadata: dict[str, Any]

    severity: Severity
    review_status: ReviewStatus
    reason: str
    error: AttemptError | None = field(default=None)


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

    metrics: List[ScanMetric] | None = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ProbeResult":
        data = dict(data)

        # Convert status to progress for EntityWithTaskProgress compatibility
        if data.get("status"):
            data["progress"] = TaskProgress.from_dict(data.get("status"))
        if data.get("metrics"):
            data["metrics"] = [
                ScanMetric.from_dict(metric) for metric in data.get("metrics")
            ]

        return super().from_dict(data, **kwargs)

    @property
    def attempts(self) -> List[ProbeAttempt]:
        if not self.id:
            raise ValueError("ProbeResult must have an ID to fetch attempts.")
        return self._client.get(f"/probes/{self.id}/attempts", cast_to=List[ProbeAttempt])

    @property
    def resource(self) -> str:
        return "probes"


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
    generator_metadata: Dict[str, Any] = field(default_factory=dict)
    target_info: Dict[str, Any] = field(default_factory=dict)
    scan_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ScanResult":
        data = dict(data)

        # Convert nested objects
        data["model"] = Model.from_dict(data["model"], **kwargs)
        if data.get("knowledge_base"):
            data["knowledge_base"] = KnowledgeBase.from_dict(
                data["knowledge_base"], **kwargs
            )
        if data.get("start_datetime"):
            data["start_datetime"] = parser.parse(data["start_datetime"])
        if data.get("end_datetime"):
            data["end_datetime"] = parser.parse(data["end_datetime"])
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
    def probes(self) -> List[ProbeResult]:
        if not self.id:
            raise ValueError("ScanResult must have an ID to fetch probes.")
        return self._client.get(f"/scans/{self.id}/probes", cast_to=List[ProbeResult])

    @property
    def resource(self) -> str:
        return "scan_results"
