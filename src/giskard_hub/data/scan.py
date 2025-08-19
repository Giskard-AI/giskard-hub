from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from dateutil import parser

from giskard_hub.data._entity import EntityWithTaskProgress
from giskard_hub.data.chat import ChatMessageWithMetadata
from giskard_hub.data.knowledge_base import KnowledgeBase
from giskard_hub.data.model import Model
from giskard_hub.data.task import TaskProgress

from ..data._base import BaseData


class ScanGrade(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    N_A = "N/A"


class Severity(IntEnum):
    SAFE = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3


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

    messages: List[ChatMessageWithMetadata]
    metadata: Dict[str, Any]

    severity: Severity = Severity.SAFE
    review_status: ReviewStatus
    reason: str
    error: AttemptError | None = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ProbeAttempt":
        data = dict(data)

        # Convert nested objects
        if data.get("messages"):
            data["messages"] = [
                ChatMessageWithMetadata.from_dict(msg) for msg in data.get("messages")
            ]
        if data.get("error"):
            data["error"] = AttemptError.from_dict(data.get("error"))

        data["review_status"] = ReviewStatus(
            data.get("review_status"), ReviewStatus.PENDING
        )
        data["severity"] = Severity(data.get("severity"), Severity.SAFE)

        return super().from_dict(data, **kwargs)

    @property
    def reviewed(self) -> bool:
        return self.review_status != ReviewStatus.PENDING


@dataclass
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
        return [
            ProbeAttempt.from_dict(r)
            for r in self._client.get(f"/probes/{self.id}/attempts")["items"]
        ]

    @property
    def resource(self) -> str:
        return "probes"


@dataclass
class ProbeErrorSummary(BaseData):
    """Probe error summary."""

    probe_lidar_id: str
    original_error: str
    trace: str


@dataclass
class ScanResult(EntityWithTaskProgress):
    model: Model
    project_id: str
    knowledge_base: Optional[KnowledgeBase] = field(default=None)
    start_datetime: Optional[datetime] = field(default=None)
    end_datetime: Optional[datetime] = field(default=None)
    grade: Optional[str] = field(default=None)
    lidar_version: str = field(default="dev")
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
        data["grade"] = ScanGrade(data.get("grade", ScanGrade.N_A))
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
    def results(self) -> List[ProbeResult]:
        if not self.id:
            raise ValueError("ScanResult must have an ID to fetch probes.")
        return [
            ProbeResult.from_dict(r)
            for r in self._client.get(f"/scans/{self.id}/probes")["items"]
        ]

    @property
    def resource(self) -> str:
        return "scan_results"

    def refresh(self) -> "ScanResult":
        """Refresh the scan result from the Hub."""
        if not self._client or not self.id:
            raise ValueError(
                "This scan result instance is detached or unsaved and cannot be refreshed."
            )

        data = self._client.scans.retrieve(self.id)
        self._hydrate(data)

        return self


@dataclass
class CreateScanRequest(BaseData):
    """Request to create a scan."""

    model_id: str
    knowledge_base_id: str | None = None
    tags: List[str] | None = None
