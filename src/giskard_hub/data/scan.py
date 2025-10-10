from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from ._base import BaseData
from ._entity import Entity, EntityWithTaskProgress
from .chat import ChatMessageWithMetadata
from .knowledge_base import KnowledgeBase
from .model import Model
from .task import TaskProgress


@dataclass
class ScanCategory(BaseData):
    id: str
    title: str
    description: str
    owasp_id: Optional[str] = field(default=None)


SCAN_CATEGORIES = [
    ScanCategory(
        id="gsk:threat-type='prompt-injection'",
        title="Prompt Injection",
        description="Attempts to manipulate model behavior through crafted inputs",
        owasp_id="OWASP LLM01",
    ),
    ScanCategory(
        id="gsk:threat-type='data-privacy-exfiltration'",
        title="Data Privacy & Exfiltration",
        description="Unauthorized exposure of sensitive or private information",
        owasp_id="OWASP LLM05",
    ),
    ScanCategory(
        id="gsk:threat-type='harmful-content-generation'",
        title="Harmful Content Generation",
        description="Generation of harmful, offensive, or inappropriate content",
    ),
    ScanCategory(
        id="gsk:threat-type='excessive-agency'",
        title="Excessive Agency",
        description="Model given too much autonomy or permissions beyond intended scope",
        owasp_id="OWASP LLM06",
    ),
    ScanCategory(
        id="gsk:threat-type='internal-information-exposure'",
        title="Internal Information Exposure",
        description="Exposure of internal system information or model architecture",
        owasp_id="OWASP LLM01-07",
    ),
    ScanCategory(
        id="gsk:threat-type='training-data-extraction'",
        title="Training Data Extraction",
        description="Attempts to extract training data from the model",
        owasp_id="OWASP LLM02",
    ),
    ScanCategory(
        id="gsk:threat-type='denial-of-service'",
        title="Denial of Service",
        description="Resource exhaustion attacks against the model or system",
        owasp_id="OWASP LLM10",
    ),
    ScanCategory(
        id="gsk:threat-type='hallucination'",
        title="Hallucination / Misinformation",
        description="Generation of false or misleading information presented as fact",
        owasp_id="OWASP LLM08",
    ),
    ScanCategory(
        id="gsk:threat-type='misguidance-and-unauthorized-advice'",
        title="Misguidance & Unauthorized Advice",
        description="Providing inappropriate guidance or advice outside intended scope",
    ),
    ScanCategory(
        id="gsk:threat-type='legal-and-financial-risk'",
        title="Legal & Financial Risk",
        description="Responses that could create legal or financial liability",
    ),
    ScanCategory(
        id="gsk:threat-type='brand-damaging-and-reputation'",
        title="Brand Damaging & Reputation",
        description="Responses that could damage brand reputation or public trust",
    ),
]


class ScanGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    N_A = "N/A"


class Severity(IntEnum):
    SAFE = 0
    MINOR = 10
    MAJOR = 20
    CRITICAL = 30


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
class ProbeAttempt(Entity):
    probe_result_id: str
    messages: List[ChatMessageWithMetadata]
    metadata: Dict[str, Any]
    severity: Severity
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
            data.get("review_status", ReviewStatus.PENDING.value),
        )

        data["severity"] = Severity(data.get("severity", Severity.SAFE.value))

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
        return self._client.scans.list_attempts(self.id)

    @property
    def resource(self) -> str:
        return "scans"

    def refresh(self) -> "ProbeResult":
        """Overwrite refresh method to get the entity data from the API."""
        if not self._client or not self.id:
            raise ValueError(
                f"This {self.resource} instance with id '{self.id}' is detached or unsaved and cannot be refreshed."
            )

        # Use the abstract resource property for the API call
        resource = self.resource
        data = getattr(self._client, resource).retrieve_probe(self.id)
        self._hydrate(data)

        return self


@dataclass
class ScanResult(EntityWithTaskProgress):
    model: Model
    project_id: str
    knowledge_base: Optional[KnowledgeBase] = field(default=None)
    grade: Optional[ScanGrade] = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], **kwargs) -> "ScanResult":
        data = dict(data)

        # Convert nested objects
        data["model"] = Model.from_dict(data["model"], **kwargs)

        if data.get("knowledge_base"):
            data["knowledge_base"] = KnowledgeBase.from_dict(
                data["knowledge_base"], **kwargs
            )

        if data.get("grade"):
            data["grade"] = ScanGrade(data.get("grade"))

        # Convert start_datetime to created_at for Entity compatibility
        if data.get("start_datetime"):
            data["created_at"] = data["start_datetime"]
            del data["start_datetime"]

        # Convert end_datetime to updated_at for Entity compatibility
        if data.get("end_datetime"):
            data["updated_at"] = data["end_datetime"]
            del data["end_datetime"]

        # Convert status to progress for EntityWithTaskProgress compatibility
        if data.get("status"):
            data["progress"] = TaskProgress.from_dict(data.get("status"))
            del data["status"]

        return super().from_dict(data, **kwargs)

    @property
    def results(self) -> List[ProbeResult]:
        if not self.id:
            raise ValueError("ScanResult must have an ID to fetch probes.")
        return self._client.scans.list_probes(scan_id=self.id)

    @property
    def resource(self) -> str:
        return "scans"

    def refresh(self) -> "ScanResult":
        """Refresh the scan result from the Hub."""
        if not self._client or not self.id:
            raise ValueError(
                "This scan result instance is detached or unsaved and cannot be refreshed."
            )

        data = self._client.scans.retrieve(self.id)
        self._hydrate(data)

        return self
