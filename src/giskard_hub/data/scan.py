from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Dict, List

from ._base import BaseData
from ._entity import Entity
from .chat_test_case import ChatMessage
from .task import TaskProgress


class ScanGrade(str, Enum):
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


class ReviewStatus(str, Enum):
    PENDING = "pending"
    IGNORED = "ignored"
    ACKNOWLEDGED = "acknowledged"
    CORRECTED = "corrected"


@dataclass
class ProbeErrorSummary(BaseData):
    """Probe error summary."""

    probe_lidar_id: str
    original_error: str
    trace: str


@dataclass
class ProbeAttempt(Entity):
    """Probe attempt."""

    probe_result_id: str
    successful: bool
    messages: List[ChatMessage] = field(default_factory=list)
    severity: Severity = Severity.SAFE
    attempt_metadata: Dict[str, Any] = field(default_factory=dict)
    review_status: ReviewStatus = ReviewStatus.PENDING

    @property
    def reviewed(self) -> bool:
        return self.review_status != ReviewStatus.PENDING

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ProbeAttempt":
        data = dict(data)
        data["messages"] = [
            ChatMessage.from_dict(msg) for msg in data.get("messages", [])
        ]
        data["severity"] = Severity(data.get("severity", Severity.SAFE))
        data["review_status"] = ReviewStatus(
            data.get("review_status", ReviewStatus.PENDING)
        )
        return super().from_dict(data, **kwargs)


@dataclass
class ProbeResult(Entity):
    """Probe result."""

    scan_result_id: str
    probe_lidar_id: str
    vulnerable: bool
    severity: Severity = Severity.SAFE
    attempts: List[ProbeAttempt] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ProbeResult":
        data = dict(data)
        data["severity"] = Severity(data.get("severity", Severity.SAFE))
        data["attempts"] = [
            ProbeAttempt.from_dict(attempt, **kwargs)
            for attempt in data.get("attempts", [])
        ]
        return super().from_dict(data, **kwargs)


@dataclass
class ScanResult(Entity):  # pylint: disable=too-many-instance-attributes
    """Scan result."""

    project_id: str
    model_id: str
    knowledge_base_id: str | None = None
    errors: List[ProbeErrorSummary] = field(default_factory=list)
    grade: ScanGrade = ScanGrade.N_A
    lidar_version: str = "dev"
    generator_metadata: Dict[str, Any] = field(default_factory=dict)
    target_info: Dict[str, Any] = field(default_factory=dict)
    tags_filter: List[str] = field(default_factory=list)
    scan_metadata: Dict[str, Any] = field(default_factory=dict)
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    status: TaskProgress | None = None
    results: List[ProbeResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ScanResult":
        data = dict(data)
        data["grade"] = ScanGrade(data.get("grade", ScanGrade.N_A))
        data["errors"] = [
            ProbeErrorSummary.from_dict(error) for error in data.get("errors", [])
        ]
        data["status"] = (
            TaskProgress.from_dict(data["status"]) if data.get("status") else None
        )
        data["results"] = [
            ProbeResult.from_dict(result, **kwargs)
            for result in data.get("results", [])
        ]
        # Parse datetime strings if they exist
        if data.get("start_datetime"):
            data["start_datetime"] = datetime.fromisoformat(
                data["start_datetime"].replace("Z", "+00:00")
            )
        if data.get("end_datetime"):
            data["end_datetime"] = datetime.fromisoformat(
                data["end_datetime"].replace("Z", "+00:00")
            )
        return super().from_dict(data, **kwargs)

    def refresh(self) -> ScanResult:
        """Refresh the scan result from the Hub."""
        if not self._client or not self.id:
            raise ValueError(
                "This scan result instance is detached or unsaved and cannot be refreshed."
            )

        data = self._client.scans.retrieve(self.id)
        self._hydrate(data)

        return self

    def is_running(self) -> bool:
        """Check if the scan is running."""
        return self.status and self.status.status == "running"

    def is_finished(self) -> bool:
        """Check if the scan is finished."""
        return self.status and self.status.status == "finished"

    def is_errored(self) -> bool:
        """Check if the scan terminated with an error."""
        return self.status and self.status.status == "error"


@dataclass
class CreateScanRequest(BaseData):
    """Request to create a scan."""

    model_id: str
    knowledge_base_id: str | None = None
    tags: List[str] | None = None
